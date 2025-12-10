"""Enhanced Orders endpoints"""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models import Order, OrderItem, Address, PaymentMethod, Product, User
from app.models.new_models import OrderReturn
from app.schemas.new_schemas import (
    OrderCreateEnhanced, OrderPublicEnhanced, OrderStatusUpdate, OrderReturnCreate
)
from app.utils.cart import calculate_cart
from .deps import get_current_user


router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("")
async def create_order_enhanced(
    payload: OrderCreateEnhanced,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Simple order creation - just save to DB"""
    # Create shipping address
    addr = Address(
        user_id=current_user.id,
        full_name=payload.shipping_address.full_name,
        street_address=payload.shipping_address.street_address,
        city=payload.shipping_address.city,
        state=payload.shipping_address.state,
        zip_code=payload.shipping_address.zip_code,
        country=payload.shipping_address.country,
        phone=payload.shipping_address.phone
    )
    db.add(addr)
    await db.flush()

    # Create payment method
    card_num = payload.payment_method.card_number.replace(" ", "")
    pm = PaymentMethod(
        user_id=current_user.id,
        last_four=card_num[-4:] if len(card_num) >= 4 else card_num,
        expiry_month=int(payload.payment_method.expiry_month) if payload.payment_method.expiry_month.isdigit() else None,
        expiry_year=int(payload.payment_method.expiry_year) if payload.payment_method.expiry_year.isdigit() else None,
        is_default=payload.payment_method.save_card
    )
    db.add(pm)
    await db.flush()

    # Calculate totals
    subtotal = sum(item.price_at_purchase * item.quantity for item in payload.items)
    delivery_fee, savings, total = calculate_cart(round(subtotal, 2))

    # Create order
    order = Order(
        order_number=f"SN-{uuid.uuid4().hex[:10].upper()}",
        user_id=current_user.id,
        subtotal=round(subtotal, 2),
        delivery_fee=delivery_fee,
        savings=savings,
        total=total,
        status="processing",
        shipping_address_id=addr.id,
        payment_method_id=pm.id
    )
    db.add(order)
    await db.flush()

    # Create order items
    for item in payload.items:
        oi = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.price_at_purchase
        )
        db.add(oi)

    await db.commit()
    
    # Return simple response - use JSONResponse to bypass validation
    return JSONResponse(
        status_code=201,
        content={
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total": float(order.total)
        }
    )


@router.get("/{order_id}", response_model=OrderPublicEnhanced)
async def get_order_details(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get order details"""
    stmt = select(Order).options(
        selectinload(Order.items),
        selectinload(Order.shipping_address),
        selectinload(Order.payment_method),
    ).where(Order.id == order_id, Order.user_id == current_user.id)
    res = await db.execute(stmt)
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("", response_model=List[OrderPublicEnhanced])
async def get_all_orders(
    status: Optional[str] = Query(None),
    limit: Optional[int] = Query(20),
    offset: Optional[int] = Query(0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all orders with optional filters"""
    stmt = select(Order).options(
        selectinload(Order.items),
        selectinload(Order.shipping_address),
        selectinload(Order.payment_method),
    ).where(Order.user_id == current_user.id)
    if status:
        stmt = stmt.where(Order.status == status)
    stmt = stmt.order_by(Order.created_at.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    return res.scalars().unique().all()


@router.post("/{order_id}/complete", response_model=OrderPublicEnhanced)
async def complete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark order as completed"""
    res = await db.execute(select(Order).where(Order.id == order_id, Order.user_id == current_user.id))
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "completed"
    await db.commit()
    # Reload with relationships
    stmt = select(Order).options(
        selectinload(Order.items),
        selectinload(Order.shipping_address),
        selectinload(Order.payment_method),
    ).where(Order.id == order.id)
    res = await db.execute(stmt)
    return res.scalar_one()


@router.post("/{order_id}/return", status_code=201)
async def request_return(
    order_id: int,
    payload: OrderReturnCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Request return for an order item"""
    res = await db.execute(select(Order).where(Order.id == order_id, Order.user_id == current_user.id))
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Verify order item exists
    item_res = await db.execute(select(OrderItem).where(OrderItem.id == payload.item_id, OrderItem.order_id == order_id))
    item = item_res.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")

    return_request = OrderReturn(
        order_id=order_id,
        order_item_id=payload.item_id,
        reason=payload.reason,
        notes=payload.notes,
        status="pending"
    )
    db.add(return_request)
    await db.commit()
    await db.refresh(return_request)
    return {"return_id": return_request.id, "status": "pending", "created_at": return_request.created_at}


@router.put("/{order_id}/status", response_model=OrderPublicEnhanced)
async def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update order status (admin or user)"""
    res = await db.execute(select(Order).where(Order.id == order_id, Order.user_id == current_user.id))
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = payload.status
    if payload.tracking_number:
        order.tracking_number = payload.tracking_number
    await db.commit()
    # Reload with relationships
    stmt = select(Order).options(
        selectinload(Order.items),
        selectinload(Order.shipping_address),
        selectinload(Order.payment_method),
    ).where(Order.id == order.id)
    res = await db.execute(stmt)
    return res.scalar_one()

