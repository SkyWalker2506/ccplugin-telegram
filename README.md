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
- Inline keyboard buttons (Status, Projects, Log, Stop)
- `/run <task>`, `/status`, `/projects`, `/cd`, `/log`, `/stop`

## Architecture

```
Telegram → getUpdates polling → tg_parse.py → bash handler → claude -p → tg_send.py → Telegram
```

## Relation to ccplugin-notifications

`ccplugin-telegram` focuses on **bidirectional control** — run Claude from your phone.  
`ccplugin-notifications` focuses on **outbound notifications** — Claude notifies you.

## Part of

- [claude-config](https://github.com/SkyWalker2506/claude-config) — Multi-Agent OS for Claude Code (134 agents, local-first routing)
- [Plugin Marketplace](https://github.com/SkyWalker2506/claude-marketplace) — Browse & install all 18 plugins
- [ClaudeHQ](https://github.com/SkyWalker2506/ClaudeHQ) — Claude ecosystem HQ
