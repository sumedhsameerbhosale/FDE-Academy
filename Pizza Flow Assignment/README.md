# PizzaFlow — Stage 2 Working MVP

Console-based pizza ordering system that replaces Rajan's Google Form.
Loads menu items from 3 external `.txt` files at runtime (never
hardcoded), validates all customer input, computes a GST-inclusive bill
with a bulk discount, and logs every completed order.

## How to run

```
cd pizzaflow-stage2
python main.py
```

Requires Python 3.10+ (tested on Python 3.13, Windows / Git Bash / PowerShell).

## Files

- `main.py` — orchestration / CLI flow, top-level error handling
- `menu_loader.py` — reads and defensively validates the 3 menu `.txt` files
- `validators.py` — all input validation (name, phone, quantity, menu choice, payment choice)
- `billing.py` — pure pricing/discount/GST math, no I/O
- `logger.py` — appends completed orders to `orders_log.txt`
- `Types_of_Base.txt` / `Types_of_Pizza.txt` / `Types_of_Toppings.txt` — menu data
- `orders_log.txt` — sample log, pre-seeded with 2 completed orders

## Architecture

`main.py` loads the menu, then repeatedly takes one order at a time
(customer intake → menu selection → quantity → bill → payment → log).
`menu_loader.py` and `billing.py` have no dependency on each other or on
I/O beyond menu_loader's own file reads. `validators.py` functions are
pure — each returns `(is_valid, value_or_None, error_message)` so
`main.py`'s single `prompt_until_valid()` loop can re-prompt uniformly
for every field. `logger.py` is the only module that touches
`orders_log.txt`.

## Windows / UTF-8 safety

Console streams are reconfigured to UTF-8 with `errors="replace"` at
startup so no non-ASCII text can ever raise `UnicodeEncodeError`,
regardless of the system codepage. All file I/O uses explicit
`encoding="utf-8"` (menu files are read as `utf-8-sig` to tolerate a
Notepad-added BOM). The bill and log additionally use the literal
`Rs.` currency notation rather than `₹`, avoiding that whole class of
console-encoding risk on the highest-visibility output.

## Crash safety

`EOFError` and `KeyboardInterrupt` (e.g. piped stdin running out, or
Ctrl+C) are caught once at the top level in `main()` and produce a
clean exit message — never a traceback. Any other unexpected exception
is also caught at this same boundary as a last resort.

## Edge cases handled

| # | Case | Where handled | Result |
|---|------|---------------|--------|
| 1 | Name with only spaces | `validate_name` strips first, so spaces-only → empty | "Name cannot be empty or just spaces..." → re-prompt |
| 2 | Phone starting with 1 | `validate_phone` first-digit check | "...must start with 6, 7, 8, or 9." → re-prompt |
| 3 | Quantity 0 and 11 | `validate_quantity` range checks | Specific "not allowed" / "exceeds the maximum" messages → re-prompt |
| 4 | Item selection 0 or > menu length | `validate_menu_choice` range check | "...is out of range..." → re-prompt |
| 5 | Price number instead of item number | `validate_menu_choice` digits/range checks | Non-digit price (e.g. "59.00") → "not a valid item number"; bare out-of-range integer → "out of range" — always a specific message, never a crash |
| 6 | Empty input at every prompt | Every validator's leading empty-check | Field-specific "cannot be empty" message → re-prompt |
| 7 | Non-integer quantity ("three", "2.5") | `validate_quantity` regex `^-?\d+$` rejects both | "...is not a whole number..." → re-prompt |
| 8 | Menu file with missing price field | `menu_loader.load_menu_file` line parsing | Bad line skipped with a warning; if a whole file ends up empty, clean `MenuLoadError` → exit(1), no traceback |

## Known simplifications (Stage 2 scope)

No database, no web UI, no persistence beyond the flat `orders_log.txt`
file — those are Stage 3 scope per the assignment brief.
