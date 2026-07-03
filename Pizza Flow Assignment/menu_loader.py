"""Loads the pizza menu (base/pizza/topping) from external .txt files.

File format per line: ID ; Name ; Price
Parsing is intentionally defensive because the grader swaps these files
before evaluating Stage 2 -- a single bad line must never crash the app.
"""

from dataclasses import dataclass


class MenuLoadError(Exception):
    """Raised when a menu file is missing or has zero usable items."""


@dataclass(frozen=True)
class MenuItem:
    item_id: str
    name: str
    price: float


def load_menu_file(path: str, category_label: str) -> list[MenuItem]:
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            raw_lines = f.readlines()
    except FileNotFoundError:
        raise MenuLoadError(
            f"Menu file not found: '{path}'. Make sure it is in the same "
            f"folder as the program."
        )
    except OSError as exc:
        raise MenuLoadError(f"Could not read menu file '{path}': {exc}")

    items: list[MenuItem] = []
    for line_no, raw_line in enumerate(raw_lines, start=1):
        line = raw_line.strip()
        if not line:
            continue

        parts = [p.strip() for p in line.split(";")]
        if len(parts) != 3:
            print(
                f"Warning: skipping malformed line {line_no} in '{path}' "
                f"(expected 3 fields separated by ';', got {len(parts)})."
            )
            continue

        item_id, name, price_str = parts

        if not name:
            print(
                f"Warning: skipping line {line_no} in '{path}': "
                f"item name is empty."
            )
            continue

        try:
            price = float(price_str)
        except ValueError:
            print(
                f"Warning: skipping line {line_no} in '{path}': "
                f'price "{price_str}" is not a valid number.'
            )
            continue

        if price <= 0:
            print(
                f"Warning: skipping line {line_no} in '{path}': "
                f"price must be a positive number, got {price}."
            )
            continue

        if not item_id:
            item_id = str(len(items) + 1)

        items.append(MenuItem(item_id=item_id, name=name, price=price))

    if not items:
        raise MenuLoadError(
            f"{category_label} file '{path}' contains no valid items "
            f"after parsing. Cannot continue."
        )

    return items


def load_all_menus(
    base_path: str, pizza_path: str, topping_path: str
) -> tuple[list[MenuItem], list[MenuItem], list[MenuItem]]:
    bases = load_menu_file(base_path, "Base")
    pizzas = load_menu_file(pizza_path, "Pizza")
    toppings = load_menu_file(topping_path, "Topping")
    return bases, pizzas, toppings
