# App Database

***

## <mark style="color:red;">Database</mark>

Vamos criar nossos arquivos que executaram nossa aplicação de banco de dados

***

1. Criaremos nosso Dockerfile

```bash
vim Dockerfile
```

```docker
FROM mysql:5.7

WORKDIR /var/lib/mysql/
ENV MYSQL_ROOT_PASSWORD=Senha123
ENV MYSQL_DATABASE=mydatabase
ADD sql.sql /docker-entrypoint-initdb.d
EXPOSE 3306
```

***

2. Vamos buildar o Dockerfile criado

```
docker build -t danncastro/mydatabase:1.0 .
```

***

3. Vamos subir essa imagem para o repositório do DockerHub

```
docker push danncastro/mydatabase:1.0
```

***

4. Como informado no ADD do Dockerfile, vamos criar nossa tabela do sql que será executada no build da imagem

```bash
vim sql.sql
```

```sql
CREATE TABLE mensagens (
    id int,
    nome varchar(50),
    mensagem varchar(100)
);
```

***

5. Vamos agora criar nosso arquivo de deployment

```bash
vim mysqldb.yml
```

```yaml
apiVersion: v1
kind: Deployment
metada:
  name: mysqldb
spec:
  selector:
    matchLabels:
      app: mysqldb
  template:
    metadata:
      labels:
        app: mysqldb
    spec:
      containers:
      - name: mysqldb
        image: danncastro/mydatabase:1.0
        imagePullPolicy: Always
        ports:
        - containerPort: 3306
```

***

6. Vamos criar nosso serviço para que haja comunicação com o banco de dados

```bash
vim mysql-connection.yml
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-connection
spec:
  ports:
  - port: 3306
  selector:
    app: mysqldb
  clusterIP: None
```

***

7. Vamos criar nosso deployment e nosso serviço

```bash
kubectl create mysqldb.yaml
```

```bash
kubectl create mysql-connection.yml
```

***

8. Podemos validar nossos recursos criados

```bash
kubectl get pods
```

> NAME                        READY          STATUS                            RESTARTS              AGE
>
> mysqldb                    1/1                 Running                            0                              10s

```
kubectl get svc
```

> NAME                         TYPE                    CLUSTER-IP        EXTERNAL-IP        PORT(S)           AGE
>
> kubernetes                 ClusterIP              10.44.0.2             \<none>                  443/TCP         3d16h
>
> mysql-connection      ClusterIP              None                   \<none>                   3306/TCP       20s

***

## <mark style="color:red;">Backend</mark>

Vamos criar nosso backend que será utilizado para conectar com nosso banco de dados criado anteriormente.

***

1. Vamos criar nosso arquivo de conexão

```bash
vim conexao.php
```

```php
<?php

$servername = "mysql-connection";
$username   = "root";
$password   = "Senha123";
$database   = "mydatabase";

// Criar conexão

$link       = new mysqli($servername, $username, $password, $database);

/* Check Connection */
if (mysqli_connect_error()){
    printf("Connect Failed: %s\n", mysqli_connect_error());
    exit();
}

?>
```

***

2. Vamos criar também um index.php para coletar dados de um formulário que estará exposto no frontend

```php
<?
header("Access-Control-Allow-Origin: *");
include 'conexao.php';

$id          = rand(1, 999);
$name        = $_POST["nome"];
$mensagem    = $_POST["mensagem"];

$query       = "INSERT INTO mensagem(id, nome, mensagem) VALUES ('$id', '$nome', '$mensagem')";

if ($link->query($query) === TRUE) {
  echo "New record created sucessfully";
}else{
  echo "Error: " .$link->error;
}
?>
```

***

3. Vamos criar nosso Dockerfile de praxe para buildar uma imagem e enviar ao DockerHub;

```bash
vim Dockerfile
```

```docker
FROM        php:7.4-apache

WORKDIR     /var/www/html
COPY        index.html /var/www/html
COPY        conexao.php /var/www/html

RUN         apt-get update && apt-get install -y \
                libfreetype6-dev \
                libjpeg62-turbo-dev \
                libpng-dev \
            && docker-php-ext-configure gd --with-freetype --with-jpeg \
            && docker-php-ext-install -j$(nproc) gd \
            && docker-php-ext-install pdo_mysql \
            && docker-php-ext-install mysqli

EXPOSE      80
```

***

4. Vamos buildar nossa imagem.

```
docker build -t danncastro/phpbackend:1.0 .
```

***

5. Subir para o DockerHub

```
docker push danncastro/phpbackend:1.0
```

***

6. Vamos agora criar nosso deployment de fato que será utilizado para subir o backend da aplicação. Neste exemplo iremos colocar o serviço no mesmo arquivo de deployment.

```bash
vim phpback.yml
```

```yaml
apiVersion: v1
kind: Deployment
metada:
  name: php-backend
  labels:
    app: php-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: php-backend
  template:
    metadata:
      labels:
        app: php-backend
    spec:
      containers:
      - name: php-backend
        image: danncastro/phpbackend:1.0
        imagePullPolicy: Always
        ports:
        - containerPort: 80
  
---

apiVersion: v1
kind: Service
metada:
  name: php-service
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30007
  selector:
    app: php-backend
    
```

***

7. Vamos deploys nossos 2 recursos descritos no arquivo acima.

```bash
kubectl apply -f phpback.yml
```

***

8. Se visualizarmos os pods veremos que além do mysql termos mais outras 2 pods que foram a quantidade de replicas informadas no arquivo de deployment, assim como também um novo serviço.

```bash
kubectl get po
```

> NAME                                  READY          STATUS                            RESTARTS              AGE
>
> mysqldb                               1/1                 Running                            0                              10s
>
> php-backend -token1         1/1                 Running                             0                              10s
>
> php-backend -token2        1/1                  Running                            0                              10s

```bash
kubectl get no
```

> NAME                         TYPE                    CLUSTER-IP      EXTERNAL-IP      PORT(S)               AGE
>
> kubernetes                 ClusterIP              10.44.0.2           \<none>                443/TCP              3d16h
>
> mysql-connection      ClusterIP              None                 \<none>                3306/TCP            6m30s
>
> php-service                NodePort             10.8.9.57           \<none>                80:30007/TCP     20s

***

## <mark style="color:red;">Frontend</mark>

Como nosso frontend está sendo executado local, vamos validar qual o ip do cluster e acessar através dele.

```
kubectl get no -owide
```

> saída ip cluster

***

1. Vamos criar nosso arquivo js

```bash
vim js.js
```

```javascript
$("#button-blue").on("click", function() {
    
    var txt_nome = $("#name").val();
    var txt_email = $("#email").val();
    var txt_comentario = $("#comment").val();

    $.ajax({
        url: "http://ip_cluster:30007/",
        
        type: "post",
        data: {nome: txt_nome, comentario: txt_comentario, email: txt_email},
        beforeSend: function() {
        
            console.log("Tentando enviar os dados....");

        }
    }).done(function(e) {
        alert("Dados Salvos");
    })

});
```

***

2. Criaremos agora nosso arquivo de index.html

```bash
vim index.html
```

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="css.css" media="screen" />


    <title>Formulário</title>
</head>
<body>
    <div id="form-main">
        <div id="form-div">
          <form class="form" form id="contact" method="post">
            
            <p class="name">
              <input name="name" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" placeholder="Nome" id="name" />
            </p>
            
            <p class="email">
              <input name="email" type="text" class="validate[required,custom[email]] feedback-input" id="email" placeholder="Email" />
            </p>
            
            <p class="text">
              <textarea name="text" class="validate[required,length[6,300]] feedback-input" id="comment" placeholder="Comentário"></textarea>
            </p>
            
            
            <div class="submit">
              <button type="button" value="SEND" id="button-blue">Enviar</button>
              <div class="ease"></div>
            </div>
          </form>
        </div>
        
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="js.js"> </script>
</body>

</html>
```

***

3. Criaremos também nosso arquivo CSS

```bash
vim css.css
```

```css
@import url(https://fonts.googleapis.com/css?family=Montserrat:400,700);

html{    background:url(http://thekitemap.com/images/feedback-img.jpg) no-repeat;
  background-size: cover;
  height:100%;
}

#feedback-page{
	text-align:center;
}

#form-main{
	width:100%;
	float:left;
	padding-top:0px;
}

#form-div {
	background-color:rgba(72,72,72,0.4);
	padding-left:35px;
	padding-right:35px;
	padding-top:35px;
	padding-bottom:50px;
	width: 450px;
	float: left;
	left: 50%;
	position: absolute;
  margin-top:30px;
	margin-left: -260px;
  -moz-border-radius: 7px;
  -webkit-border-radius: 7px;
}

.feedback-input {
	color:#3c3c3c;
	font-family: Helvetica, Arial, sans-serif;
  font-weight:500;
	font-size: 18px;
	border-radius: 0;
	line-height: 22px;
	background-color: #fbfbfb;
	padding: 13px 13px 13px 54px;
	margin-bottom: 10px;
	width:100%;
	-webkit-box-sizing: border-box;
	-moz-box-sizing: border-box;
	-ms-box-sizing: border-box;
	box-sizing: border-box;
  border: 3px solid rgba(0,0,0,0);
}

.feedback-input:focus{
	background: #fff;
	box-shadow: 0;
	border: 3px solid #3498db;
	color: #3498db;
	outline: none;
  padding: 13px 13px 13px 54px;
}

.focused{
	color:#30aed6;
	border:#30aed6 solid 3px;
}

/* Icons ---------------------------------- */
#name{
	background-image: url(http://rexkirby.com/kirbyandson/images/name.svg);
	background-size: 30px 30px;
	background-position: 11px 8px;
	background-repeat: no-repeat;
}

#name:focus{
	background-image: url(http://rexkirby.com/kirbyandson/images/name.svg);
	background-size: 30px 30px;
	background-position: 8px 5px;
  background-position: 11px 8px;
	background-repeat: no-repeat;
}

#email{
	background-image: url(http://rexkirby.com/kirbyandson/images/email.svg);
	background-size: 30px 30px;
	background-position: 11px 8px;
	background-repeat: no-repeat;
}

#email:focus{
	background-image: url(http://rexkirby.com/kirbyandson/images/email.svg);
	background-size: 30px 30px;
  background-position: 11px 8px;
	background-repeat: no-repeat;
}

#comment{
	background-image: url(http://rexkirby.com/kirbyandson/images/comment.svg);
	background-size: 30px 30px;
	background-position: 11px 8px;
	background-repeat: no-repeat;
}

textarea {
    width: 100%;
    height: 150px;
    line-height: 150%;
    resize:vertical;
}

input:hover, textarea:hover,
input:focus, textarea:focus {
	background-color:white;
}

#button-blue{
	font-family: 'Montserrat', Arial, Helvetica, sans-serif;
	float:left;
	width: 100%;
	border: #fbfbfb solid 4px;
	cursor:pointer;
	background-color: #3498db;
	color:white;
	font-size:24px;
	padding-top:22px;
	padding-bottom:22px;
	-webkit-transition: all 0.3s;
	-moz-transition: all 0.3s;
	transition: all 0.3s;
  margin-top:-4px;
  font-weight:700;
}

#button-blue:hover{
	background-color: rgba(0,0,0,0);
	color: #0493bd;
}
	
.submit:hover {
	color: #3498db;
}
	
.ease {
	width: 0px;
	height: 74px;
	background-color: #fbfbfb;
	-webkit-transition: .3s ease;
	-moz-transition: .3s ease;
	-o-transition: .3s ease;
	-ms-transition: .3s ease;
	transition: .3s ease;
}

.submit:hover .ease{
  width:100%;
  background-color:white;
}

@media only screen and (max-width: 580px) {
	#form-div{
		left: 3%;
		margin-right: 3%;
		width: 88%;
		margin-left: 0;
		padding-left: 3%;
		padding-right: 3%;
	}
}
```

***

### <mark style="color:red;">Testando a aplicação</mark>

1. Testaremos nossa aplicação executando no navegador o arquivo de index.html

***

2. Após executar alguns inputs na aplicação vamos validar se os dados foram adicionados ao banco

```bash
kubectl exec --stdin --tty mysqldb -- /bin/bash
```

```bash
mysql -uroot -p -h 127.0.0.1
```

```bash
use mydatabase;
select * FROM mensagens;
```

***

3. Delete todos os recursos criados.

```
kubectl delele pod --all
kubectl delete service --all
```

***
