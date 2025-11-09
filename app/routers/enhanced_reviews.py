"""Enhanced Reviews endpoints"""
import base64
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models import Review, Product, User
from app.models.new_models import ReviewPhoto, ReviewHelpfulVote
from app.models import User as UserModel
from app.schemas.new_schemas import ReviewCreateEnhanced, ReviewPublicEnhanced, ReviewHelpfulResponse
from .deps import get_current_user


router = APIRouter(prefix="/api", tags=["reviews"])


@router.post("/products/{product_id}/reviews", response_model=ReviewPublicEnhanced, status_code=201)
async def submit_review(
    product_id: int,
    payload: ReviewCreateEnhanced,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit review with optional photos"""
    # Check if product exists
    prod = await db.execute(select(Product).where(Product.id == product_id))
    if not prod.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if user already reviewed
    existing = await db.execute(
        select(Review).where(Review.user_id == current_user.id, Review.product_id == product_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already reviewed this product")

    # Create review
    review = Review(
        product_id=product_id,
        user_id=current_user.id,
        rating=payload.rating,
        comment=payload.comment,
        helpful_count=0
    )
    db.add(review)
    await db.flush()

    # Handle photos (base64 to URL - in production, upload to S3/cloud storage)
    if payload.photos:
        for idx, photo_base64 in enumerate(payload.photos):
            # In production, upload to storage and get URL
            # For now, save as placeholder
            photo_url = f"https://picsum.photos/seed/review_{review.id}_{idx}/400/400"
            photo = ReviewPhoto(
                review_id=review.id,
                image_url=photo_url,
                display_order=idx
            )
            db.add(photo)

    await db.commit()
    await db.refresh(review)
    
    # Load photos for response
    photos_res = await db.execute(select(ReviewPhoto).where(ReviewPhoto.review_id == review.id))
    review.photos = photos_res.scalars().all()
    
    # Get user name
    user_res = await db.execute(select(UserModel).where(UserModel.id == review.user_id))
    user = user_res.scalar_one_or_none()
    review.user_name = user.name if user else None
    
    return review


@router.get("/products/{product_id}/reviews", response_model=List[ReviewPublicEnhanced])
async def get_product_reviews(
    product_id: int,
    rating: Optional[int] = Query(None),
    with_photos: Optional[bool] = Query(None),
    sort: Optional[str] = Query("recent"),  # recent, helpful, rating
    limit: Optional[int] = Query(10),
    offset: Optional[int] = Query(0),
    db: AsyncSession = Depends(get_db)
):
    """Get product reviews with filters"""
    # Note: Review model doesn't have photos relationship yet, need to query separately
    stmt = select(Review).where(Review.product_id == product_id)

    if rating:
        stmt = stmt.where(Review.rating == rating)

    # Apply sorting
    if sort == "helpful":
        stmt = stmt.order_by(Review.helpful_count.desc(), Review.created_at.desc())
    elif sort == "rating":
        stmt = stmt.order_by(Review.rating.desc(), Review.created_at.desc())
    else:  # recent
        stmt = stmt.order_by(Review.created_at.desc())

    stmt = stmt.limit(limit).offset(offset)
    res = await db.execute(stmt)
    reviews = res.scalars().all()

    # Load photos and user names for each review
    for review in reviews:
        photos_res = await db.execute(select(ReviewPhoto).where(ReviewPhoto.review_id == review.id))
        review.photos = photos_res.scalars().all()
        user_res = await db.execute(select(UserModel).where(UserModel.id == review.user_id))
        user = user_res.scalar_one_or_none()
        review.user_name = user.name if user else None

    # Filter by photos if needed
    if with_photos:
        reviews = [r for r in reviews if len(r.photos) > 0]

    return reviews


@router.post("/reviews/{review_id}/helpful", response_model=ReviewHelpfulResponse)
async def mark_review_helpful(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark review as helpful"""
    res = await db.execute(select(Review).where(Review.id == review_id))
    review = res.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Check if already voted
    vote_res = await db.execute(
        select(ReviewHelpfulVote).where(
            ReviewHelpfulVote.review_id == review_id,
            ReviewHelpfulVote.user_id == current_user.id
        )
    )
    existing_vote = vote_res.scalar_one_or_none()

    if existing_vote:
        # Remove vote
        await db.delete(existing_vote)
        review.helpful_count = max(0, review.helpful_count - 1)
        user_has_voted = False
    else:
        # Add vote
        vote = ReviewHelpfulVote(review_id=review_id, user_id=current_user.id)
        db.add(vote)
        review.helpful_count += 1
        user_has_voted = True

    await db.commit()
    await db.refresh(review)
    return {
        "review_id": review_id,
        "helpful_count": review.helpful_count,
        "user_has_voted": user_has_voted
    }

