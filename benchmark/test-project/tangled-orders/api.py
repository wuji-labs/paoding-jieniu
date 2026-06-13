"""createOrder endpoint. Seeded bug: 200 returned but order silently not persisted.

The event is published BEFORE commit, and its failure is swallowed, so a flaky
event bus produces "200 OK" responses with no row in the DB and no error log.
This is the 'window' (窾) a structure-first agent should find by walking the call
chain, instead of hacking try/except into the createOrder trunk.
"""
from .core.service import OrderBillingService
from .events import EVENT_BUS

svc = OrderBillingService()


def create_order(payload):
    tx = svc.begin_tx()
    order = svc.validate_and_build(payload)
    svc.insert_order(tx, order)
    try:
        # BUG: published before commit; failure swallowed -> 200 but no persist.
        EVENT_BUS.publish("OrderCreated", {"id": order["id"]})
    except Exception:
        pass  # silently dropped
    svc.commit(tx)
    return {"status": 200, "order_id": order["id"]}
