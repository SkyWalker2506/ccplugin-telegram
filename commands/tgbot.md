---
description: Start, stop, or check status of the Telegram bot bridge
argument-hint: [start|stop|status]
allowed-tools: [Bash]
---

# Telegram Bot Bridge

Manage the bidirectional Telegram ↔ Claude Code bridge.

## Usage

```
/tgbot start    — Start the bot (background)
/tgbot stop     — Stop the bot
/tgbot status   — Check if bot is running
```

## What this does

Based on `$ARGUMENTS`:

- **start**: Run `nohup bash ~/.claude/config/telegram-poll.sh ${PWD} > ~/.watchdog/telegram.log 2>&1 &` and confirm PID
- **stop**: Run `pkill -f telegram-poll.sh` and confirm
- **status**: Check `ps aux | grep telegram-poll | grep -v grep` and show last 3 lines of `~/.watchdog/telegram.log`
- **no argument**: Show status

Report the result clearly. If starting, mention the bot is now listening on Telegram.
If secrets are missing (`TELEGRAM_BOT_TOKEN` not set), instruct user to add them to `~/.claude/secrets/secrets.env`.
