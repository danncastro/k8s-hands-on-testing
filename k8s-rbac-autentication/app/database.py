from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from sqlalchemy import inspect # type: ignore
from app.config import DATABASE_URL
from app.models.base import Base
import logging

# Configura o log para rastrear os eventos
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criando o motor do banco de dados
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Criando a fábrica de sessões
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Testando a conexão com o banco
async def test_connection():
    try:
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            logger.info(f"Conexão bem-sucedida. Resultado da consulta: {result.scalar()}")
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")

async def create_tables_sync():
    try:
        # Verifica os modelos registrados
        logger.info(f"Modelos registrados para criação: {list(Base.metadata.tables.keys())}")

        # Cria as tabelas
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Tabelas criadas com sucesso!")

        # Verifica tabelas existentes
        async with engine.connect() as conn:
            existing_tables = await conn.run_sync(lambda c: inspect(c).get_table_names())
            logger.info(f"Tabelas existentes no banco de dados: {existing_tables}")
    except Exception as e:
        logger.error("Erro ao criar tabelas: ", exc_info=True)

# Dependência do banco de dados
async def get_db():
    async with async_session_factory() as session:
        yield session
