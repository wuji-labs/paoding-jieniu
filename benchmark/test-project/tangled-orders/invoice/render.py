"""Pure invoice renderer (窾 — the clean seam, the correct first cut).

No side effects, no I/O, no dependency on the god object. data dict -> html str.
This is the module a structure-first agent should extract first when asked to
'pull invoice generation out', because it can be isolated and tested trivially.
"""


def render_invoice(data: dict) -> str:
    lines = "".join(
        f"<tr><td>{item['name']}</td><td>{item['cents']}</td></tr>"
        for item in data.get("items", [])
    )
    return f"<table><caption>Invoice {data.get('id','?')}</caption>{lines}</table>"
