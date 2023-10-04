#pylint: disable=E0213

from pydantic import BaseModel, confloat, constr, Field, HttpUrl, validator
from datetime import datetime
from typing import Union, List, Annotated, Optional


class Ingredient(BaseModel):
    """ Modelo de ingrediente """
    name: constr(
        max_length=50,
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        ) = Field(..., example="tomate")
    quantity: confloat(gt=0) = Field(..., example=1)
    observations: constr(
        max_length=500,
        strip_whitespace=True,
        min_length=1,
        ) = Optional[Field(..., example="tomate")]

class IngredientResponse(Ingredient):
    """ Modelo de resposta de ingrediente """
    id: int
