from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator


class Message(BaseModel):
    message: str


# Auth / User
class UserBase(BaseModel):
    name: str
    email: str
    is_guest: bool = False


class UserCreate(BaseModel):
    name: str = ""
    email: str = ""
    password: str = ""


class UserLogin(BaseModel):
    email: str = ""
    password: str = ""


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# Categories
class CategoryBase(BaseModel):
    slug: str
    title: str
    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    image_url: Optional[str] = None


class CategoryPublic(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# Products
class ProductImagePublic(BaseModel):
    id: int
    image_url: str
    display_order: int

    class Config:
        from_attributes = True


class ProductHowToUsePublic(BaseModel):
    id: int
    instruction: str
    step_order: int

    class Config:
        from_attributes = True


class ProductGuaranteePublic(BaseModel):
    id: int
    guarantee_text: str

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    product_id: str
    title: str
    tagline: Optional[str] = None
    description: Optional[str] = None
    price: float
    compare_at_price: Optional[float] = None
    rating: float = 0.0
    reviews_count: int = 0
    brand_info: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: bool = False
    is_bestseller: bool = False


class ProductPublic(ProductBase):
    id: int
    images: List[ProductImagePublic] = []
    how_to_use: List[ProductHowToUsePublic] = []
    guarantees: List[ProductGuaranteePublic] = []

    class Config:
        from_attributes = True


# Ritual Guide
class RitualGuidePublic(BaseModel):
    id: int
    category_id: int
    step_number: int
    step_title: str
    product_id: Optional[int] = None

    class Config:
        from_attributes = True


# Cart
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemPublic(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartSummary(BaseModel):
    subtotal: float
    delivery_fee: float
    savings: float
    total: float


# Orders
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderItemPublic(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: float

    class Config:
        from_attributes = True


class OrderPublic(BaseModel):
    id: int
    order_number: str
    subtotal: float
    delivery_fee: float
    savings: float
    total: float
    status: str
    created_at: datetime
    items: List[OrderItemPublic] = []

    class Config:
        from_attributes = True


# Reviews
class ReviewCreate(BaseModel):
    rating: int
    comment: Optional[str] = None


class ReviewPublic(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Wishlist
class WishlistCreate(BaseModel):
    product_id: int


class WishlistPublic(BaseModel):
    id: int
    product_id: int

    class Config:
        from_attributes = True


# Addresses
class AddressCreate(BaseModel):
    full_name: str
    street_address: str
    city: str
    state: Optional[str] = None
    zip_code: str
    country: str = "USA"
    phone: Optional[str] = None
    is_default: bool = False


class AddressPublic(AddressCreate):
    id: int

    class Config:
        from_attributes = True


# Payment Methods
class PaymentMethodCreate(BaseModel):
    card_type: Optional[str] = None
    last_four: str
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None
    is_default: bool = False


class PaymentMethodPublic(PaymentMethodCreate):
    id: int

    class Config:
        from_attributes = True


# Tips / Blog
class TipPublic(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    content: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Newsletter
class NewsletterSubscribe(BaseModel):
    email: EmailStr

