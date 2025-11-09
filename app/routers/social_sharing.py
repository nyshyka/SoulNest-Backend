"""Social Sharing endpoints"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.new_models import ProductShare, GroupRitual, GroupRitualParticipant
from app.models import Product, Category, User
from app.schemas.new_schemas import ShareCreate, SharePublic, GroupRitualCreate, GroupRitualPublic
from .deps import get_current_user


router = APIRouter(prefix="/api", tags=["social"])


@router.post("/products/{product_id}/share", response_model=SharePublic)
async def share_product(
    product_id: int,
    payload: ShareCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Share a product"""
    prod = await db.execute(select(Product).where(Product.id == product_id))
    if not prod.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")

    share_code = uuid.uuid4().hex[:12]
    share = ProductShare(
        product_id=product_id,
        user_id=current_user.id,
        share_code=share_code,
        platform=payload.platform
    )
    db.add(share)
    await db.commit()

    return {
        "share_url": f"https://soulnest.com/product/{product_id}?ref={share_code}",
        "share_code": share_code
    }


@router.post("/rituals/group", response_model=GroupRitualPublic, status_code=201)
async def create_group_ritual(
    payload: GroupRitualCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a group ritual"""
    group_ritual = GroupRitual(
        user_id=current_user.id,
        name=payload.name,
        ritual_id=payload.ritual_id
    )
    db.add(group_ritual)
    await db.flush()

    # Add participants
    for email in payload.participants:
        participant = GroupRitualParticipant(
            group_ritual_id=group_ritual.id,
            email=email
        )
        db.add(participant)

    await db.commit()
    await db.refresh(group_ritual)
    return group_ritual


@router.get("/rituals/group", response_model=List[GroupRitualPublic])
async def get_group_rituals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all group rituals"""
    stmt = select(GroupRitual).options(
        selectinload(GroupRitual.participants)
    ).where(GroupRitual.user_id == current_user.id).order_by(GroupRitual.created_at.desc())
    res = await db.execute(stmt)
    rituals = res.scalars().all()
    # Add participants_count
    for r in rituals:
        r.participants_count = len(r.participants) if r.participants else 0
    return rituals

