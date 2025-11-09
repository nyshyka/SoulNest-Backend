from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from app.routers import auth as auth_router
from app.routers import products as products_router
from app.routers import categories as categories_router
from app.routers import cart as cart_router
from app.routers import orders as orders_router
from app.routers import enhanced_orders as enhanced_orders_router
from app.routers import reviews as reviews_router
from app.routers import enhanced_reviews as enhanced_reviews_router
from app.routers import newsletter as newsletter_router
from app.routers import tips as tips_router
from app.routers import profile as profile_router
from app.routers import custom_rituals as custom_rituals_router
from app.routers import multiple_wishlists as multiple_wishlists_router
from app.routers import subscriptions as subscriptions_router
from app.routers import social_sharing as social_sharing_router
from app.routers import for_you as for_you_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to catch unhandled errors"""
    from fastapi import HTTPException
    # Don't catch HTTPExceptions - let them through
    if isinstance(exc, HTTPException):
        raise exc
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


# Routers
app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(categories_router.router)
app.include_router(cart_router.router)
app.include_router(orders_router.router)
app.include_router(enhanced_orders_router.router)  # Enhanced orders (overrides some endpoints)
app.include_router(reviews_router.router)
app.include_router(enhanced_reviews_router.router)  # Enhanced reviews (overrides some endpoints)
app.include_router(newsletter_router.router)
app.include_router(tips_router.router)
app.include_router(profile_router.router)
app.include_router(custom_rituals_router.router)
app.include_router(multiple_wishlists_router.router)
app.include_router(subscriptions_router.router)
app.include_router(social_sharing_router.router)
app.include_router(for_you_router.router)

