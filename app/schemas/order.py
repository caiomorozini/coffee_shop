#pylint: disable=E0213

import re
from pydantic import BaseModel, confloat, constr, Field, HttpUrl, validator
from datetime import datetime
from typing import Union, List, Annotated, Optional
from unidecode import unidecode

class Order(BaseModel):
    """ Modelo de ingrediente """
    products: List[Optional[int]] # Lista com ids na tabela de produtos
    price: float = Field(example=2.59)
    observations: Optional[constr(
        max_length=500,
        strip_whitespace=True,
        min_length=1,
     )] = Field(None, example="Não colocar canela no capuccino")


class OrderResponse(Order):
    """ Modelo de resposta de ingrediente """
    id: int
