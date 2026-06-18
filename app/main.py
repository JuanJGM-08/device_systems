from fastapi import FastAPI

from app.database.connection import Base, engine
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    version="3.0.0"
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/")
def root():
    return {
        "message": "API funcionando",
        "endpoints": {
            "users": "/users",
            "devices": "/devices",
            "loans": "/loans"
        }
    }