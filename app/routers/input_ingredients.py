from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.input_ingredients import InputIngredient, InputIngredientResponse
from app.database.database import database, input_table


input_ingredients_router = APIRouter(prefix="/input-ingredients")


@input_ingredients_router.post("/")
async def create(
        ingredient: InputIngredient = Body(
            ...,
            **InputIngredient.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "name": "farinha de trigo",
                        "quantity": 1,
                        "unit_price": 3.86,
                        "date": "09/10/2023"
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "name": "maracuja",
                        "quantity": "abc",
                        "unit_price": 1.0,
                        "date": "02/08/2023"
                    }
                },
            }
        )) -> InputIngredientResponse:

    # Cria comando SQL para inserir o lote e executa
    query = input_table.insert().values(
        **ingredient.model_dump(exclude_unset=True))
    last_record_id = await database.execute(query)

    return InputIngredientResponse(
        id=last_record_id, **ingredient.model_dump()
    )

@input_ingredients_router.get(
    "/",
    # tags=[Tags.items, Tags.users],
    summary="Mostra os ingredientes",
    response_description="A lista de ingredientes registrados",
    response_model=List[InputIngredientResponse],
)
async def mostrar_items(
    query: list = Query(
        default_factory=list,
        title="Query string",
        description="Query string para filtrar os items",
        alias="abc",
    ),
    limit: int = Query(default=10, ge=1, le=50),
    recent: bool = False
):
    """
    Returns:
        Retorna ingredientes comprados
    """

    query = input_table.select().limit(limit)
    if recent is True:
        query = input_table.select().order_by(
            input_table.c.created_at.desc()).limit(limit)

    return await database.fetch_all(query)

@input_ingredients_router.put("/{ingredient_id}")
async def update_ingredient(
        id: int = Path(..., title="ID do ingrediente"),
        ingredient: InputIngredient = Body(
            ...,
            **InputIngredient.model_config
        )) -> InputIngredientResponse:
    ingredient_exists = await database.fetch_one(
        input_table.select().where(input_table.c.id == id)
    )
    if not ingredient_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não existe",
        )
    updated_id = await database.execute(
        input_table.update().where(input_table.c.id == id).values(
            **ingredient.model_dump(exclude_unset=True))
    )

    return InputIngredientResponse(
        id=updated_id, **ingredient.model_dump()
    )

@input_ingredients_router.delete("/{id}")
async def update_ingredient(
        id: int = Path(..., title="ID do ingrediente"),
        ingredient: InputIngredient = Body(
            ...,
            **InputIngredient.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "name": "tomate",
                        "quantity": 4,
                        "unit_price": 0.6,
                        "date": "08/10/2023",
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "name": "tomate",
                        "quantity": "quatro",
                        "unit_price": 0.6,
                        "date": "08/10/2023",
                    }
                },
            }
        )) -> InputIngredientResponse:

    ingredient_exists = await database.fetch_one(
        input_table.select().where(
            input_table.c.id == id)
    )
    if not ingredient_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não existe",
        )
    deleted_id = await database.execute(
        input_table.delete().where(
            input_table.c.id == id).values(
                **ingredient.model_dump(exclude_unset=True))
    )

    return InputIngredientResponse(
        id=deleted_id, **ingredient.model_dump()
    )
