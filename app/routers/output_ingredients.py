from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.output_ingredient import OutputIngredient, OutputIngredientResponse
from app.database.database import database, output_table


output_ingredients_router = \
    APIRouter(prefix="/output-ingredients")


@output_ingredients_router.post("/")
async def create_ingredient(
        ingredient: OutputIngredient = Body(
            ...,
            **OutputIngredient.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        # "name": "tomate",
                        "quantity": 4,
                        "date": 15/12/2023,
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        # "name": "tomate",
                        "quantity": "quatro",
                        "date": 15/12/2023,
                    },
                },
            }
        )) -> OutputIngredientResponse:
    pass