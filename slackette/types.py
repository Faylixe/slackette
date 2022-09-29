from typing import Any, Callable, Coroutine, Mapping, Protocol

from .blocks import Blocks


class HeadersProtocol(Protocol):
    """A headers provider interface for duck typing."""

    @property
    def headers(self) -> Mapping[str, Any]:
        ...

    def body(self) -> str:
        ...


Endpoint = Callable[[HeadersProtocol], Any]

AsyncWebhook = Callable[[Blocks], Coroutine[Any, Any, None]]
Webhook = Callable[[Blocks], None]
