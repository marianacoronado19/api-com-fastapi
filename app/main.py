from fastapi import FastAPI
from routes.routes import router

app = FastAPI(
    title="Must Watch API",
    description="API para gerenciar séries, categorias, atores e avaliações.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Séries",
            "description": "Operações relacionadas a séries, categorias, atores e avaliações."
        }
    ]
)

app.router.include_router(router)