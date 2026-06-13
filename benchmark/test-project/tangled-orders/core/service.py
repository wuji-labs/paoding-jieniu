"""OrderBillingService — the god object (軱). Everything depends on it.

It mixes three domains (orders, points, coupons) that have different natural
invariants. A structure-first agent should recognize this as the hard bone NOT
to cut first, and propose splitting along domain grain rather than editing it
in place.
"""


class OrderBillingService:
    def __init__(self):
        self._orders = {}
        self._points = {}      # mixed domain: points ledger
        self._coupons = {}     # mixed domain: coupon state machine

    def begin_tx(self):
        return {"ops": []}

    def commit(self, tx):
        for op in tx["ops"]:
            op()

    def validate_and_build(self, payload):
        if "user_id" not in payload:
            raise ValueError("user_id required")
        return {"id": payload.get("id", "o-1"), "user": payload["user_id"]}

    def insert_order(self, tx, order):
        tx["ops"].append(lambda: self._orders.__setitem__(order["id"], order))

    # --- mixed-in foreign domains below (should not live here) ---
    def accrue_points(self, user_id, amount):
        self._points[user_id] = self._points.get(user_id, 0) + amount

    def redeem_coupon(self, user_id, code):
        self._coupons[(user_id, code)] = "redeemed"
