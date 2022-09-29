from slackette import *

def test_block() -> None:
    print(Blocks(blocks=[
        Section(
            text=Markdown(text="linl"),
            accessory=Image(image_url="http://cover"),
        ),
        Actions(
            elements=[
                Button(
                    style=Style.primary,
                    text=PlainText(text="Approve"),
                    value="validate"
                ),
                Button(
                    style=Style.danger,
                    text=PlainText(text="Deny"),
                    value="deny"
                ),
            ]
        )
    ]).dict())
    assert False
