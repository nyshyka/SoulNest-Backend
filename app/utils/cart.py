from typing import Iterable, Tuple


def calculate_cart(subtotal: float) -> Tuple[float, float, float]:
    delivery_fee = 0.0 if subtotal >= 80.0 else 6.0
    savings = round(subtotal * 0.10, 2)
    total = round(subtotal + delivery_fee - savings, 2)
    return delivery_fee, savings, total

