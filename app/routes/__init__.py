from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

__all__ = ["user_router", "device_router", "loan_router"]