import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.session import get_db
from app.models import Order, OrderItem, CartItem, Product, User
from app.schemas import OrderCreate, OrderPublic
from app.utils.cart import calculate_cart
from .deps import get_current_user


router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderPublic, status_code=201)
async def create_order(payload: OrderCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Calculate subtotal from payload
    subtotal = 0.0
    items: list[OrderItem] = []
    for it in payload.items:
        prod_res = await db.execute(select(Product).where(Product.id == it.product_id))
        product = prod_res.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {it.product_id} not found")
        price = float(product.price)
        subtotal += price * it.quantity
        items.append(OrderItem(product_id=it.product_id, quantity=it.quantity, price_at_purchase=price))

    delivery_fee, savings, total = calculate_cart(round(subtotal, 2))
    order = Order(
        order_number=str(uuid.uuid4())[:8],
        user_id=current_user.id,
        subtotal=round(subtotal, 2),
        delivery_fee=delivery_fee,
        savings=savings,
        total=total,
        status="pending",
    )
    db.add(order)
    await db.flush()
    for oi in items:
        oi.order_id = order.id
        db.add(oi)
    await db.commit()
    await db.refresh(order)
    # Clear cart after checkout
    await db.execute(delete(CartItem).where(CartItem.user_id == current_user.id))
    await db.commit()
    return order


@router.get("", response_model=List[OrderPublic])
async def list_orders(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Order).where(Order.user_id == current_user.id).order_by(Order.created_at.desc()))
    return res.scalars().all()


@router.get("/{id}", response_model=OrderPublic)
async def get_order(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Order).where(Order.id == id, Order.user_id == current_user.id))
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{id}/cancel", response_model=OrderPublic)
async def cancel_order(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Order).where(Order.id == id, Order.user_id == current_user.id))
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status not in ("pending", "processing"):
        raise HTTPException(status_code=400, detail="Order cannot be cancelled")
    order.status = "cancelled"
    await db.commit()
    await db.refresh(order)
    return order


