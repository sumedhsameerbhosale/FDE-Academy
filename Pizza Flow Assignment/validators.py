"""All customer-input validation for PizzaFlow.

Every validator returns (is_valid, value_or_None, error_message) so the
main loop can handle every field the same way via prompt_until_valid().
"""

import re

NAME_RE = re.compile(r"^[A-Za-z ]{2,40}$")
PHONE_RE = re.compile(r"^[6-9]\d{9}$")
INT_RE = re.compile(r"^-?\d+$")
DIGITS_RE = re.compile(r"^\d+$")


def safe_input(prompt: str) -> str:
    """Single choke point for all input() calls.

    Deliberately does NOT catch EOFError/KeyboardInterrupt -- those must
    propagate up to the one top-level handler in main.py so there is
    exactly one place deciding how a broken input stream is handled.
    """
    return input(prompt)


def validate_name(raw: str):
    candidate = raw.strip()
    if not candidate:
        return False, None, (
            "Name cannot be empty or just spaces. "
            "Please enter your name (letters and spaces only)."
        )
    if not NAME_RE.match(candidate):
        return False, None, (
            "Invalid name: only alphabets and spaces are allowed, "
            "length 2-40 characters. Please try again."
        )
    return True, candidate, ""


def validate_phone(raw: str):
    candidate = raw.strip()
    if not candidate:
        return False, None, "Phone number cannot be empty. Please enter a 10-digit number."
    if not candidate.isdigit():
        return False, None, (
            "Invalid phone number: must contain digits only "
            "(no spaces, dashes, or letters)."
        )
    if len(candidate) != 10:
        return False, None, (
            f"Invalid phone number: must be exactly 10 digits, "
            f"you entered {len(candidate)}."
        )
    if candidate[0] not in "6789":
        return False, None, "Invalid phone number: must start with 6, 7, 8, or 9."
    return True, candidate, ""


def validate_quantity(raw: str):
    candidate = raw.strip()
    if not candidate:
        return False, None, "Quantity cannot be empty. Please enter a whole number from 1 to 10."
    if not INT_RE.match(candidate):
        return False, None, (
            f'Invalid quantity: "{raw.strip()}" is not a whole number. '
            f"Please enter digits only (e.g. 3)."
        )
    value = int(candidate)
    if value <= 0:
        return False, None, f"Invalid quantity: {value} is not allowed. Quantity must be between 1 and 10."
    if value > 10:
        return False, None, f"Invalid quantity: {value} exceeds the maximum. Quantity must be between 1 and 10."
    return True, value, ""


def validate_menu_choice(raw: str, menu_length: int):
    candidate = raw.strip()
    if not candidate:
        return False, None, "No input entered. Please enter the item number from the list above."
    if not DIGITS_RE.match(candidate):
        return False, None, (
            f'Invalid selection: "{raw.strip()}" is not a valid item number. '
            f"Please enter digits only."
        )
    value = int(candidate)
    if value < 1 or value > menu_length:
        return False, None, (
            f"Invalid selection: {value} is out of range. "
            f"Please enter a number between 1 and {menu_length}."
        )
    return True, value - 1, ""


def validate_payment_choice(raw: str):
    candidate = raw.strip()
    if not candidate:
        return False, None, "No input entered. Please enter 1 for Cash, 2 for Card, or 3 for UPI."
    if not DIGITS_RE.match(candidate):
        return False, None, f'Invalid selection: "{raw.strip()}" is not valid. Please enter 1, 2, or 3.'
    value = int(candidate)
    if value not in (1, 2, 3):
        return False, None, f"Invalid selection: {value} is not a valid option. Please enter 1, 2, or 3."
    return True, value, ""
