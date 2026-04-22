#!/usr/bin/env python3
"""
tg_parse.py — Parse Telegram getUpdates JSON response
Output: TSV lines: TYPE\tUPDATE_ID\tFIELD1\tFIELD2
Types: MSG, CB, PHOTO, DOC, VOICE
Usage: echo <json> | python3 tg_parse.py <CHAT_ID>
"""
import json
import sys

CHAT_ID = sys.argv[1] if len(sys.argv) > 1 else ""


def out(*fields):
    print("\t".join(str(f) for f in fields))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    results = data.get("result", [])
    for upd in results:
        uid = upd.get("update_id", 0)

        # Callback query (inline keyboard button)
        if "callback_query" in upd:
            cq = upd["callback_query"]
            sender = str(cq.get("message", {}).get("chat", {}).get("id", ""))
            if CHAT_ID and sender != CHAT_ID:
                continue
            out("CB", uid, cq.get("id", ""), cq.get("data", ""))
            continue

        msg = upd.get("message", {})
        if not msg:
            continue

        chat_id = str(msg.get("chat", {}).get("id", ""))
        if CHAT_ID and chat_id != CHAT_ID:
            continue

        # Photo
        if "photo" in msg:
            photos = msg["photo"]
            file_id = photos[-1]["file_id"]  # largest size
            caption = msg.get("caption", "")
            out("PHOTO", uid, file_id, caption)
            continue

        # Document
        if "document" in msg:
            doc = msg["document"]
            file_id = doc.get("file_id", "")
            fname = doc.get("file_name", "document")
            caption = msg.get("caption", "")
            out("DOC", uid, file_id, f"{fname}|{caption}")
            continue

        # Voice
        if "voice" in msg:
            voice = msg["voice"]
            file_id = voice.get("file_id", "")
            duration = voice.get("duration", 0)
            out("VOICE", uid, file_id, str(duration))
            continue

        # Text
        text = msg.get("text", "")
        if text:
            out("MSG", uid, text, "")


if __name__ == "__main__":
    main()
