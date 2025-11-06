from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from app.db.session import get_db
from app.models import CartItem, Product, User
from app.schemas import CartItemCreate, CartItemPublic, CartSummary
from app.utils.cart import calculate_cart
from .deps import get_current_user


router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("", response_model=List[CartItemPublic])
async def get_cart(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(CartItem).where(CartItem.user_id == current_user.id))
    return res.scalars().all()


@router.post("", response_model=CartItemPublic, status_code=201)
async def add_to_cart(payload: CartItemCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Ensure product exists
    prod = await db.execute(select(Product).where(Product.id == payload.product_id))
    if not prod.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")
    # Upsert-like behavior
    existing = await db.execute(
        select(CartItem).where(CartItem.user_id == current_user.id, CartItem.product_id == payload.product_id)
    )
    item = existing.scalar_one_or_none()
    if item:
        item.quantity += payload.quantity
    else:
        item = CartItem(user_id=current_user.id, product_id=payload.product_id, quantity=payload.quantity)
        db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/{item_id}", response_model=CartItemPublic)
async def update_cart_item(item_id: int, payload: CartItemCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(CartItem).where(CartItem.id == item_id, CartItem.user_id == current_user.id))
    item = res.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.product_id = payload.product_id
    item.quantity = payload.quantity
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
async def remove_cart_item(item_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(
        delete(CartItem).where(CartItem.id == item_id, CartItem.user_id == current_user.id)
    )
    await db.commit()
    return None


@router.delete("", status_code=204)
async def clear_cart(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(delete(CartItem).where(CartItem.user_id == current_user.id))
    await db.commit()
    return None


@router.get("/summary", response_model=CartSummary)
async def cart_summary(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(CartItem).where(CartItem.user_id == current_user.id))
    items = res.scalars().all()
    subtotal = 0.0
    for item in items:
        prod_res = await db.execute(select(Product).where(Product.id == item.product_id))
        product = prod_res.scalar_one()
        subtotal += float(product.price) * item.quantity
    delivery_fee, savings, total = calculate_cart(round(subtotal, 2))
    return CartSummary(subtotal=round(subtotal, 2), delivery_fee=delivery_fee, savings=savings, total=total)


