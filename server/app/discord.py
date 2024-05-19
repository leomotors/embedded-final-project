import requests


def send_discord_message(bot_token: str, channel_id: str, image_bytes: bytes):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

    headers = {
        "Authorization": f"Bot {bot_token}",
    }

    files = {"file": ("image.png", image_bytes, "image/png")}

    response = requests.post(url, headers=headers, files=files)

    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
