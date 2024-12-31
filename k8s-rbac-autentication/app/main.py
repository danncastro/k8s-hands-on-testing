from fastapi import FastAPI # type: ignore
from app.routers import auth2 # type: ignore

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Kubernetes RBAC Autentication",
    description="Aplicação com autenticação e integração ao Kubernetes",
    version="1.0.0",
)

# Inclui o roteador de autenticação
def include_routers():
    print("OK")
    app.include_router(auth2.router)
include_routers()

# Define uma rota simples de teste
@app.get("/")
def read_root():
    """
    Endpoint inicial da aplicação.
    Retorna uma mensagem de boas-vindas para o usuário.
    """
    return {"message": "Bem-vindo ao Kubernetes RBAC Autentication."}
