#pylint: disable=E0213

import re
from pydantic import BaseModel, confloat, constr, Field, HttpUrl, validator
from datetime import datetime
from typing import Union, List, Annotated, Optional
from unidecode import unidecode

class InputIngredient(BaseModel):
    """ Modelo de ingrediente """
    name: constr(
        max_length=50,
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        ) = Field(..., example="tomate")
    quantity: int = Field(0, example=5)
    unit_price: float = Field(example=2.98)
    date: datetime = Field(exemple="15/12/2023")

    @validator("name")
    def apply_unidecode(cls, v):
        """ Aplica unidecode no nome """
        return re.sub(r'[^\w\s]', '', unidecode(v))

class InputIngredientResponse(InputIngredient):
    """ Modelo de resposta de ingrediente """
    id: int