from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models import Tip
from app.schemas import TipPublic


router = APIRouter(prefix="/api/tips", tags=["tips"])


@router.get("", response_model=List[TipPublic])
async def list_tips(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Tip).order_by(Tip.created_at.desc()))
    return res.scalars().all()


@router.get("/{id}", response_model=TipPublic)
async def get_tip(id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Tip).where(Tip.id == id))
    tip = res.scalar_one_or_none()
    if not tip:
        raise HTTPException(status_code=404, detail="Tip not found")
    return tip


