#pylint: disable=E0213

import re
from pydantic import BaseModel, confloat, constr, Field, HttpUrl, validator
from datetime import datetime
from typing import Union, List, Annotated, Optional
from unidecode import unidecode

class Product(BaseModel):
    """ Modelo de ingrediente """
    name: constr(
        max_length=50,
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        ) = Field(..., example="café com leite")
    price: float = Field(example=2.59)
    descript: Optional[constr(
        max_length=2000,
        strip_whitespace=True,
        min_length=1,
     )] = Field(None, example="Com o café passado, acrescentar 100ml de leite")

    @validator("name")
    def apply_unidecode(cls, v):
        """ Aplica unidecode no nome """
        return re.sub(r'[^\w\s]', '', unidecode(v))

class ProductResponse(Product):
    """ Modelo de resposta de ingrediente """
    id: int
