from hashlib import sha256
from hmac import new as hmac
from typing import Any, Callable, Mapping, Protocol, TypeVar


class SlackHeaders(object):
    X_SLACK_SIGNATURE = "X-Slack-Signature"
    X_SLACK_REQUEST_TIMESTAMP = "X-Slack-Request-Timestamp"


class HeadersProtocol(Protocol):
    """ A headers provider interface for duck typing. """

    @property
    def headers(self) -> Mapping[str, Any]:
        ...

    def body(self) -> str:
        ...

Response = TypeVar("Response")
Endpoint = Callable[[HeadersProtocol], Response]


class InvalidSignatureError(ValueError):
    pass


def compute_slack_signature(
    protocol: HeadersProtocol,
    signing_secret: str,
    version: str,
) -> str:
    """
    """
    timestamp = protocol.headers.get(SlackHeaders.X_SLACK_REQUEST_TIMESTAMP)
    body = protocol.body()
    message = f"{version}:{timestamp}:{body}"
    signature = hmac(
        bytes(signing_secret),
        msg=bytes(message),
        digestmod=sha256,
    )
    return signature.hexdigest()


def SlackRequest(
    signing_secret: str,
    version: str = "v0",
) -> Callable[[Endpoint], Endpoint]:
    """
    Decorator that acts as middleware to ensure that an
    incoming HTTP request is a valid issued Slack request.

    See https://api.slack.com/authentication/verifying-requests-from-slack
    """
    def wrapper(endpoint: Endpoint) -> Endpoint:
        def middleware(protocol: HeadersProtocol) -> Any:
            try:
                expected = protocol.headers.get(SlackHeaders.X_SLACK_SIGNATURE)
                actual = compute_slack_signature(
                    protocol,
                    signing_secret,
                    version,
                )
                if actual != expected:
                    raise InvalidSignatureError()
                return endpoint(protocol)
            except Exception as e:
                # TODO: log
                pass
        return middleware
    return wrapper
