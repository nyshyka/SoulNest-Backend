from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.session import get_db
from app.models import Review, Product, User
from app.schemas import ReviewCreate, ReviewPublic
from .deps import get_current_user


router = APIRouter(prefix="/api", tags=["reviews"])


@router.get("/products/{id}/reviews", response_model=List[ReviewPublic])
async def list_reviews(id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Review).where(Review.product_id == id).order_by(Review.created_at.desc()))
    return res.scalars().all()


@router.post("/products/{id}/reviews", response_model=ReviewPublic, status_code=201)
async def create_review(id: int, payload: ReviewCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    prod = await db.execute(select(Product).where(Product.id == id))
    if not prod.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")
    existing = await db.execute(select(Review).where(Review.user_id == current_user.id, Review.product_id == id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already reviewed")
    review = Review(product_id=id, user_id=current_user.id, rating=payload.rating, comment=payload.comment)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


@router.put("/reviews/{id}", response_model=ReviewPublic)
async def update_review(id: int, payload: ReviewCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Review).where(Review.id == id, Review.user_id == current_user.id))
    review = res.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review.rating = payload.rating
    review.comment = payload.comment
    await db.commit()
    await db.refresh(review)
    return review


@router.delete("/reviews/{id}", status_code=204)
async def delete_review(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Review).where(Review.id == id, Review.user_id == current_user.id))
    review = res.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    await db.execute(delete(Review).where(Review.id == id))
    await db.commit()
    return None


