"""Custom Rituals endpoints"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.new_models import CustomRitual, RitualStep, RitualShare
from app.models import Product, User
from app.schemas.new_schemas import (
    CustomRitualCreate, CustomRitualPublic, RitualStepCreate, RitualShareCreate, RitualSharePublic
)
from .deps import get_current_user


router = APIRouter(prefix="/api/rituals", tags=["rituals"])


@router.post("/custom", response_model=CustomRitualPublic, status_code=201)
async def save_custom_ritual(
    payload: CustomRitualCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save a custom ritual"""
    # Calculate bundle price
    bundle_price = 0.0
    for step in payload.steps:
        if step.product_id:
            prod = await db.execute(select(Product).where(Product.id == step.product_id))
            product = prod.scalar_one_or_none()
            if product:
                bundle_price += float(product.price)

    savings = round(bundle_price * 0.10, 2) if bundle_price > 0 else 0.0

    ritual = CustomRitual(
        user_id=current_user.id,
        name=payload.name,
        bundle_price=round(bundle_price, 2),
        savings=savings
    )
    db.add(ritual)
    await db.flush()

    for step_data in payload.steps:
        step = RitualStep(
            ritual_id=ritual.id,
            step_number=step_data.step_number,
            title=step_data.title,
            product_id=step_data.product_id
        )
        db.add(step)

    await db.commit()
    await db.refresh(ritual)
    return ritual


@router.get("/custom", response_model=List[CustomRitualPublic])
async def get_saved_rituals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all saved rituals for user"""
    stmt = select(CustomRitual).options(
        selectinload(CustomRitual.steps)
    ).where(CustomRitual.user_id == current_user.id).order_by(CustomRitual.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/custom/{ritual_id}", response_model=CustomRitualPublic)
async def get_ritual_details(
    ritual_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get ritual details"""
    stmt = select(CustomRitual).options(
        selectinload(CustomRitual.steps)
    ).where(CustomRitual.id == ritual_id, CustomRitual.user_id == current_user.id)
    res = await db.execute(stmt)
    ritual = res.scalar_one_or_none()
    if not ritual:
        raise HTTPException(status_code=404, detail="Ritual not found")
    return ritual


@router.delete("/custom/{ritual_id}", status_code=204)
async def delete_ritual(
    ritual_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a custom ritual"""
    res = await db.execute(select(CustomRitual).where(CustomRitual.id == ritual_id, CustomRitual.user_id == current_user.id))
    ritual = res.scalar_one_or_none()
    if not ritual:
        raise HTTPException(status_code=404, detail="Ritual not found")
    await db.delete(ritual)
    await db.commit()
    return None


@router.post("/custom/{ritual_id}/share", response_model=RitualSharePublic)
async def share_ritual(
    ritual_id: int,
    payload: RitualShareCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Share a ritual"""
    res = await db.execute(select(CustomRitual).where(CustomRitual.id == ritual_id, CustomRitual.user_id == current_user.id))
    ritual = res.scalar_one_or_none()
    if not ritual:
        raise HTTPException(status_code=404, detail="Ritual not found")

    share_code = uuid.uuid4().hex[:12]
    share = RitualShare(
        ritual_id=ritual_id,
        share_code=share_code
    )
    db.add(share)
    await db.commit()

    return {
        "share_url": f"https://soulnest.com/ritual/share/{share_code}",
        "share_code": share_code
    }


@router.get("/share/{share_code}", response_model=CustomRitualPublic)
async def get_shared_ritual(
    share_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Get shared ritual (public, no auth)"""
    res = await db.execute(select(RitualShare).where(RitualShare.share_code == share_code))
    share = res.scalar_one_or_none()
    if not share:
        raise HTTPException(status_code=404, detail="Shared ritual not found")

    stmt = select(CustomRitual).options(
        selectinload(CustomRitual.steps)
    ).where(CustomRitual.id == share.ritual_id)
    res = await db.execute(stmt)
    ritual = res.scalar_one_or_none()
    if not ritual:
        raise HTTPException(status_code=404, detail="Ritual not found")
    return ritual


@router.post("/custom/{ritual_id}/add-to-cart")
async def add_ritual_to_cart(
    ritual_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add all products from ritual to cart"""
    from app.models import CartItem

    stmt = select(CustomRitual).options(
        selectinload(CustomRitual.steps)
    ).where(CustomRitual.id == ritual_id, CustomRitual.user_id == current_user.id)
    res = await db.execute(stmt)
    ritual = res.scalar_one_or_none()
    if not ritual:
        raise HTTPException(status_code=404, detail="Ritual not found")

    items_added = 0
    for step in ritual.steps:
        if step.product_id:
            # Check if already in cart
            existing = await db.execute(
                select(CartItem).where(
                    CartItem.user_id == current_user.id,
                    CartItem.product_id == step.product_id
                )
            )
            if not existing.scalar_one_or_none():
                cart_item = CartItem(
                    user_id=current_user.id,
                    product_id=step.product_id,
                    quantity=1
                )
                db.add(cart_item)
                items_added += 1

    await db.commit()
    return {"message": "Ritual products added to cart", "items_added": items_added}

