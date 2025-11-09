"""Subscriptions endpoints"""
from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.new_models import Subscription, SubscriptionItem, SubscriptionSkip
from app.models import Product, User
from app.schemas.new_schemas import (
    SubscriptionCreate, SubscriptionPublic, SubscriptionUpdate,
    SubscriptionCancel, SubscriptionSkip as SubscriptionSkipSchema
)
from .deps import get_current_user


router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])


def calculate_next_delivery(frequency: str) -> date:
    """Calculate next delivery date based on frequency"""
    today = date.today()
    if frequency == "monthly":
        return today + timedelta(days=30)
    elif frequency == "bi-monthly":
        return today + timedelta(days=60)
    elif frequency == "quarterly":
        return today + timedelta(days=90)
    return today + timedelta(days=30)


@router.post("", response_model=SubscriptionPublic, status_code=201)
async def create_subscription(
    payload: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a subscription"""
    next_delivery = calculate_next_delivery(payload.frequency)

    subscription = Subscription(
        user_id=current_user.id,
        name=payload.name,
        frequency=payload.frequency,
        price=payload.price,
        status="active",
        next_delivery=next_delivery
    )
    db.add(subscription)
    await db.flush()

    # Add products
    for product_id in payload.products:
        item = SubscriptionItem(
            subscription_id=subscription.id,
            product_id=product_id,
            quantity=1
        )
        db.add(item)

    await db.commit()
    await db.refresh(subscription)
    return subscription


@router.get("", response_model=List[SubscriptionPublic])
async def get_all_subscriptions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all subscriptions"""
    stmt = select(Subscription).where(Subscription.user_id == current_user.id).order_by(Subscription.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/{subscription_id}", response_model=SubscriptionPublic)
async def get_subscription_details(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get subscription details"""
    stmt = select(Subscription).options(
        selectinload(Subscription.items).selectinload(SubscriptionItem.product)
    ).where(Subscription.id == subscription_id, Subscription.user_id == current_user.id)
    res = await db.execute(stmt)
    subscription = res.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.put("/{subscription_id}", response_model=SubscriptionPublic)
async def update_subscription(
    subscription_id: int,
    payload: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update subscription"""
    stmt = select(Subscription).where(Subscription.id == subscription_id, Subscription.user_id == current_user.id)
    res = await db.execute(stmt)
    subscription = res.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    if payload.name:
        subscription.name = payload.name
    if payload.frequency:
        subscription.frequency = payload.frequency
        subscription.next_delivery = calculate_next_delivery(payload.frequency)
    if payload.price:
        subscription.price = payload.price
    if payload.products:
        # Delete old items
        await db.execute(delete(SubscriptionItem).where(SubscriptionItem.subscription_id == subscription_id))
        # Add new items
        for product_id in payload.products:
            item = SubscriptionItem(subscription_id=subscription_id, product_id=product_id, quantity=1)
            db.add(item)

    await db.commit()
    await db.refresh(subscription)
    return subscription


@router.post("/{subscription_id}/pause", response_model=SubscriptionPublic)
async def pause_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Pause subscription"""
    res = await db.execute(select(Subscription).where(Subscription.id == subscription_id, Subscription.user_id == current_user.id))
    subscription = res.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.status = "paused"
    await db.commit()
    await db.refresh(subscription)
    return subscription


@router.post("/{subscription_id}/resume", response_model=SubscriptionPublic)
async def resume_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Resume subscription"""
    res = await db.execute(select(Subscription).where(Subscription.id == subscription_id, Subscription.user_id == current_user.id))
    subscription = res.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.status = "active"
    subscription.next_delivery = calculate_next_delivery(subscription.frequency)
    await db.commit()
    await db.refresh(subscription)
    return subscription


@router.post("/{subscription_id}/cancel", response_model=SubscriptionPublic)
async def cancel_subscription(
    subscription_id: int,
    payload: SubscriptionCancel,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Cancel subscription"""
    from datetime import datetime
    res = await db.execute(select(Subscription).where(Subscription.id == subscription_id, Subscription.user_id == current_user.id))
    subscription = res.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.status = "cancelled"
    subscription.cancelled_at = datetime.utcnow()
    subscription.cancellation_reason = payload.reason
    await db.commit()
    await db.refresh(subscription)
    return subscription


@router.post("/{subscription_id}/skip")
async def skip_next_delivery(
    subscription_id: int,
    payload: SubscriptionSkipSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Skip next delivery(s)"""
    res = await db.execute(select(Subscription).where(Subscription.id == subscription_id, Subscription.user_id == current_user.id))
    subscription = res.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    for i in range(payload.skip_count):
        skip_date = subscription.next_delivery
        if skip_date:
            skip = SubscriptionSkip(subscription_id=subscription_id, skip_date=skip_date)
            db.add(skip)
            # Calculate next delivery after skip
            subscription.next_delivery = calculate_next_delivery(subscription.frequency)

    await db.commit()
    return {"message": f"Skipped {payload.skip_count} delivery(s)"}

