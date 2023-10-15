#pylint: disable=E0213

import re
from pydantic import BaseModel, confloat, constr, Field, HttpUrl, validator
from datetime import datetime
from unidecode import unidecode

class OutputIngredient(BaseModel):
    """ Modelo de ingrediente """
    id_ingredient: int
    quantity: int = Field(0, example=5)
    date: datetime = Field(exemple="15/12/2023")

    @validator("date", pre=True)
    def format_date(cls, v):
        """ Formata a data para datetime """

        if isinstance(v, str):
            try:
                v = datetime.strptime(v, "%d/%m/%Y")
            except ValueError:
                try:
                    v = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
                except ValueError as value_error:
                    raise ValueError(
                        f"Data {v} não está no formato dd/mm/yyyy") \
                        from value_error
        return v

class OutputIngredientResponse(OutputIngredient):
    """ Modelo de resposta de ingrediente """
    id: int
