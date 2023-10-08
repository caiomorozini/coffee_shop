from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.ingredient import Ingredient, IngredientResponse
from app.database.database import database, ingredients


ingredients_router = APIRouter(prefix="/ingredients")


@ingredients_router.post("/")
async def create_ingredient(
        ingredient: Ingredient = Body(
            ...,
            **Ingredient.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "name": "tomate",
                        "observations": "comprado no mercado",
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "name": "tomate",
                        "observations": "comprado no mercado",
                    },
                },
            }
        )) -> IngredientResponse:

    # Checando se ingredient já existe
    query = ingredients.select().where(
        (ingredients.c.name == ingredient.name)
    )
    ingredient_exists = await database.fetch_one(query)

    if ingredient_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingrediente já existe",
        )

    # Cria comando SQL para inserir o lote e executa
    query = ingredients.insert().values(
        **ingredient.model_dump(exclude_unset=True))
    last_record_id = await database.execute(query)

    return IngredientResponse(
        id=last_record_id, **ingredient.model_dump()
    )


@ingredients_router.get(
    "/",
    # tags=[Tags.items, Tags.users],
    summary="Mostra os ingredientes",
    response_description="A lista de ingredientes registrados",
    response_model=List[IngredientResponse],
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
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """

    query = ingredients.select().limit(limit)
    if recent is True:
        query = ingredients.select().order_by(
            ingredients.c.created_at.desc()).limit(limit)

    return await database.fetch_all(query)


@ingredients_router.put("/{ingredient_id}")
async def update_ingredient(
        ingredient_id: int = Path(..., title="ID do ingrediente"),
        ingredient: Ingredient = Body(
            ...,
            **Ingredient.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "name": "tomate",
                        "observations": "comprado no mercado",
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "name": "tomate",
                        "observations": "comprado no mercado",
                    },
                },
            }
        )) -> IngredientResponse:
    ingredient_exists = await database.fetch_one(
        ingredients.select().where(ingredients.c.id == ingredient_id)
    )
    if not ingredient_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não existe",
        )
    updated_id = await database.execute(
        ingredients.update().where(ingredients.c.id == ingredient_id).values(
            **ingredient.model_dump(exclude_unset=True))
    )

    return IngredientResponse(
        id=updated_id, **ingredient.model_dump()
    )

@ingredients_router.delete("/{ingredient_id}")
async def update_ingredient(
        ingredient_id: int = Path(..., title="ID do ingrediente"),
        ingredient: Ingredient = Body(
            ...,
            **Ingredient.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "name": "tomate",
                        "observations": "comprado no mercado",
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "name": "tomate",
                        "observations": "comprado no mercado",
                    },
                },
            }
        )) -> IngredientResponse:
    ingredient_exists = await database.fetch_one(
        ingredients.select().where(ingredients.c.id == ingredient_id)
    )
    if not ingredient_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não existe",
        )
    deleted_id = await database.execute(
        ingredients.delete().where(ingredients.c.id == ingredient_id
            ).values(**ingredient.model_dump(exclude_unset=True))
    )

    return IngredientResponse(
        id=deleted_id, **ingredient.model_dump()
    )



