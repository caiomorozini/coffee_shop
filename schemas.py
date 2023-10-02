
from pydantic import BaseModel, confloat, constr, Field, HttpUrl
from typing import Union, List, Annotated
from enum import Enum

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


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


class Tags(Enum):
    items = "items"
    users = "users"


class ResponseCoffee(Coffee):
    id: int
