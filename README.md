# telegram-bridge — Claude Code Plugin

by [Musab Kara](https://linkedin.com/in/musab-kara-85580612a) · [GitHub](https://github.com/SkyWalker2506)

Bidirectional Telegram bot for Claude Code. Control Claude from your phone — text, photos, documents, and voice (Whisper TR/EN).

## Quickstart (5 steps)

1. **Get credentials** — Create a bot at [@BotFather](https://t.me/BotFather), get your chat ID from [@userinfobot](https://t.me/userinfobot)

2. **Set secrets**
   ```bash
   echo 'export TELEGRAM_BOT_TOKEN="your-token"' >> ~/.claude/secrets/secrets.env
   echo 'export TELEGRAM_CHAT_ID="your-chat-id"' >> ~/.claude/secrets/secrets.env
   ```

3. **Install**
   ```bash
   git clone https://github.com/SkyWalker2506/ccplugin-telegram
   cd ccplugin-telegram && bash install.sh
   ```

4. **Start bot** (from Claude Code)
   ```
   /tgbot start
   ```

5. **Message your bot** — any free text is sent to Claude. Use `/help` for command list.

> Optional: Set `CLAUDE_TIMEOUT=600` in secrets for longer tasks.

## Commands

| Command | Description |
|---------|-------------|
| `/tgbot start` | Start the bot in background |
| `/tgbot stop` | Stop the bot |
| `/tgbot status` | Check if bot is running |

## Bot Commands (in Telegram)

| Command | Description |
|---------|-------------|
| `/run <task>` | Send task to Claude |
| `/status` | Current project + time |
| `/projects` | List ~/Projects |
| `/cd <name>` | Switch project |
| `/log` | Last 30 log lines |
| `/restart [project]` | Hot-restart bot |
| `/stop` | Stop the bot |
| Free text | Routed to Claude directly |

## Features

- Text, photos, documents → Claude executes / analyzes
- **Voice messages** → Whisper transcription (Apple Speech / whisper.cpp / OpenAI API) → Claude
- Inline keyboard buttons (Status, Projects, Log, Stop)
- Progress updates every 60s for long tasks
- Auth guard — ignores messages from unknown senders
- `telegram-ask.sh` — agentic wait-for-reply helper for unattended flows

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
