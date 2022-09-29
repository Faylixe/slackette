# Slackette

Slackette is a modern small tooklit for building Slack applications


## Examples

### Use webhook to publish BlockKit messages

```python
from slackette import SlackWebhook
from slackette.blocks import *

webhook = SlackWebhook("YOUR SLACK WEBHOOK")
webhook(
    Blocks(
        blocks=[
            Section(
                text=Markdown(text="**hello**"),
            )
        ]
    )
)
```

### Implement a interactive callback with FastAPI

```python
from fastapi import FastAPI, Request
from pydantic import BaseSettings
from slackette.security import SlackRequest


class Settings(BaseSettings):
    SLACK_SIGNING_SECRET: str


settings = Settings()
api = FastAPI()

@api.post("/slack")
@SlackRequest(signing_secret=settings.SLACK_SIGNING_SECRET)
def on_interactive_event(request: Request) -> None:
    ...
```