"""Multiple Wishlists endpoints"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.new_models import Wishlist, WishlistItem, WishlistShare, WishlistPriceAlert, WishlistStockAlert
from app.models import Product, User
from app.schemas.new_schemas import (
    WishlistCreate, WishlistPublic, WishlistUpdate, WishlistSharePublic,
    PriceAlertCreate, StockAlertCreate
)
from .deps import get_current_user


router = APIRouter(prefix="/api/wishlists", tags=["wishlists"])


@router.post("", response_model=WishlistPublic, status_code=201)
async def create_wishlist(
    payload: WishlistCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new wishlist"""
    wishlist = Wishlist(
        user_id=current_user.id,
        name=payload.name
    )
    db.add(wishlist)
    await db.commit()
    await db.refresh(wishlist)
    return wishlist


@router.get("", response_model=List[WishlistPublic])
async def get_all_wishlists(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all wishlists for user"""
    stmt = select(Wishlist).where(Wishlist.user_id == current_user.id).order_by(Wishlist.created_at.desc())
    res = await db.execute(stmt)
    wishlists = res.scalars().all()
    # Add products_count
    for w in wishlists:
        count_res = await db.execute(select(func.count(WishlistItem.id)).where(WishlistItem.wishlist_id == w.id))
        w.products_count = count_res.scalar() or 0
    # Convert to dict for Pydantic
    return [{"id": w.id, "name": w.name, "is_shared": w.is_shared, "products_count": w.products_count, "created_at": w.created_at, "products": []} for w in wishlists]


@router.get("/{wishlist_id}", response_model=WishlistPublic)
async def get_wishlist_details(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get wishlist details with products"""
    stmt = select(Wishlist).options(
        selectinload(Wishlist.items).selectinload(WishlistItem.product)
    ).where(Wishlist.id == wishlist_id, Wishlist.user_id == current_user.id)
    res = await db.execute(stmt)
    wishlist = res.scalar_one_or_none()
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    return wishlist


@router.post("/{wishlist_id}/products", status_code=201)
async def add_product_to_wishlist(
    wishlist_id: int,
    payload: dict,  # {"product_id": 1}
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add product to wishlist"""
    res = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id, Wishlist.user_id == current_user.id))
    wishlist = res.scalar_one_or_none()
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    existing = await db.execute(
        select(WishlistItem).where(
            WishlistItem.wishlist_id == wishlist_id,
            WishlistItem.product_id == payload["product_id"]
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Product already in wishlist")

    item = WishlistItem(
        wishlist_id=wishlist_id,
        product_id=payload["product_id"]
    )
    db.add(item)
    await db.commit()
    return {"message": "Product added to wishlist"}


@router.delete("/{wishlist_id}/products/{product_id}", status_code=204)
async def remove_product_from_wishlist(
    wishlist_id: int,
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove product from wishlist"""
    res = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id, Wishlist.user_id == current_user.id))
    if not res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Wishlist not found")

    await db.execute(
        delete(WishlistItem).where(
            WishlistItem.wishlist_id == wishlist_id,
            WishlistItem.product_id == product_id
        )
    )
    await db.commit()
    return None


@router.post("/{wishlist_id}/share", response_model=WishlistSharePublic)
async def share_wishlist(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Share wishlist"""
    res = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id, Wishlist.user_id == current_user.id))
    wishlist = res.scalar_one_or_none()
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    share_code = uuid.uuid4().hex[:12]
    share = WishlistShare(
        wishlist_id=wishlist_id,
        share_code=share_code
    )
    db.add(share)
    await db.commit()

    return {
        "share_url": f"https://soulnest.com/wishlist/share/{share_code}",
        "share_code": share_code
    }


@router.get("/share/{share_code}", response_model=WishlistPublic)
async def get_shared_wishlist(
    share_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Get shared wishlist (public)"""
    res = await db.execute(select(WishlistShare).where(WishlistShare.share_code == share_code))
    share = res.scalar_one_or_none()
    if not share:
        raise HTTPException(status_code=404, detail="Shared wishlist not found")

    stmt = select(Wishlist).options(
        selectinload(Wishlist.items).selectinload(WishlistItem.product)
    ).where(Wishlist.id == share.wishlist_id)
    res = await db.execute(stmt)
    wishlist = res.scalar_one_or_none()
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    return wishlist


@router.put("/{wishlist_id}", response_model=WishlistPublic)
async def update_wishlist(
    wishlist_id: int,
    payload: WishlistUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update wishlist"""
    res = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id, Wishlist.user_id == current_user.id))
    wishlist = res.scalar_one_or_none()
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    if payload.name:
        wishlist.name = payload.name
    if payload.is_shared is not None:
        wishlist.is_shared = payload.is_shared

    await db.commit()
    await db.refresh(wishlist)
    return wishlist


@router.delete("/{wishlist_id}", status_code=204)
async def delete_wishlist(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete wishlist"""
    res = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id, Wishlist.user_id == current_user.id))
    wishlist = res.scalar_one_or_none()
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    await db.delete(wishlist)
    await db.commit()
    return None


@router.post("/{wishlist_id}/price-alerts", status_code=201)
async def create_price_alert(
    wishlist_id: int,
    payload: PriceAlertCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create price drop alert"""
    res = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id, Wishlist.user_id == current_user.id))
    if not res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Wishlist not found")

    alert = WishlistPriceAlert(
        wishlist_id=wishlist_id,
        product_id=payload.product_id,
        alert_threshold=payload.alert_threshold
    )
    db.add(alert)
    await db.commit()
    return {"message": "Price alert created"}


@router.post("/{wishlist_id}/stock-alerts", status_code=201)
async def create_stock_alert(
    wishlist_id: int,
    payload: StockAlertCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create back in stock alert"""
    res = await db.execute(select(Wishlist).where(Wishlist.id == wishlist_id, Wishlist.user_id == current_user.id))
    if not res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Wishlist not found")

    alert = WishlistStockAlert(
        wishlist_id=wishlist_id,
        product_id=payload.product_id
    )
    db.add(alert)
    await db.commit()
    return {"message": "Stock alert created"}

