from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.session import get_db
from app.models import Product, Category, ProductImage, ProductHowToUse, ProductGuarantee
from app.schemas import ProductPublic


router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=List[ProductPublic])
async def list_products(
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    bestseller: Optional[bool] = Query(None),
):
    stmt = select(Product)
    conditions = []
    if search:
        like = f"%{search.lower()}%"
        conditions.append(
            (Product.title.ilike(like))
            | (Product.description.ilike(like))
            | (Product.tagline.ilike(like))
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


@router.get("/featured", response_model=List[ProductPublic])
async def featured_products(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Product).where(Product.is_featured.is_(True)).order_by(Product.created_at.desc()))
    return res.scalars().all()


@router.get("/bestsellers", response_model=List[ProductPublic])
async def bestseller_products(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Product).where(Product.is_bestseller.is_(True)).order_by(Product.created_at.desc()))
    return res.scalars().all()


@router.get("/search", response_model=List[ProductPublic])
async def search_products(q: str, db: AsyncSession = Depends(get_db)):
    like = f"%{q.lower()}%"
    res = await db.execute(
        select(Product).where(
            (Product.title.ilike(like)) | (Product.description.ilike(like)) | (Product.tagline.ilike(like))
        )
    )
    return res.scalars().all()


@router.get("/{id}", response_model=ProductPublic)
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Product).where(Product.id == id))
    product = res.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/{id}/related", response_model=List[ProductPublic])
async def related_products(id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Product).where(Product.id == id))
    current = res.scalar_one_or_none()
    if not current:
        raise HTTPException(status_code=404, detail="Product not found")
    if current.category_id is None:
        return []
    rel = await db.execute(
        select(Product)
        .where(Product.category_id == current.category_id, Product.id != current.id)
        .order_by(Product.created_at.desc())
        .limit(6)
    )
    return rel.scalars().all()


