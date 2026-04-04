# telegram-bridge — Claude Code Plugin

by [Musab Kara](https://linkedin.com/in/musab-kara-85580612a) · [GitHub](https://github.com/SkyWalker2506)

Bidirectional Telegram bot for Claude Code. Control Claude from your phone — text, photos, documents, and voice (Whisper TR/EN).

## Install

```bash
claude plugin install telegram-bridge@musabkara-claude-marketplace
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

- [claude-config](https://github.com/SkyWalker2506/claude-config) — Multi-Agent OS for Claude Code (110 agents, local-first routing)
- [Plugin Marketplace](https://github.com/SkyWalker2506/claude-marketplace) — Browse & install all 14 plugins
