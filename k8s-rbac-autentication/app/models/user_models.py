from sqlalchemy import Column, Integer, String # type: ignore
from app.models.base import Base

class User(Base):
    """
    Modelo de Usuário representando a tabela 'users' no banco de dados.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
