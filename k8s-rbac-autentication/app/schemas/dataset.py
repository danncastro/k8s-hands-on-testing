from pydantic import BaseModel, Field # type: ignore

class UserBase(BaseModel):
    """
    Esquema base para representar dados de usuários.
    """
    username: str = Field(..., min_length=3, max_length=40, description="Nome do usuário único")

class UserCreate(UserBase):
    """
    Esquema para criar um novo usuário.
    """
    password: str = Field(..., min_length=6, description="Senha do usuário (mínimo 6 caracteres).")

class UserResponse(UserBase):
    """
    Esquema para responder dados de um usuário.
    """
    id: int = Field(..., description="Identificador único do usuário.")
    class config:
        orm_mode = True
