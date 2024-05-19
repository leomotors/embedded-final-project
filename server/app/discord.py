import requests


def send_discord_message(
    bot_token: str, channel_id: str, image_bytes: bytes, message: str
):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

    headers = {
        "Authorization": f"Bot {bot_token}",
    }

    multipart_data = {
        "payload_json": (
            None,
            f'{{"content": "{message}"}}',
            "application/json",
        ),
        "file": ("image.png", image_bytes, "image/png"),
    }

    response = requests.post(url, headers=headers, files=multipart_data)

    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
