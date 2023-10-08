#pylint: disable=E0213

import re
from pydantic import BaseModel, confloat, constr, Field, HttpUrl, validator
from datetime import datetime
from unidecode import unidecode

class OutputIngredient(BaseModel):
    """ Modelo de ingrediente """
    quantity: int = Field(0, example=5)
    date: datetime = Field(exemple="15/12/2023")


class OutputIngredientResponse(OutputIngredient):
    """ Modelo de resposta de ingrediente """
    id: int
