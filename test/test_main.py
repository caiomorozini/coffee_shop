from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Cnfigurando o banco de dados de teste
# from app.database import metadata
# from app.config import DATABASE_URL
# from sqlalchemy import create_engine
# from sqlalchemy_utils import create_database, database_exists
# from app.database.database import database

# engine = create_engine(DATABASE_URL)
# if not database_exists(engine.url):
#     create_database(engine.url)
# metadata.create_all(engine)

# # Inserindo dados de teste
# from app.schemas.ingredient import Ingredient
# from app.database import ingredients
# from app.database import database

# async def create_sample_data():

#     query = ingredients.insert()
#     values = [
#         Ingredient(name="cafe").model_dump(),
#         Ingredient(name="chocolate").model_dump(),
#         Ingredient(name="agua").model_dump(),
#         Ingredient(name="leite").model_dump(),
#         Ingredient(name="acucar").model_dump(),
#     ]
#     await database.execute_many(query=query, values=values)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(create_sample_data())

# # Testes
# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}

def test_read_ingredients():
    with TestClient(app) as c:
        response = c.get("/api/v1/ingredients/?limit=5")

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "cafe",
            "observations": None,
            "id": 1
        },
        {
            "name": "chocolate",
            "observations": None,
            "id": 2
        },
        {
            "name": "agua",
            "observations": None,
            "id": 3
        },
        {
            "name": "leite",
            "observations": None,
            "id": 4
        },
        {
            "name": "acucar",
            "observations": None,
            "id": 5
        }
    ]

def test_get_one_ingredient():
    with TestClient(app) as c:
        response = c.get("/api/v1/ingredients/1")

    assert response.status_code == 200
    assert response.json() == {
        "name": "cafe",
        "observations": None,
        "id": 1
    }

def test_get_one_ingredient_not_found():
    with TestClient(app) as c:
        response = c.get("/api/v1/ingredients/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ingrediente não encontrado"
    }

def test_create_new_ingredient():
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/ingredients/",
            json={
                "name": "test_ingredient4",
                "observations": "test"
            }
        )

    assert response.status_code == 200
    assert response.json() == {
        "name": "test_ingredient4",
        "observations": "test",
        "id": response.json()["id"]
    }

    # Deletando o ingrediente criado
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/ingredients/{response.json()['id']}")

def test_create_new_ingredient_already_exists():
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/ingredients/",
            json={
                "name": "test_ingredient_already_exists",
                "observations": "test"
            }
        )

    assert response.status_code == 200
    assert response.json() == {
        "name": "test_ingredient_already_exists",
        "observations": "test",
        "id": response.json()["id"]
    }

    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/ingredients/",
            json={
                "name": "test_ingredient_already_exists",
                "observations": "test"
            }
        )

    assert invalid_response.status_code == 400
    assert invalid_response.json() == {
        "detail": "Ingrediente já existe"
    }

    with TestClient(app) as c:
        response = c.delete(f"/api/v1/ingredients/{response.json()['id']}")


def test_delete_ingredient():
    # Criando o ingrediente
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/ingredients/",
            json={
                "name": "test_ingredient_delete",
                "observations": "test"
            }
        )

    # Deletando o ingrediente criado
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/ingredients/{response.json()['id']}")

    assert response.status_code == 204
