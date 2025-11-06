from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routers import auth as auth_router
from app.routers import products as products_router
from app.routers import categories as categories_router
from app.routers import cart as cart_router
from app.routers import orders as orders_router
from app.routers import reviews as reviews_router
from app.routers import newsletter as newsletter_router
from app.routers import tips as tips_router
from app.routers import profile as profile_router


def get_cors_origins() -> list[str]:
    origins = os.getenv("CORS_ORIGINS", "").split(",")
    return [o.strip() for o in origins if o.strip()]


app = FastAPI(title="SoulNest API", openapi_url="/api/openapi.json", docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins() or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


# Routers
app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(categories_router.router)
app.include_router(cart_router.router)
app.include_router(orders_router.router)
app.include_router(reviews_router.router)
app.include_router(newsletter_router.router)
app.include_router(tips_router.router)
app.include_router(profile_router.router)

