from fastapi import (
    Query,
    Path, Body, Header, Response, status, Form, File,
    UploadFile, HTTPException,
    APIRouter
)
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel, confloat, constr, Field, HttpUrl
from typing import Union, List, Annotated
from enum import Enum
from schemas import Coffee, Tags, ResponseCoffee


dados = []

route = APIRouter()

@route.post("/")
async def create_item(
    coffee: Coffee = Body(
        ...,
        **Coffee.model_config,
        openapi_examples={
            "normal": {
                "summary": "Um exemplo normal",
                "description": "Um exemplo normal",
                "value": {
                    "nome": "nome do cafe",
                    "preco": 76.0,
                    "descricao": "Exemplo de descrição",
                    "tamanho": "p",
                    "imagens": [
                        {
                            "name": "nome_da_imagem",
                            "url": "https://www.example.com.br"
                        }
                    ]
                }
            },
            "invalid": {
                "summary": "Um exemplo inválido",
                "description": "Um exemplo inválido",
                "value": {
                    "nome": "nome do cafe",
                    "preco": 76.0,
                    "descricao": "Exemplo de descrição",
                    "tamanho": "pequeno",
                    "imagens": [
                        {
                            "name": "nome da imagem",
                            "url": "https://www.example.com.br"
                        }
                    ]
                }
            }
        }
    )) -> ResponseCoffee:

    insert_coffee = coffee.model_dump()
    insert_coffee["id"] = len(dados) + 1
    dados.append(insert_coffee)

    return ResponseCoffee(
        id=len(dados),
        **coffee.model_dump(),
    )


@route.get(
    "/coffee/",
    tags=[Tags.items, Tags.users],
    summary="Mostra os cafés registrados",
    response_description="A lista de cafés registrados",
    response_model=List[ResponseCoffee],
)
async def mostrar_items(
    query: list = Query(
        default_factory=list,
        title="Query string",
        description="Query string para filtrar os items",
        alias="abc",
        ),
    limit: int = Query(default=10, ge=1, le=50, deprecated=True),
    menor_preco: bool = False
):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    if menor_preco is True:
        dados.sort(key=lambda x: x["preco"])
    return [ResponseCoffee(
        **dado
    ) for dado in dados[:limit]]

@route.get("/items/{item_id}")
async def mostrar_item(
    item_id: int = Path(title="The ID of the item to get"),
    user_agent: str = Header(None, convert_underscores=True),
):
    if item_id > len(dados):
        raise HTTPException(status_code=404, detail="Produto não existe")
    return dados[item_id - 1]
