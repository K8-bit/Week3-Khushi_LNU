from fastapi import FastAPI

from product import models
from product.db.base import Base
from product.db.session import engine
from product.routers.cart_router import router as cart_router
from product.routers.category_router import router as category_router
from product.routers.order_router import router as order_router
from product.routers.product_router import router as product_router
from product.routers.user_router import router as user_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Online Shopping API",
    version="1.0.0",
)


app.include_router(
    user_router,
    prefix="/api",
)

app.include_router(
    category_router,
    prefix="/api",
)

app.include_router(
    product_router,
    prefix="/api",
)

app.include_router(
    cart_router,
    prefix="/api",
)

app.include_router(
    order_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "message": "Online Shopping API is running",
    }
