from fastapi import FastAPI
from endpoints import route

app = FastAPI(
    summary="API de exemplo",
    title="API de exemplo2",
    description="Descrição da API de exemplo",
)

app.include_router(route, prefix="/v1", tags=["v1"])

@app.on_event("startup")
async def startup_event():
    print("Iniciando a API")

@app.on_event("shutdown")
async def shutdown_event():
    print("Finalizando a API")