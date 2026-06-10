from fastapi import FastAPI

from app.database.connection import Base, engine
from app.routes.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    version="3.0.0"
)

app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "API funcionando"
    }