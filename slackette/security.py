from hashlib import sha256
from hmac import new as hmac
from typing import Any, Callable, Mapping, Protocol, TypeVar, Union


class HeadersProtocol(Protocol):
    """ A headers provider interface for duck typing. """

    @property
    def headers(self) -> Mapping[str, Any]:
        ...

    def body(self) -> str:
        ...

Response = TypeVar("Response")
Endpoint = Callable[[HeadersProtocol], Response]


def SlackRequest(
    signing_secret: Union[bytes, str],
    version: str = "v0",
) -> Callable[[Endpoint], Endpoint]:
    """
    Decorator that acts as middleware to ensure that an
    incoming HTTP request is a valid issued Slack request.

    See https://api.slack.com/authentication/verifying-requests-from-slack
    """
    def wrapper(endpoint: Endpoint) -> Endpoint:
        def middleware(request: HeadersProtocol) -> Response:
            try:
                expected = request.headers.get("X-Slack-Signature")
                timestamp = request.headers.get("X-Slack-Request-Timestamp")
                body = request.body()
                message = bytes(f"{version}:{timestamp}:{body}")
                if isinstance(signing_secret, str):
                    signing_secret = bytes(signing_secret)
                signature = hmac(signing_secret, msg=message, digestmod=sha256)
                if signature.hexdigest() != expected:
                    raise ValueError("Invalid signature")
                return endpoint(request)
            except Exception as e:
                # TODO: log
                pass
        return middleware
    return wrapper
