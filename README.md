# telegram-bridge — Claude Code Plugin

Bidirectional Telegram bot for Claude Code. Control Claude from your phone — text, photos, documents, and voice (Whisper TR/EN).

## Install

```bash
claude plugin install telegram-bridge@SkyWalker2506-claude-plugins
```

Or directly from this repo:
```bash
claude plugin marketplace add SkyWalker2506/ccplugin-telegram
claude plugin install telegram-bridge@SkyWalker2506-ccplugin-telegram
```

## Commands

| Command | Description |
|---------|-------------|
| `/tgbot start` | Start the bot in background |
| `/tgbot stop` | Stop the bot |
| `/tgbot status` | Check if bot is running |

## Setup

Add to `~/.claude/secrets/secrets.env`:
```
TELEGRAM_BOT_TOKEN=<from @BotFather>
TELEGRAM_CHAT_ID=<from @userinfobot>
```

## Features

- Text commands → Claude executes
- Photos → image analysis
- Documents → file processing
- Voice messages → Whisper transcription (TR/EN)
- Inline keyboard buttons (Status, Projects, Log, Stop)
- `/run <task>`, `/status`, `/projects`, `/cd`, `/log`, `/stop`

## Part of

[SkyWalker2506/claude-config](https://github.com/SkyWalker2506/claude-config) — Multi-Agent OS for Claude Code
