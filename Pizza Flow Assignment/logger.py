"""Appends completed orders (and session-start markers) to orders_log.txt.

Format is one 'Key: Value' line per field, blocks separated by a blank
line, so the file stays both human-readable and trivially parseable
(e.g. by splitting on '\n\n').
"""

from billing import Bill


def append_session_marker(path: str, session_timestamp: str) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"--- Session started: {session_timestamp} ---\n\n")


def append_order(
    path: str,
    order_timestamp: str,
    customer_name: str,
    phone: str,
    lines: list,
    bill: Bill,
    payment_mode: str,
) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"Timestamp: {order_timestamp}\n")
        f.write(f"Customer Name: {customer_name}\n")
        f.write(f"Phone: {phone}\n")
        for line in lines:
            f.write(f"{line.label}: {line.item_name} | Rs.{line.unit_price:.2f}\n")
        f.write(f"Unit Price Total: Rs.{bill.unit_total:.2f}\n")
        f.write(f"Quantity: {bill.quantity}\n")
        f.write(f"Subtotal: Rs.{bill.subtotal:.2f}\n")
        f.write(f"Discount Rate: {int(bill.discount_rate * 100)}%\n")
        f.write(f"Discount Amount: Rs.{bill.discount_amount:.2f}\n")
        f.write(f"Post-Discount Total: Rs.{bill.post_discount_total:.2f}\n")
        f.write(f"GST (18%): Rs.{bill.gst_amount:.2f}\n")
        f.write(f"Grand Total: Rs.{bill.grand_total:.2f}\n")
        f.write(f"Payment Mode: {payment_mode}\n")
        f.write("\n")
