from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models import NewsletterSubscription
from app.schemas import NewsletterSubscribe, Message


router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])


@router.post("/subscribe", response_model=Message)
async def subscribe(payload: NewsletterSubscribe, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(NewsletterSubscription).where(NewsletterSubscription.email == payload.email))
    existing = res.scalar_one_or_none()
    if existing:
        existing.is_active = True
    else:
        db.add(NewsletterSubscription(email=payload.email, is_active=True))
    await db.commit()
    return Message(message="Subscribed")


@router.post("/unsubscribe", response_model=Message)
async def unsubscribe(payload: NewsletterSubscribe, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(NewsletterSubscription).where(NewsletterSubscription.email == payload.email))
    existing = res.scalar_one_or_none()
    if existing:
        existing.is_active = False
        await db.commit()
    return Message(message="Unsubscribed")

