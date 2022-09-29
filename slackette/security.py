from hashlib import sha256
from hmac import new as hmac
from typing import Any, Callable

from .types import Endpoint, RequestProtocol


class SlackHeaders(object):
    X_SLACK_SIGNATURE = "X-Slack-Signature"
    X_SLACK_REQUEST_TIMESTAMP = "X-Slack-Request-Timestamp"


class InvalidSignatureError(ValueError):
    pass


def compute_slack_signature(
    request: RequestProtocol,
    signing_secret: str,
    version: str,
) -> str:
    """Compute a Slack signature from the given request."""
    timestamp = request.headers.get(SlackHeaders.X_SLACK_REQUEST_TIMESTAMP)
    body = request.body()
    message = f"{version}:{timestamp}:{body}"
    signature = hmac(
        bytes(signing_secret, "latin-1"),
        msg=bytes(message, "latin-1"),
        digestmod=sha256,
    )
    return signature.hexdigest()


def SignedSlackRoute(
    signing_secret: str,
    version: str = "v0",
) -> Callable[[Endpoint], Endpoint]:
    """
    Decorator that acts as middleware to ensure that an
    incoming HTTP request is a valid issued Slack request.

    See https://api.slack.com/authentication/verifying-requests-from-slack
    """

    def wrapper(endpoint: Endpoint) -> Endpoint:
        def middleware(request: RequestProtocol) -> Any:
            expected = request.headers.get(SlackHeaders.X_SLACK_SIGNATURE)
            actual = compute_slack_signature(
                request,
                signing_secret,
                version,
            )
            if actual != expected:
                raise InvalidSignatureError()
            return endpoint(request)

        return middleware

    return wrapper
