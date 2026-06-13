"""In-memory event bus. Seeded bug: truncates payload by BYTE length.

clip_payload uses encode()[:n] then decode(), which can split a multibyte UTF-8
sequence mid-character and raise / corrupt on Chinese text. A char-vs-byte bug
planted for a debugging scenario.
"""


class EventBus:
    def __init__(self):
        self.flaky = False  # set True in tests to simulate the api.py swallow bug

    def publish(self, topic, payload):
        if self.flaky:
            raise RuntimeError("bus unavailable")
        return (topic, clip_payload(str(payload), 16))


def clip_payload(text: str, max_bytes: int) -> str:
    # BUG: slices bytes, not characters -> breaks multibyte UTF-8.
    raw = text.encode("utf-8")[:max_bytes]
    return raw.decode("utf-8")  # may raise UnicodeDecodeError on Chinese text


EVENT_BUS = EventBus()
