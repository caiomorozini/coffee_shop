
from pydantic import BaseModel, confloat, constr, Field, HttpUrl
from typing import Union, List, Annotated
from enum import Enum


class Imagem(BaseModel):
    name: constr(
        to_lower=True,
        strip_whitespace=True,
        min_length=1,
        max_length=50,
        pattern="^[a-z0-9_\-]+$"
    ) = "foto_cafe"
    url: HttpUrl


class Coffee(BaseModel):
    nome: str = "expresso"
    preco: float = Field(
        float,
        gt=0,
        le=100.0,
        description="O preco deve ser maior que zero e menor que 100.0",
        example=14.0,
    )
    descricao: Union[str, None] = None
    tamanho: constr(
        to_lower=True,
        strip_whitespace=True,
        min_length=1,
        max_length=1,
        pattern="^[p|m|g]$"
    ) = "p"
    imagens: List[Imagem]

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "nome": "nome do cafe",
                    "preco": 76.0,
                    "descricao": "Exemplo de descrição",
                    "tamanho": "p",
                    "imagens": [
                        {
                            "name": "nome da imagem",
                            "url": "https://www.example.com.br"
                        }
                    ]
                }
            ]
        }
    }


class Tags(Enum):
    items = "items"
    users = "users"


class ResponseCoffee(Coffee):
    id: int
