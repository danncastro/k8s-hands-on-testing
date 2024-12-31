## Passo 2: Configuração do Banco de Dados

Para integrar a aplicação com o banco de dados PostgreSQL, utilizamos a biblioteca SQLAlchemy, que é um ORM (Object Relational Mapper). Isso permite interagir com o banco de dados usando objetos Python, em vez de escrever comandos SQL diretamente.

**1. Instalação das Dependências:**

- Instale as bibliotecas necessárias:
  - **sqlalchemy:** Biblioteca ORM para gerenciar o banco de dados.
  - **psycopg2:** Driver para conexão com PostgreSQL.

  ~~~bash
  pip install sqlalchemy psycopg2 --trusted-host pypi.python.org \
  --trusted-host pypi.org --trusted-host=files.pythonhosted.org
  ~~~

**2. Configuração do Arquivo ``database.py``**
No diretório **app/**, crie o arquivo ``database.py``. Este arquivo será responsável por configurar a conexão com o banco de dados e gerenciar sessões.

**3. Conexão ao Banco de Dados no Código**
Para garantir o gerenciamento eficiente das sessões de banco de dados durante as requisições, crie uma função chamada ``get_db`` no arquivo ``database.py``.

### Explicação do Código ``database.py``

**1. DATABASE_URL:**

- **Formato:** ``postgresql://<usuário>:<senha>@<host>:<porta>/<nome_do_banco>.``
- Substitua os valores pelos dados do seu banco.

**2. create_engine:**

- Configura o motor de conexão com o PostgreSQL, que gerencia a comunicação com o banco.

**3. SessionLocal:**

- Fábrica de sessões para executar operações no banco de dados.
  - **autocommit=False:** Exige que as transações sejam explicitamente confirmadas.
  - **autoflush=False:** Evita atualizações automáticas dos objetos antes de cada consulta.

**4. Base:**

- Classe base usada para definir modelos que representam tabelas do banco de dados.

**5. get_db():**

- Essa função será usada nas rotas para obter uma sessão do banco de dados automaticamente.
  - ``yield:`` Permite que o FastAPI injete o objeto de sessão no endpoint.
  - ``finally:`` Garante que a conexão será fechada após o uso, evitando vazamento de recursos.

---

## Passo 3: Criando o Modelo de Usuário

Agora, vamos criar o modelo de dados do usuário. Esse modelo será usado pelo SQLAlchemy para mapear a tabela users no banco de dados. Ele também servirá como base para as operações relacionadas a usuários, como autenticação e registro.

**1. Configuração do Arquivo ``user.py`` em models**

- Navegue até o diretório **models/** e crie o arquivo ``user.py``.

### Explicação do Código ``app/models/user.py``

**1. Classe User:**

- Representa a tabela users no banco de dados.
- Herda de Base, que foi configurada no arquivo ``database.py``.
- **Atributos:**
  - **id:** Identificador único de cada usuário. É a chave primária da tabela.
  - **username:** Nome de usuário único para login.
  - **hashed_password:** Armazena a senha do usuário de forma segura (usaremos hashing para proteger as senhas).
  - **email:** Endereço de e-mail único para cada usuário.
- **Parâmetros de Coluna:**
  - **primary_key=True:** Define o atributo como chave primária.
  - **unique=True:** Garante que o valor seja único na tabela.
  - **index=True:** Cria índices para otimizar buscas.

---

## Passo 4: Criando os Schemas para Validação

Agora, precisamos criar os esquemas usando Pydantic para garantir que os dados de entrada nas rotas sejam válidos. Vamos começar criando um esquema para o usuário.

**1. Criação do arquivo ``dataset.py`` dentro do diretório schemas/:**

### Explicação do Código ``app/schemas/dataset.py``

**1. UserBase:**

- Contém os campos comuns entre os diferentes tipos de dados do usuário (como username e email).

**2. UserCreate:**

- Define os campos necessários para criar um novo usuário, incluindo a senha.

**3. UserInDB:**

- Representa um usuário existente no banco de dados, incluindo o ID e a transformação para JSON usando orm_mode.

**4. UserOut:**

- Representa um usuário para exibição (sem a senha).

---

## Passo 5: Implementando as Rotas de Autenticação ``auth.py``

Em seguida, criaremos as rotas de autenticação. Isso incluirá endpoints para registrar e autenticar o usuário, com a geração de um JWT após o login.

**1. Criação do arquivo ``auth.py`` em routers/**

### Explicação do Código ``app/routers/auth.py``

**1. @router.post("/register"):**

- O ``@router.post`` é o decorador que mapeia a função ``register_user`` para o método **HTTP POST** no caminho **/register**. Isso significa que, quando uma solicitação **POST** for feita para ``http://<servidor>/register``, a função ``register_user`` será executada.
  - **response_model=schemas.UserOut:**
    - O parâmetro ``response_model`` indica ao modelo Pydantic que será usado para validar e formatar a resposta da API. Aqui, o modelo ``dataset.UserOut`` define como a resposta será estruturada. Ou seja, após a criação de um usuário, a API retornará um objeto **JSON** que segue a estrutura definida pelo ``UserOut`` (com os campos como id, username, email).

**2. A função register_user:**

- Ela é chamada sempre que uma solicitação **POST** é recebida na rota **/register**.
- A função recebe:
  - **user:** ``schemas.UserCreate:`` O corpo da requisição é automaticamente convertido para o esquema ``UserCreate``, o que permite que o FastAPI valide e converta os dados.
  - **db:** ``Session = Depends(database.get_db):`` O Depends injeta a dependência da sessão do banco de dados, ou seja, a função ``get_db`` vai garantir que a função tenha acesso à sessão do banco de dados para realizar as operações.

**3. login_user:**

- Valida as credenciais do usuário e, se forem válidas, gera um JWT.

---

## Passo 6: Lógica de Autenticação com JWT

- O objetivo é implementar a funcionalidade de login, onde o usuário envia suas credenciais (nome de usuário e senha), o sistema verifica essas credenciais no banco de dados, e se forem válidas, o sistema gera um token JWT (JSON Web Token) para autenticar o usuário em futuras requisições.

**1. Criação do arquivo ``auth_utils.py`` em utils/**
**2. Receber o nome de usuário e senha do cliente.**
**3. Validar as credenciais do usuário — buscar o usuário no banco de dados e comparar a senha fornecida com a senha mazenada de forma segura (com hash).**
**4. Gerar um token JWT para autenticação do usuário, que será utilizado para autorizar futuras requisições.**
**5. Retornar o token JWT para o cliente, que poderá usá-lo para autenticação nas próximas requisições.**

### Explicação do Código ``app/utils/ger_token.py``

  ~~~python
  from datetime import datetime, timedelta
  from jose import JWTError, jwt # type: ignore
  from typing import Optional
  from app import config

  # Chave secreta usada para codificar e decodificar o JWT
  SECRET_KEY = config.settings.SECRET_KEY
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 30

  def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
      to_encode = data.copy()

      if expires_delta:
          expire = datetime.utcnow() + expires_delta
      else:
          expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      to_encode.update({"exp": expire})

      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt
  ~~~

**1. Importações**
.

- **APIRouter:** O FastAPI usa o ``APIRouter`` para criar rotas de maneira modular. No caso, estamos criando uma rota de login.
- **Session:** Usamos Session do SQLAlchemy para interagir com o banco de dados.
- **CryptContext:** Da biblioteca passlib, usada para verificar se a senha fornecida pelo usuário corresponde à senha armazenada, que está de forma criptografada no banco de dados.
- **auth_utils:** Um módulo personalizado onde você terá a lógica para criar o token JWT.

**2. Criação do Contexto de Criptografia**
A biblioteca passlib é usada para criptografar as senhas e validá-las de forma segura. No caso, estamos utilizando o algoritmo bcrypt.

  ~~~python
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  ~~~

**3.  A Rota de Login**
A rota ``login_user`` é um **POST** que recebe um objeto ``UserCreate`` (definido em ``schemas.dataset.py``) com o nome de usuário e senha.

  ~~~python
  @router.post("/login")
  def login_user(user: dataset.UserCreate, db: Session = Depends(database.get_db)):
~~~

- Aqui, o FastAPI faz a validação automática da entrada com o Pydantic (``UserCreate``), garantindo que o corpo da requisição contenha os dados corretos.

**4. Verificação das Credenciais**
Primeiro, buscamos o usuário no banco de dados.

  ~~~python
  db_user = db.query(user_models.User).filter(user_models.User.username == user.username).first()
  ~~~

- Se o usuário não for encontrado ou a senha não corresponder ao valor armazenado (usando ``pwd_context.verify()``), a função retorna um erro ``401 Unauthorized``.

  ~~~python
  if db_user is None or not pwd_context.verify(user.password, db_user.hashed_password):
      raise HTTPException(status_code=401, detail="Credenciais inválidas")
  ~~~

**5. Geração do Token JWT**
Se as credenciais estiverem corretas, geramos um token JWT para o usuário. A função ``create_access_token`` será responsável por criar esse token. O JWT vai conter um **payload** com informações do usuário, que neste caso estamos utilizando o ``username`` como ``sub`` (subject).

  ~~~pythoon
  token = auth_utils.create_access_token(data={"sub": user.username})
  ~~~

- A função ``create_access_token`` pode estar definida em ``app/utils/auth_utils.py``, por exemplo.

**6. Retorno do Token**
Finalmente, retornamos o token JWT para o cliente em formato JSON. O cliente usará esse token para autenticação em futuras requisições.

  ~~~python
  return {"access_token": token, "token_type": "bearer"}
  ~~~

- O campo ``"token_type": "bearer"`` é uma convenção utilizada para indicar que o token é um Bearer Token, usado para autenticação.
