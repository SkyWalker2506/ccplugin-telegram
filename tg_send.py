#!/usr/bin/env python3
"""
tg_send.py — Send a text message to Telegram
Usage: python3 tg_send.py <BOT_TOKEN> <CHAT_ID> <TEXT> [KEYBOARD_JSON]

KEYBOARD_JSON: optional reply_markup JSON string (e.g. inline keyboard)
Text supports Markdown parse_mode.
Long messages (>4096 chars) are split automatically.
"""
import json
import sys
import urllib.request
import urllib.parse

MAX_LEN = 4096


def send_chunk(api: str, chat_id: str, text: str, keyboard: str = ""):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    if keyboard:
        try:
            payload["reply_markup"] = json.loads(keyboard)
        except Exception:
            pass

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{api}/sendMessage",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"send error: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 4:
        print("Usage: tg_send.py <TOKEN> <CHAT_ID> <TEXT> [KEYBOARD_JSON]", file=sys.stderr)
        sys.exit(1)

    token = sys.argv[1]
    chat_id = sys.argv[2]
    text = sys.argv[3]
    keyboard = sys.argv[4] if len(sys.argv) > 4 else ""

    api = f"https://api.telegram.org/bot{token}"

    # Split if too long
    chunks = [text[i:i + MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    for i, chunk in enumerate(chunks):
        kb = keyboard if i == len(chunks) - 1 else ""
        send_chunk(api, chat_id, chunk, kb)


if __name__ == "__main__":
    main()
