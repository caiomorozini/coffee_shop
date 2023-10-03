#pylint: disable=E0213

from pydantic import BaseModel, confloat, constr, Field, HttpUrl, validator
from datetime import datetime
from typing import Union, List, Annotated


class Batch(BaseModel):
    """ Modelo de lote """
    purchase: datetime
    expiration: datetime
    manufacturing: datetime

    @validator("purchase", "expiration", "manufacturing", pre=True)
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

    @validator("purchase", "manufacturing")
    def purchase_and_manufacturing_must_be_before_today(cls, v):
        """ Verifica se a data é anterior a hoje """
        if v is not None:
            if v > datetime.now():
                raise ValueError(f"Data {v} é posterior a hoje")
            if v < datetime(year=2000, month=1, day=1):
                raise ValueError(f"Data {v} é anterior a data mínima permitida")
        return v

    @validator("expiration")
    def expiration_must_be_after_purchase(cls, v, values, **kwargs):
        """ Verifica se a data é posterior a data de compra """
        if not values.get("purchase"):
            raise ValueError("Data de compra não foi informada")
        if v is not None:
            if v < values["purchase"]:
                raise ValueError("Data de expiração é anterior a data de compra")
        return v

class BatchResponse(Batch):
    """ Modelo de resposta de lote """
    id: int
