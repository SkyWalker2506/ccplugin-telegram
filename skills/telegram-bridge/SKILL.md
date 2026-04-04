---
name: telegram-bridge
description: This skill should be used when the user mentions "telegram", "tgbot", "bot", "mobile control", "remote access", asks to start/stop the bot, wants to send a Telegram notification, or needs to interact with Claude from their phone. Also activates when asking about voice transcription, Whisper, or Turkish voice commands.
version: 1.1.0
---

# Telegram Bridge Skill

Bidirectional Telegram bot integration for Claude Code.

## Capabilities

- **Text commands**: Send any task to Claude via Telegram
- **Photos**: Send images for analysis
- **Documents**: Send text/code files for processing
- **Voice**: TR/EN voice messages transcribed via Whisper
- **Inline keyboard**: Quick access buttons (Status, Projects, Log, Stop)

## Bot Commands

| Command | Description |
|---------|-------------|
| `/run <task>` | Execute a Claude task |
| `/status` | Show current project and time |
| `/projects` | List ~/Projects/ directories |
| `/cd <name>` | Switch active project |
| `/log` | Show last 30 log lines |
| `/stop` | Stop the bot |
| Free text | Directly sent to Claude as task |

## Setup Requirements

Add to `~/.claude/secrets/secrets.env`:
```
TELEGRAM_BOT_TOKEN=<your-bot-token>
TELEGRAM_CHAT_ID=<your-chat-id>
```

Get token from [@BotFather](https://t.me/BotFather), chat ID from [@userinfobot](https://t.me/userinfobot).

## Starting the Bot

```bash
/tgbot start
# or directly:
nohup bash ~/.claude/config/telegram-poll.sh ${PWD} > ~/.watchdog/telegram.log 2>&1 &
```

## Architecture

```
Telegram → getUpdates polling → tg_parse.py → bash handler → claude -p → tg_send.py → Telegram
```

- `telegram-poll.sh`: Main loop, handles all message types
- `tg_parse.py`: Parses Telegram API responses, handles UTF-8/emoji
- `tg_send.py`: Sends messages with optional inline keyboards
- `tg_voice.py`: Whisper transcription (openai-whisper → whisper.cpp → OpenAI API)

## When Absent

When the user is away and Claude needs input, use `telegram-ask.sh` to wait for a Telegram reply before proceeding.
