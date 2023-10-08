#pylint: disable=E0213

from pydantic import BaseModel, confloat, constr, Field, HttpUrl, validator
from datetime import datetime
from typing import Union, List, Annotated


class Batch(BaseModel):
    """ Modelo de lote """
    expiration: datetime
    quantity: int

    @validator("expiration", pre=True)
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

class BatchResponse(Batch):
    """ Modelo de resposta de lote """
    id: int
