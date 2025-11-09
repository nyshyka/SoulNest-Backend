"""New schemas for enhanced features"""
from __future__ import annotations
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr


# Enhanced Orders
class ShippingAddressCreate(BaseModel):
    full_name: str
    street_address: str
    city: str
    state: Optional[str] = None
    zip_code: str
    country: str = "United States"
    phone: Optional[str] = None


class PaymentMethodCreateOrder(BaseModel):
    card_number: str  # Will be masked
    card_name: str
    expiry_month: str
    expiry_year: str
    save_card: bool = False


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float


class OrderCreateEnhanced(BaseModel):
    items: List[OrderItemCreate]
    shipping_address: ShippingAddressCreate
    payment_method: PaymentMethodCreateOrder


class OrderItemPublicEnhanced(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: float

    class Config:
        from_attributes = True


class ShippingAddressPublic(BaseModel):
    id: int
    full_name: str
    street_address: str
    city: str
    state: Optional[str] = None
    zip_code: str
    country: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True


class PaymentMethodPublicEnhanced(BaseModel):
    id: int
    card_type: Optional[str] = None
    last_four: str
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None

    class Config:
        from_attributes = True


class OrderPublicEnhanced(BaseModel):
    id: int
    order_number: str
    status: str
    tracking_number: Optional[str] = None
    subtotal: float
    delivery_fee: float
    savings: float
    total: float
    created_at: datetime
    items: List[OrderItemPublicEnhanced] = []
    shipping_address: Optional[ShippingAddressPublic] = None
    payment_method: Optional[PaymentMethodPublicEnhanced] = None

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
    tracking_number: Optional[str] = None


class OrderReturnCreate(BaseModel):
    item_id: int
    reason: str
    notes: Optional[str] = None


# Custom Rituals
class RitualStepCreate(BaseModel):
    step_number: int
    title: str
    product_id: Optional[int] = None


class CustomRitualCreate(BaseModel):
    name: str
    steps: List[RitualStepCreate]


class RitualStepPublic(BaseModel):
    id: int
    step_number: int
    title: str
    product_id: Optional[int] = None

    class Config:
        from_attributes = True


class CustomRitualPublic(BaseModel):
    id: int
    name: str
    bundle_price: Optional[float] = None
    savings: float = 0.0
    created_at: datetime
    steps: List[RitualStepPublic] = []

    class Config:
        from_attributes = True


class RitualShareCreate(BaseModel):
    platform: Optional[str] = None
    recipient_email: Optional[EmailStr] = None


class RitualSharePublic(BaseModel):
    share_url: str
    share_code: str


# Enhanced Reviews
class ReviewCreateEnhanced(BaseModel):
    rating: int
    comment: Optional[str] = None
    photos: Optional[List[str]] = None  # base64 images


class ReviewPhotoPublic(BaseModel):
    id: int
    image_url: str
    display_order: int

    class Config:
        from_attributes = True


class ReviewPublicEnhanced(BaseModel):
    id: int
    user_id: int
    user_name: Optional[str] = None
    product_id: int
    rating: int
    comment: Optional[str] = None
    photos: List[ReviewPhotoPublic] = []
    helpful_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewHelpfulResponse(BaseModel):
    review_id: int
    helpful_count: int
    user_has_voted: bool


# Multiple Wishlists
class WishlistCreate(BaseModel):
    name: str = "My Wishlist"


class WishlistItemPublic(BaseModel):
    id: int
    product_id: int
    product: Optional[Any] = None
    added_at: datetime

    class Config:
        from_attributes = True


class WishlistPublic(BaseModel):
    id: int
    name: str
    is_shared: bool = False
    products_count: int = 0
    created_at: datetime
    products: List[WishlistItemPublic] = []

    class Config:
        from_attributes = True


class WishlistSharePublic(BaseModel):
    share_url: str
    share_code: str


class WishlistUpdate(BaseModel):
    name: Optional[str] = None
    is_shared: Optional[bool] = None


class PriceAlertCreate(BaseModel):
    product_id: int
    alert_threshold: Optional[float] = None


class StockAlertCreate(BaseModel):
    product_id: int


# Subscriptions
class SubscriptionItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class SubscriptionCreate(BaseModel):
    name: str
    frequency: str  # monthly, bi-monthly, quarterly
    products: List[int]
    price: float


class SubscriptionPublic(BaseModel):
    id: int
    name: str
    frequency: str
    price: float
    status: str
    next_delivery: Optional[date] = None
    created_at: datetime
    products: List[Any] = []

    class Config:
        from_attributes = True


class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[str] = None
    products: Optional[List[int]] = None
    price: Optional[float] = None


class SubscriptionCancel(BaseModel):
    reason: Optional[str] = None


class SubscriptionSkip(BaseModel):
    skip_count: int = 1


# Social Sharing
class ShareCreate(BaseModel):
    platform: Optional[str] = None  # facebook, twitter, pinterest, email
    message: Optional[str] = None
    recipient_email: Optional[EmailStr] = None


class SharePublic(BaseModel):
    share_url: str
    share_code: str


class GroupRitualCreate(BaseModel):
    name: str
    ritual_id: Optional[int] = None
    participants: List[EmailStr]


class GroupRitualPublic(BaseModel):
    id: int
    name: str
    ritual_id: Optional[int] = None
    participants_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


# For You Section
class QuizResultCreate(BaseModel):
    answers: Dict[str, int]
    recommended_ritual_id: Optional[int] = None


class MoodEntryCreate(BaseModel):
    mood: int  # 1-5
    note: Optional[str] = None
    date: Optional[date] = None


class MoodEntryPublic(BaseModel):
    id: int
    mood: int
    note: Optional[str] = None
    entry_date: date
    created_at: datetime

    class Config:
        from_attributes = True


class CalendarEntryCreate(BaseModel):
    date: date
    ritual_completed: bool = False
    notes: Optional[str] = None


class CalendarEntryPublic(BaseModel):
    id: int
    entry_date: date
    ritual_completed: bool
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class JournalEntryCreate(BaseModel):
    content: str
    date: Optional[date] = None


class JournalEntryPublic(BaseModel):
    id: int
    content: str
    entry_date: date
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

