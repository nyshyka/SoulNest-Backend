from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.session import get_db
from app.models import User, OldWishlist, Address, PaymentMethod, Order, Product
from app.schemas import (
    UserPublic,
    WishlistCreate,
    WishlistPublic,
    AddressCreate,
    AddressPublic,
    PaymentMethodCreate,
    PaymentMethodPublic,
    ProductPublic,
)
from .deps import get_current_user


router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("", response_model=UserPublic)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("", response_model=UserPublic)
async def update_profile(payload: UserPublic, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    current_user.name = payload.name
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/wishlist", response_model=List[WishlistPublic])
async def list_wishlist(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(OldWishlist).where(OldWishlist.user_id == current_user.id))
    return res.scalars().all()


@router.post("/wishlist", response_model=WishlistPublic, status_code=201)
async def add_wishlist(payload: WishlistCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    exists = await db.execute(select(OldWishlist).where(OldWishlist.user_id == current_user.id, OldWishlist.product_id == payload.product_id))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already in wishlist")
    item = OldWishlist(user_id=current_user.id, product_id=payload.product_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/wishlist/{id}", status_code=204)
async def remove_wishlist(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(delete(OldWishlist).where(OldWishlist.id == id, OldWishlist.user_id == current_user.id))
    await db.commit()
    return None


@router.get("/addresses", response_model=List[AddressPublic])
async def list_addresses(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Address).where(Address.user_id == current_user.id))
    return res.scalars().all()


@router.post("/addresses", response_model=AddressPublic, status_code=201)
async def add_address(payload: AddressCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    addr = Address(user_id=current_user.id, **payload.model_dump())
    db.add(addr)
    await db.commit()
    await db.refresh(addr)
    return addr


@router.put("/addresses/{id}", response_model=AddressPublic)
async def update_address(id: int, payload: AddressCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Address).where(Address.id == id, Address.user_id == current_user.id))
    addr = res.scalar_one_or_none()
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    for k, v in payload.model_dump().items():
        setattr(addr, k, v)
    await db.commit()
    await db.refresh(addr)
    return addr


@router.delete("/addresses/{id}", status_code=204)
async def delete_address(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Address).where(Address.id == id, Address.user_id == current_user.id))
    await db.commit()
    return None


@router.get("/payment-methods", response_model=List[PaymentMethodPublic])
async def list_payment_methods(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(PaymentMethod).where(PaymentMethod.user_id == current_user.id))
    return res.scalars().all()


@router.post("/payment-methods", response_model=PaymentMethodPublic, status_code=201)
async def add_payment_method(payload: PaymentMethodCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    pm = PaymentMethod(user_id=current_user.id, **payload.model_dump())
    db.add(pm)
    await db.commit()
    await db.refresh(pm)
    return pm


@router.delete("/payment-methods/{id}", status_code=204)
async def delete_payment_method(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(delete(PaymentMethod).where(PaymentMethod.id == id, PaymentMethod.user_id == current_user.id))
    await db.commit()
    return None


@router.get("/recommendations", response_model=List[ProductPublic])
async def recommendations(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Very simple heuristic: products from categories of user's past orders, otherwise featured
    cat_ids_res = await db.execute(
        select(Product.category_id)
        .join(Order, isouter=True)
        .join(Order.items)
        .where(Order.user_id == current_user.id)
    )
    cat_ids = [cid for cid in cat_ids_res.scalars().all() if cid]
    if cat_ids:
        res = await db.execute(select(Product).where(Product.category_id.in_(cat_ids)).limit(8))
        return res.scalars().all()
    res = await db.execute(select(Product).where(Product.is_featured.is_(True)).limit(8))
    return res.scalars().all()


