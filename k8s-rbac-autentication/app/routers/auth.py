from fastapi import APIRouter, Depends, HTTPException, status # type: ignore
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from sqlalchemy.orm import Session # type: ignore
from app.database import get_db
from app.models.user_models import User
from app.schemas.dataset import UserCreate, UserResponse
from app.utils.security import create_access_token, verify_password, get_password_hash, verify_token, is_valid_password # Corrigido: importando a função is_valid_password
from fastapi import Security # type: ignore
from sqlalchemy.future import select # type: ignore
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Endpoint de registro de usuário (sem alterações aqui)
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if not is_valid_password(user.password): # type: ignore
        raise HTTPException(status_code=400, detail="A senha é muito fraca.")
    try:
        logger.info("Iniciando registro do usuário: %s", user.username)

        # Verifica se o usuário já existe
        query = select(User).where(User.username == user.username)
        result = await db.execute(query)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.warning("Tentativa de registro com username já existente: %s", user.username)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        # Cria o novo usuário
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, hashed_password=hashed_password)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        logger.info("Usuário registrado com sucesso: %s", user.username)
        return new_user

    except HTTPException as http_ex:
        logger.error("Erro de validação: %s", http_ex.detail)
        raise http_ex

    except Exception as e:
        logger.error("Erro inesperado ao registrar usuário %s: %s", user.username, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao registrar usuário",
        )

# Endpoint de login corrigido (com JSON)
@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint de login para autenticar o usuário e gerar o JWT.
    """
    # Verificando se os dados de entrada são válidos
    if not user_credentials.username or not user_credentials.password:
        logger.error("Campos obrigatórios ausentes: username ou password.")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Campos obrigatórios ausentes: username ou password.",
        )

    # Verificando se o usuário existe
    query = select(User).where(User.username == user_credentials.username)  # Corrigido para usar `select`
    result = await db.execute(query)  # Executar a consulta assíncrona
    user = result.scalars().first()  # Obter o primeiro usuário encontrado

    # Se o usuário não for encontrado ou a senha estiver errada
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        logger.warning("Credenciais inválidas para o usuário: %s", user_credentials.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gerando o token JWT
    access_token = create_access_token(data={"sub": user.username})
    logger.info("Login bem-sucedido para o usuário: %s", user_credentials.username)
    
    return {"access_token": access_token, "token_type": "bearer"}

# Rota protegida para testar se o JWT funciona
@router.get("/protected")
async def protected_route(current_user: User = Depends(verify_token)):
    """
    Exemplo de rota protegida que requer autenticação via token JWT.
    """
    return {"message": f"Hello {current_user.username}, you are authenticated!"}
