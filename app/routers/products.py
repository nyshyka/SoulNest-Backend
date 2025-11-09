from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
import logging

from app.db.session import get_db
from app.models import Product, Category, ProductImage, ProductHowToUse, ProductGuarantee
from app.schemas import ProductPublic

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=List[ProductPublic])
async def list_products(
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    bestseller: Optional[bool] = Query(None),
):
    try:
        stmt = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.how_to_use),
            selectinload(Product.guarantees)
        )
        conditions = []
        if search:
            like = f"%{search}%"
            # MySQL LIKE is case-insensitive with utf8mb4_unicode_ci collation
            conditions.append(
                or_(
                    Product.title.like(like),
                    Product.description.like(like),
                    Product.tagline.like(like)
                )
            )
        if category:
            sub = select(Category.id).where(Category.slug == category)
            conditions.append(Product.category_id.in_(sub))
        if featured is True:
            conditions.append(Product.is_featured.is_(True))
        if bestseller is True:
            conditions.append(Product.is_bestseller.is_(True))
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(Product.created_at.desc())
        res = await db.execute(stmt)
        products = res.scalars().unique().all()
        return products
    except Exception as e:
        logger.error(f"Error in list_products: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/featured", response_model=List[ProductPublic])
async def featured_products(db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.how_to_use),
            selectinload(Product.guarantees)
        ).where(Product.is_featured.is_(True)).order_by(Product.created_at.desc())
        res = await db.execute(stmt)
        return res.scalars().unique().all()
    except Exception as e:
        logger.error(f"Error in featured_products: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/bestsellers", response_model=List[ProductPublic])
async def bestseller_products(db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.how_to_use),
            selectinload(Product.guarantees)
        ).where(Product.is_bestseller.is_(True)).order_by(Product.created_at.desc())
        res = await db.execute(stmt)
        return res.scalars().unique().all()
    except Exception as e:
        logger.error(f"Error in bestseller_products: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/search", response_model=List[ProductPublic])
async def search_products(q: str, db: AsyncSession = Depends(get_db)):
    try:
        like = f"%{q}%"
        stmt = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.how_to_use),
            selectinload(Product.guarantees)
        ).where(
            or_(
                Product.title.like(like),
                Product.description.like(like),
                Product.tagline.like(like)
            )
        )
        res = await db.execute(stmt)
        return res.scalars().unique().all()
    except Exception as e:
        logger.error(f"Error in search_products: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{id}", response_model=ProductPublic)
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.how_to_use),
            selectinload(Product.guarantees)
        ).where(Product.id == id)
        res = await db.execute(stmt)
        product = res.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_product: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{id}/related", response_model=List[ProductPublic])
async def related_products(id: int, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.how_to_use),
            selectinload(Product.guarantees)
        ).where(Product.id == id)
        res = await db.execute(stmt)
        current = res.scalar_one_or_none()
        if not current:
            raise HTTPException(status_code=404, detail="Product not found")
        if current.category_id is None:
            return []
        rel_stmt = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.how_to_use),
            selectinload(Product.guarantees)
        ).where(
            Product.category_id == current.category_id, 
            Product.id != current.id
        ).order_by(Product.created_at.desc()).limit(6)
        rel = await db.execute(rel_stmt)
        return rel.scalars().unique().all()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in related_products: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


