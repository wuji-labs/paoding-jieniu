"""Out-of-tree verification that the seeded bug is real, single, and triggered.

Compares the system's invoice grand total against a reference computed with
the group-standard banker's rounding (ROUND_HALF_EVEN) that the code's own
docstrings claim to use. Any divergence is the bug.
"""
import sys
from decimal import Decimal, ROUND_HALF_EVEN
sys.path.insert(0, "test-project-large")

from app import Application
from domain.models import Customer
from domain.currency import DEFAULT_CONVERTER
from domain.discount import net_multiplier
from domain.tax import tax_rate
from util.money import to_minor, from_minor


def reference_invoice_total(order, customer):
    """Recompute with banker's rounding at every settlement boundary."""
    grand = 0
    for line in order.lines:
        extended = line.unit_price * Decimal(line.quantity)
        converted = DEFAULT_CONVERTER.convert(extended, line.currency, order.target_currency)
        discounted = converted * net_multiplier(order.discount_code)
        # settle net with banker's rounding (the stated standard)
        net = to_minor(
            discounted.quantize(Decimal(1).scaleb(-2), rounding=ROUND_HALF_EVEN),
            order.target_currency,
        )
        rate = tax_rate(customer.country, line.tax_category)
        raw_tax = from_minor(net, order.target_currency) * rate
        tax = to_minor(
            raw_tax.quantize(Decimal(1).scaleb(-2), rounding=ROUND_HALF_EVEN),
            order.target_currency,
        )
        grand += net + tax
    return grand


def run_case(name, lines, currency, discount, country):
    app = Application()
    app.seed_customer(Customer(id="c", name="t", country=country))
    o = app.order_api.create_order({
        "customer_id": "c", "target_currency": currency,
        "lines": lines, "discount_code": discount,
    })
    order = app.orders.get(o["id"])
    cust = app.customers.get("c")
    inv = app.invoice_api.create_invoice({"order_id": o["id"]})
    system_total = inv["grand_total"]["minor"]
    ref = reference_invoice_total(order, cust)
    delta = system_total - ref
    flag = "  <-- OFF BY ONE CENT" if delta != 0 else ""
    multi = len({app.orders.get(o["id"]).lines[i].currency for i in range(len(order.lines))} | {currency}) > 1
    print(f"{name:20s} system={system_total:6d} ref={ref:6d} delta={delta:+d} multi_ccy={multi}{flag}")
    return delta


cases = [
    ("gadget x1 EUR->USD", [{"sku": "SKU-GADGET", "quantity": 1}], "USD", None, "US"),
    ("gadget x2 EUR->USD", [{"sku": "SKU-GADGET", "quantity": 2}], "USD", None, "US"),
    ("gizmo  x1 GBP->USD", [{"sku": "SKU-GIZMO", "quantity": 1}], "USD", None, "US"),
    ("gizmo  x3 GBP->USD", [{"sku": "SKU-GIZMO", "quantity": 3}], "USD", None, "US"),
    ("doodad x1 CNY->USD", [{"sku": "SKU-DOODAD", "quantity": 1}], "USD", None, "US"),
    ("widget x1 USD->USD", [{"sku": "SKU-WIDGET", "quantity": 1}], "USD", None, "US"),
]
any_hit = False
for c in cases:
    if run_case(*c) != 0:
        any_hit = True

# brute search for a clean multi-currency off-by-one-cent case
print("\n--- brute search for a triggering order ---")
import itertools
skus = ["SKU-WIDGET", "SKU-GADGET", "SKU-GIZMO", "SKU-DOODAD"]
src_of = {"SKU-WIDGET":"USD","SKU-GADGET":"EUR","SKU-GIZMO":"GBP","SKU-DOODAD":"CNY"}
discounts = [None, "WELCOME10", "VIP15", "BLACKFRIDAY"]
found = []
for currency in ["USD", "EUR", "GBP", "CNY"]:
    for disc in discounts:
        for combo in itertools.product(range(0, 6), repeat=4):
            if sum(combo) == 0:
                continue
            lines = [{"sku": s, "quantity": q} for s, q in zip(skus, combo) if q]
            srcs = {src_of[s] for s,q in zip(skus,combo) if q}
            if len(srcs) < 2:
                continue
            app = Application()
            app.seed_customer(Customer(id="c", name="t", country="US"))
            try:
                o = app.order_api.create_order({"customer_id":"c","target_currency":currency,"lines":lines,"discount_code":disc})
            except Exception:
                continue
            order = app.orders.get(o["id"]); cust = app.customers.get("c")
            inv = app.invoice_api.create_invoice({"order_id": o["id"]})
            d = inv["grand_total"]["minor"] - reference_invoice_total(order, cust)
            if d != 0:
                found.append((currency, disc, lines, d))
print(f"triggering multi-currency orders found: {len(found)}")
for currency, disc, lines, d in found[:12]:
    desc = ",".join(f"{l['sku'].split('-')[1]}x{l['quantity']}" for l in lines)
    print(f"  target={currency} disc={disc} lines=[{desc}] delta={d:+d}")

print("\nBUG REPRODUCED" if (any_hit or found) else "\nNO DIVERGENCE - redesign needed")
