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
from schemas import Coffee, Imagem, Tags, ResponseCoffee
from database import dados


route = APIRouter()

@route.post("/coffees/")
async def create_coffee(
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

    dados.append(coffee.model_dump())

    return ResponseCoffee(
        id=len(dados),
        **coffee.model_dump(),
    )


@route.get(
    "/items/",
    tags=[Tags.items, Tags.users],
    summary="Mostra os items",
    response_description="A lista de items",
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

@route.get("/items/{item_id}", tags=["items", "produtos", "cafe"])
async def mostrar_item(
    item_id: int = Path(title="The ID of the item to get"),
    user_agent: str = Header(None, convert_underscores=True),
):
    if item_id > len(dados):
        raise HTTPException(status_code=404, detail="Produto não existe")
    return dados[item_id - 1]

@route.get("/portal", status_code=status.HTTP_201_CREATED)
async def get_portal(teleport: bool = False) -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/")

@route.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


@route.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@route.post("/uploadfile/")
async def create_upload_file(file: list[UploadFile]):
    return {"filename": file.filename}


@route.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)