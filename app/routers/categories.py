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
    try:
        res = await db.execute(select(Category).where(Category.slug == slug))
        cat = res.scalar_one_or_none()
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Get products with their relationships loaded
        from sqlalchemy.orm import selectinload
        products_res = await db.execute(
            select(Product)
            .where(Product.category_id == cat.id)
            .options(
                selectinload(Product.images),
                selectinload(Product.how_to_use),
                selectinload(Product.guarantees)
            )
        )
        products = products_res.scalars().all()
        
        # Get ritual guides
        guides_res = await db.execute(
            select(RitualGuide)
            .where(RitualGuide.category_id == cat.id)
            .order_by(RitualGuide.step_number.asc())
        )
        guides = guides_res.scalars().all()
        
        return {
            "category": CategoryPublic.model_validate(cat),
            "products": [ProductPublic.model_validate(p) for p in products],
            "guide": [RitualGuidePublic.model_validate(g) for g in guides],
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

