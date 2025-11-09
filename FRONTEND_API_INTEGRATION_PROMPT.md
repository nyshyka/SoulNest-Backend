# SoulNest Backend API Integration Guide

Complete API documentation with curl examples and response formats for frontend integration.

**Base URL:** `http://127.0.0.1:8002` (or your backend URL)
**Authentication:** Bearer token in `Authorization` header: `Bearer {token}`

---

## Table of Contents
1. [Enhanced Orders](#enhanced-orders)
2. [Custom Rituals](#custom-rituals)
3. [Enhanced Reviews](#enhanced-reviews)
4. [Multiple Wishlists](#multiple-wishlists)
5. [Subscriptions](#subscriptions)
6. [Social Sharing](#social-sharing)
7. [For You Section](#for-you-section)

---

## Enhanced Orders

### 1. Create Order (Enhanced)
**POST** `/api/orders`

**Request:**
```bash
curl -X POST http://127.0.0.1:8002/api/orders \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": 1, "quantity": 2, "price_at_purchase": 24.99}
    ],
    "shipping_address": {
      "full_name": "John Doe",
      "street_address": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip_code": "10001",
      "country": "United States",
      "phone": "+1234567890"
    },
    "payment_method": {
      "card_number": "****1234",
      "card_name": "JOHN DOE",
      "expiry_month": "12",
      "expiry_year": "25",
      "save_card": false
    }
  }'
```

**Response:**
```json
{
  "id": 1,
  "order_number": "SN-A1B2C3D4E5",
  "status": "processing",
  "tracking_number": null,
  "subtotal": 49.98,
  "delivery_fee": 0.0,
  "savings": 5.0,
  "total": 44.98,
  "created_at": "2024-01-15T10:30:00Z",
  "items": [],
  "shipping_address": null,
  "payment_method": null
}
```

### 2. Get Order Details
**GET** `/api/orders/{order_id}`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/orders/1
```

### 3. Get All Orders
**GET** `/api/orders?status=processing&limit=20&offset=0`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://127.0.0.1:8002/api/orders?status=processing&limit=20&offset=0"
```

**Response:**
```json
[
  {
    "id": 1,
    "order_number": "SN-A1B2C3D4E5",
    "status": "processing",
    "total": 44.98,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### 4. Complete Order
**POST** `/api/orders/{order_id}/complete`

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/orders/1/complete
```

### 5. Request Return
**POST** `/api/orders/{order_id}/return`

```bash
curl -X POST http://127.0.0.1:8002/api/orders/1/return \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "reason": "Defective product",
    "notes": "Additional details"
  }'
```

**Response:**
```json
{
  "return_id": 1,
  "status": "pending",
  "created_at": "2024-01-15T12:00:00Z"
}
```

### 6. Update Order Status
**PUT** `/api/orders/{order_id}/status`

```bash
curl -X PUT http://127.0.0.1:8002/api/orders/1/status \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped",
    "tracking_number": "TRK-1234567890"
  }'
```

---

## Custom Rituals

### 1. Save Custom Ritual
**POST** `/api/rituals/custom`

```bash
curl -X POST http://127.0.0.1:8002/api/rituals/custom \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Evening Self-Care Ritual",
    "steps": [
      {"step_number": 1, "title": "Light a candle", "product_id": 1},
      {"step_number": 2, "title": "Brew tea", "product_id": 2}
    ]
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Evening Self-Care Ritual",
  "bundle_price": 45.98,
  "savings": 4.60,
  "created_at": "2024-01-15T10:30:00Z",
  "steps": [
    {"id": 1, "step_number": 1, "title": "Light a candle", "product_id": 1},
    {"id": 2, "step_number": 2, "title": "Brew tea", "product_id": 2}
  ]
}
```

### 2. Get Saved Rituals
**GET** `/api/rituals/custom`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/rituals/custom
```

### 3. Get Ritual Details
**GET** `/api/rituals/custom/{ritual_id}`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/rituals/custom/1
```

### 4. Delete Ritual
**DELETE** `/api/rituals/custom/{ritual_id}`

```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/rituals/custom/1
```

### 5. Share Ritual
**POST** `/api/rituals/custom/{ritual_id}/share`

```bash
curl -X POST http://127.0.0.1:8002/api/rituals/custom/1/share \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "email",
    "recipient_email": "friend@example.com"
  }'
```

**Response:**
```json
{
  "share_url": "https://soulnest.com/ritual/share/abc123def456",
  "share_code": "abc123def456"
}
```

### 6. Get Shared Ritual (Public)
**GET** `/api/rituals/share/{share_code}`

```bash
curl http://127.0.0.1:8002/api/rituals/share/abc123def456
```

### 7. Add Ritual to Cart
**POST** `/api/rituals/custom/{ritual_id}/add-to-cart`

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/rituals/custom/1/add-to-cart
```

**Response:**
```json
{
  "message": "Ritual products added to cart",
  "items_added": 2
}
```

---

## Enhanced Reviews

### 1. Submit Review with Photos
**POST** `/api/products/{product_id}/reviews`

```bash
curl -X POST http://127.0.0.1:8002/api/products/1/reviews \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Amazing product!",
    "photos": ["base64_image_1", "base64_image_2"]
  }'
```

**Response:**
```json
{
  "id": 1,
  "product_id": 1,
  "user_id": 1,
  "rating": 5,
  "comment": "Amazing product!",
  "photos": [
    {"id": 1, "image_url": "https://...", "display_order": 0}
  ],
  "helpful_count": 0,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 2. Get Product Reviews (Enhanced)
**GET** `/api/products/{product_id}/reviews?rating=5&with_photos=true&sort=recent&limit=10&offset=0`

```bash
curl "http://127.0.0.1:8002/api/products/1/reviews?rating=5&with_photos=true&sort=recent"
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "user_name": "Sarah M.",
    "rating": 5,
    "comment": "Amazing product!",
    "photos": [{"id": 1, "image_url": "https://...", "display_order": 0}],
    "helpful_count": 12,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### 3. Mark Review as Helpful
**POST** `/api/reviews/{review_id}/helpful`

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/reviews/1/helpful
```

**Response:**
```json
{
  "review_id": 1,
  "helpful_count": 13,
  "user_has_voted": true
}
```

### 4. Delete Review
**DELETE** `/api/reviews/{review_id}`

```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/reviews/1
```

---

## Multiple Wishlists

### 1. Create Wishlist
**POST** `/api/wishlists`

```bash
curl -X POST http://127.0.0.1:8002/api/wishlists \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "For Me"}'
```

**Response:**
```json
{
  "id": 1,
  "name": "For Me",
  "user_id": 1,
  "products_count": 0,
  "is_shared": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 2. Get All Wishlists
**GET** `/api/wishlists`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/wishlists
```

### 3. Get Wishlist Details
**GET** `/api/wishlists/{wishlist_id}`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/wishlists/1
```

**Response:**
```json
{
  "id": 1,
  "name": "For Me",
  "is_shared": false,
  "products": [
    {
      "id": 1,
      "product_id": 1,
      "product": {
        "id": 1,
        "title": "Calm Candle",
        "price": 24.99
      },
      "added_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 4. Add Product to Wishlist
**POST** `/api/wishlists/{wishlist_id}/products`

```bash
curl -X POST http://127.0.0.1:8002/api/wishlists/1/products \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'
```

### 5. Remove Product from Wishlist
**DELETE** `/api/wishlists/{wishlist_id}/products/{product_id}`

```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/wishlists/1/products/1
```

### 6. Share Wishlist
**POST** `/api/wishlists/{wishlist_id}/share`

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/wishlists/1/share
```

**Response:**
```json
{
  "share_url": "https://soulnest.com/wishlist/share/xyz789",
  "share_code": "xyz789"
}
```

### 7. Get Shared Wishlist (Public)
**GET** `/api/wishlists/share/{share_code}`

```bash
curl http://127.0.0.1:8002/api/wishlists/share/xyz789
```

### 8. Update Wishlist
**PUT** `/api/wishlists/{wishlist_id}`

```bash
curl -X PUT http://127.0.0.1:8002/api/wishlists/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "is_shared": true
  }'
```

### 9. Delete Wishlist
**DELETE** `/api/wishlists/{wishlist_id}`

```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/wishlists/1
```

### 10. Price Drop Alert
**POST** `/api/wishlists/{wishlist_id}/price-alerts`

```bash
curl -X POST http://127.0.0.1:8002/api/wishlists/1/price-alerts \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "alert_threshold": 20.00
  }'
```

### 11. Back in Stock Alert
**POST** `/api/wishlists/{wishlist_id}/stock-alerts`

```bash
curl -X POST http://127.0.0.1:8002/api/wishlists/1/stock-alerts \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'
```

---

## Subscriptions

### 1. Create Subscription
**POST** `/api/subscriptions`

```bash
curl -X POST http://127.0.0.1:8002/api/subscriptions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monthly Self-Care Box",
    "frequency": "monthly",
    "products": [1, 2, 3],
    "price": 49.99
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Monthly Self-Care Box",
  "frequency": "monthly",
  "price": 49.99,
  "status": "active",
  "next_delivery": "2024-02-15",
  "created_at": "2024-01-15T10:30:00Z",
  "products": []
}
```

### 2. Get All Subscriptions
**GET** `/api/subscriptions`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/subscriptions
```

### 3. Get Subscription Details
**GET** `/api/subscriptions/{subscription_id}`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/subscriptions/1
```

### 4. Update Subscription
**PUT** `/api/subscriptions/{subscription_id}`

```bash
curl -X PUT http://127.0.0.1:8002/api/subscriptions/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "frequency": "bi-monthly",
    "products": [1, 2, 3, 4],
    "price": 59.99
  }'
```

### 5. Pause Subscription
**POST** `/api/subscriptions/{subscription_id}/pause`

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/subscriptions/1/pause
```

**Response:**
```json
{
  "id": 1,
  "status": "paused",
  "paused_until": null
}
```

### 6. Resume Subscription
**POST** `/api/subscriptions/{subscription_id}/resume`

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/subscriptions/1/resume
```

### 7. Cancel Subscription
**POST** `/api/subscriptions/{subscription_id}/cancel`

```bash
curl -X POST http://127.0.0.1:8002/api/subscriptions/1/cancel \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason": "No longer needed"}'
```

**Response:**
```json
{
  "id": 1,
  "status": "cancelled",
  "cancelled_at": "2024-01-15T10:30:00Z"
}
```

### 8. Skip Next Delivery
**POST** `/api/subscriptions/{subscription_id}/skip`

```bash
curl -X POST http://127.0.0.1:8002/api/subscriptions/1/skip \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"skip_count": 1}'
```

---

## Social Sharing

### 1. Share Product
**POST** `/api/products/{product_id}/share`

```bash
curl -X POST http://127.0.0.1:8002/api/products/1/share \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "facebook",
    "message": "Check out this amazing product!",
    "recipient_email": "friend@example.com"
  }'
```

**Response:**
```json
{
  "share_url": "https://soulnest.com/product/1?ref=abc123",
  "share_code": "abc123"
}
```

### 2. Create Group Ritual
**POST** `/api/rituals/group`

```bash
curl -X POST http://127.0.0.1:8002/api/rituals/group \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Friends Self-Care Night",
    "ritual_id": 1,
    "participants": ["user@example.com", "friend@example.com"]
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Friends Self-Care Night",
  "ritual_id": 1,
  "participants_count": 3,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 3. Get Group Rituals
**GET** `/api/rituals/group`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8002/api/rituals/group
```

---

## For You Section

### 1. Save Quiz Result
**POST** `/api/for-you/quiz-results`

```bash
curl -X POST http://127.0.0.1:8002/api/for-you/quiz-results \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {"1": 0, "2": 2, "3": 1, "4": 3},
    "recommended_ritual_id": 1
  }'
```

### 2. Save Mood Entry
**POST** `/api/for-you/mood-entries`

```bash
curl -X POST http://127.0.0.1:8002/api/for-you/mood-entries \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mood": 4,
    "note": "Feeling great today!",
    "date": "2024-01-15"
  }'
```

### 3. Get Mood Entries
**GET** `/api/for-you/mood-entries?start_date=2024-01-01&end_date=2024-01-31`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://127.0.0.1:8002/api/for-you/mood-entries?start_date=2024-01-01&end_date=2024-01-31"
```

### 4. Save Calendar Entry
**POST** `/api/for-you/calendar-entries`

```bash
curl -X POST http://127.0.0.1:8002/api/for-you/calendar-entries \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-01-15",
    "ritual_completed": true,
    "notes": "Completed evening ritual"
  }'
```

### 5. Get Calendar Entries
**GET** `/api/for-you/calendar-entries?month=2024-01&year=2024`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://127.0.0.1:8002/api/for-you/calendar-entries?month=2024-01&year=2024"
```

### 6. Save Journal Entry
**POST** `/api/for-you/journal-entries`

```bash
curl -X POST http://127.0.0.1:8002/api/for-you/journal-entries \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Today I'\''m grateful for...",
    "date": "2024-01-15"
  }'
```

### 7. Get Journal Entries
**GET** `/api/for-you/journal-entries?limit=10&offset=0`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://127.0.0.1:8002/api/for-you/journal-entries?limit=10&offset=0"
```

---

## Error Handling

All endpoints return errors in this format:
```json
{
  "detail": "Error message"
}
```

**Common Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

---

## Implementation Notes

1. **Token Storage:** Store JWT token in `localStorage` as `sn_token`
2. **Error Handling:** Show toast messages for all errors
3. **Loading States:** Show skeletons while fetching
4. **Optimistic Updates:** Update UI immediately, rollback on error
5. **Pagination:** Use limit/offset for list endpoints
6. **Image Upload:** Convert images to base64 for review photos
7. **Date Format:** Use ISO 8601 format (YYYY-MM-DD) for dates

---

## Quick Integration Checklist

- [ ] Update API base URL in frontend config
- [ ] Implement token storage/retrieval
- [ ] Create API client wrapper with error handling
- [ ] Add toast notifications
- [ ] Implement loading skeletons
- [ ] Wire up all endpoints to UI components
- [ ] Add error boundaries
- [ ] Test all endpoints with real data

