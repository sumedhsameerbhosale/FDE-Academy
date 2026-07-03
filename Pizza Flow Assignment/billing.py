"""Pure pricing/discount/GST math -- no I/O, easy to hand-verify."""

from dataclasses import dataclass

GST_RATE = 0.18
DISCOUNT_RATE = 0.10
DISCOUNT_QTY_THRESHOLD = 5


@dataclass
class BillLine:
    label: str
    item_name: str
    unit_price: float


@dataclass
class Bill:
    lines: list
    quantity: int
    unit_total: float
    subtotal: float
    discount_rate: float
    discount_amount: float
    post_discount_total: float
    gst_amount: float
    grand_total: float


def compute_bill(lines: list, quantity: int) -> Bill:
    unit_total = sum(line.unit_price for line in lines)
    subtotal = unit_total * quantity

    discount_rate = DISCOUNT_RATE if quantity >= DISCOUNT_QTY_THRESHOLD else 0.0
    discount_amount = round(subtotal * discount_rate, 2)

    post_discount_total = round(subtotal - discount_amount, 2)
    gst_amount = round(post_discount_total * GST_RATE, 2)
    grand_total = round(post_discount_total + gst_amount, 2)

    return Bill(
        lines=lines,
        quantity=quantity,
        unit_total=round(unit_total, 2),
        subtotal=round(subtotal, 2),
        discount_rate=discount_rate,
        discount_amount=discount_amount,
        post_discount_total=post_discount_total,
        gst_amount=gst_amount,
        grand_total=grand_total,
    )
