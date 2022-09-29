from typing import Any, Callable, Coroutine, Mapping, Protocol

from .blocks import Blocks


class RequestProtocol(Protocol):
    """A headers provider interface for duck typing."""

    @property
    def headers(self) -> Mapping[str, Any]:
        ...

    def body(self) -> str:
        ...


Endpoint = Callable[[RequestProtocol], Any]

AsyncWebhook = Callable[[Blocks], Coroutine[Any, Any, None]]
Webhook = Callable[[Blocks], None]
