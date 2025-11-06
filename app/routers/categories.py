from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models import Category, Product, RitualGuide
from app.schemas import CategoryPublic, ProductPublic, RitualGuidePublic


router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=List[CategoryPublic])
async def list_categories(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Category).order_by(Category.title.asc()))
    return res.scalars().all()


@router.get("/{slug}")
async def get_category(slug: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Category).where(Category.slug == slug))
    cat = res.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    products_res = await db.execute(select(Product).where(Product.category_id == cat.id))
    guides_res = await db.execute(
        select(RitualGuide).where(RitualGuide.category_id == cat.id).order_by(RitualGuide.step_number.asc())
    )
    return {
        "category": CategoryPublic.model_validate(cat),
        "products": [ProductPublic.model_validate(p) for p in products_res.scalars().all()],
        "guide": [RitualGuidePublic.model_validate(g) for g in guides_res.scalars().all()],
    }

