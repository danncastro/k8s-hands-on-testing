from fastapi import FastAPI # type: ignore
from app.routers import auth
from app.database import create_tables_sync
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.exceptions import RequestValidationError # type: ignore
from starlette.responses import JSONResponse # type: ignore
from starlette.exceptions import HTTPException as StarletteHTTPException # type: ignore
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Kubernetes RBAC Autentication",
    description="Aplicação com autenticação e integração ao Kubernetes",
    version="1.0.0",
)

# Configurar o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL do frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os headers
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

# Função assíncrona para inicializar as tabelas
async def init():
    logging.info("Iniciando a criação das tabelas no banco de dados...")
    await create_tables_sync()

# Chama a função assíncrona para criar as tabelas no banco de dados
@app.on_event("startup")
async def startup():
    logging.info("Iniciando a aplicação...")
    await init()  # Chama a criação das tabelas quando a aplicação iniciar

# Inclui o roteador de autenticação
def include_routers():
    logging.info("Incluindo rotas de autenticação...")
    app.include_router(auth.router)
include_routers()

# Define uma rota simples de teste
@app.get("/")
def read_root():
    """
    Endpoint inicial da aplicação.
    Retorna uma mensagem de boas-vindas para o usuário.
    """
    return {"message": "Bem-vindo ao Kubernetes RBAC Autentication."}
