from pydantic import BaseModel
from typing import Optional, List
from model.madeira import Madeira


from pydantic import BaseModel, Field

class MadeiraSchema(BaseModel):
    madeira: str = Field(..., description="Nome da madeira")
    volume: float = Field(..., description="Volume da madeira")
    produto: str = Field(..., description="Tipo de produto feito com a madeira")
    origem: str = Field(..., description="Origem da madeira")

class MadeiraViewSchema(BaseModel):
    id: int = Field(..., description="ID da madeira")
    madeira: str = Field(..., description="Nome da madeira")
    volume: float = Field(..., description="Volume da madeira")
    produto: str = Field(..., description="Tipo de produto feito com a madeira")
    origem: str = Field(..., description="Origem da madeira")

class ListagemMadeirasSchema(BaseModel):
    madeiras: list[MadeiraViewSchema] = Field(..., description="Lista de madeiras cadastradas")

class MadeiraBuscaSchema(BaseModel):
    nome: str = Field(..., description="Nome da madeira para buscar")

class MadeiraDelSchema(BaseModel):
    message: str = Field(..., description="Mensagem de status da deleção")
    nome: str = Field(..., description="Nome da madeira deletada")

class ErrorSchema(BaseModel):
    message: str = Field(..., description="Mensagem de erro")
