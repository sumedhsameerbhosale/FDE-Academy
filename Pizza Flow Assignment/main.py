"""PizzaFlow -- Stage 2 Working MVP.

Console pizza-ordering system that replaces Rajan's Google Form:
loads the menu from external .txt files, validates every customer
input, computes a GST-inclusive bill with a bulk discount, and logs
every completed order to orders_log.txt.
"""

import io
import sys
from datetime import datetime

import validators
from billing import BillLine, compute_bill
from logger import append_order, append_session_marker
from menu_loader import MenuLoadError, load_all_menus

BASE_FILE = "Types_of_Base.txt"
PIZZA_FILE = "Types_of_Pizza.txt"
TOPPING_FILE = "Types_of_Toppings.txt"
LOG_FILE = "orders_log.txt"

PAYMENT_MODES = {1: "Cash", 2: "Card", 3: "UPI"}


def _force_utf8_console() -> None:
    """Force UTF-8 on stdout/stderr/stdin so any non-ASCII text (e.g. a
    menu item name saved with special characters) can never raise
    UnicodeEncodeError on a default Windows console codepage."""
    for stream_name in ("stdout", "stderr", "stdin"):
        stream = getattr(sys, stream_name)
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            wrapped = io.TextIOWrapper(
                stream.buffer, encoding="utf-8", errors="replace", newline=""
            )
            setattr(sys, stream_name, wrapped)


def prompt_until_valid(prompt_text, validator_fn, *validator_args):
    while True:
        raw = validators.safe_input(prompt_text)
        ok, value, err = validator_fn(raw, *validator_args)
        if ok:
            return value
        print(err)


def display_menu(title, items):
    print(f"\n{title}")
    for i, item in enumerate(items, start=1):
        print(f"  {i}. {item.name:<25} Rs.{item.price:>7.2f}")


def choose_item(title, items):
    display_menu(title, items)
    idx = prompt_until_valid("Choice: ", validators.validate_menu_choice, len(items))
    return items[idx]


def format_bill(customer_name, phone, order_timestamp, lines, bill):
    out = []
    out.append("=" * 66)
    out.append("PIZZAFLOW - ORDER BILL".center(66))
    out.append("=" * 66)
    out.append(f"Customer   : {customer_name}")
    out.append(f"Phone      : {phone}")
    out.append(f"Order Time : {order_timestamp}")
    out.append("-" * 66)
    out.append(f"{'Item':<45}{'Unit Price (Rs.)':>21}")
    out.append("-" * 66)
    for line in lines:
        label = f"{line.label} : {line.item_name}"
        out.append(f"{label:<45}{line.unit_price:>18.2f}")
    out.append("-" * 66)
    out.append(f"{'Price per pizza':<45}{bill.unit_total:>18.2f}")
    out.append(f"{'Quantity':<45}{('x ' + str(bill.quantity)):>18}")
    out.append("-" * 66)
    out.append(f"{'Subtotal':<45}{bill.subtotal:>18.2f}")
    discount_label = f"Discount ({int(bill.discount_rate * 100)}%)"
    out.append(f"{discount_label:<45}{bill.discount_amount:>18.2f}")
    out.append(f"{'Post-Discount Total':<45}{bill.post_discount_total:>18.2f}")
    out.append(f"{'GST (18%)':<45}{bill.gst_amount:>18.2f}")
    out.append("-" * 66)
    out.append(f"{'GRAND TOTAL PAYABLE':<45}{'Rs. ' + f'{bill.grand_total:.2f}':>18}")
    out.append("=" * 66)
    return "\n".join(out)


def take_one_order(bases, pizzas, toppings):
    print("\n" + "#" * 66)
    print("NEW ORDER".center(66))
    print("#" * 66)

    name = prompt_until_valid("Enter customer name: ", validators.validate_name)
    phone = prompt_until_valid("Enter phone number: ", validators.validate_phone)

    base = choose_item("Choose Base:", bases)
    pizza = choose_item("Choose Pizza:", pizzas)
    topping = choose_item("Choose Topping:", toppings)

    quantity = prompt_until_valid(
        "Enter quantity (1-10): ", validators.validate_quantity
    )

    lines = [
        BillLine(label="Base", item_name=base.name, unit_price=base.price),
        BillLine(label="Pizza", item_name=pizza.name, unit_price=pizza.price),
        BillLine(label="Topping", item_name=topping.name, unit_price=topping.price),
    ]
    bill = compute_bill(lines, quantity)

    order_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + format_bill(name, phone, order_timestamp, lines, bill))

    print("\n1. Cash\n2. Card\n3. UPI")
    payment_choice = prompt_until_valid(
        "Select payment mode: ", validators.validate_payment_choice
    )
    payment_mode = PAYMENT_MODES[payment_choice]
    print(f"Payment confirmed: {payment_mode}")
    print("=" * 66)

    append_order(LOG_FILE, order_timestamp, name, phone, lines, bill, payment_mode)
    print("Order saved to orders_log.txt.")


def run_app():
    try:
        bases, pizzas, toppings = load_all_menus(BASE_FILE, PIZZA_FILE, TOPPING_FILE)
    except MenuLoadError as e:
        print(f"[Startup error] {e}")
        sys.exit(1)

    session_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Welcome to PizzaFlow!")
    print(f"Session started at {session_timestamp}")
    append_session_marker(LOG_FILE, session_timestamp)

    while True:
        take_one_order(bases, pizzas, toppings)
        again = validators.safe_input("\nStart another order? (y/n): ").strip().lower()
        if again != "y":
            break

    print("\nThank you for using PizzaFlow. Goodbye!")


def main():
    _force_utf8_console()
    try:
        run_app()
    except (EOFError, KeyboardInterrupt):
        print("\n[Session ended] Input stream closed or interrupted. Exiting PizzaFlow. Goodbye.")
        sys.exit(0)
    except Exception as exc:
        print(f"\n[Fatal error] PizzaFlow encountered an unexpected problem and must close: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
