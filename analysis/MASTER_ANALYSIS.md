# MASTER_ANALYSIS — ccplugin-telegram

Date: 2026-04-22
Scope: Full plugin codebase audit post-v1.1.0

## Current footprint

- **Plugin:** `telegram-bridge` v1.1.0
- **Core file:** `telegram-poll.sh` — polling loop, message dispatch, Claude execution
- **Skill:** `skills/telegram-bridge/SKILL.md` — trigger definitions, capability docs
- **Command:** `commands/tgbot.md` — `/tgbot [start|stop|status]`
- **Helper scripts referenced (not in repo):** `tg_parse.py`, `tg_send.py`, `tg_voice.py` — expected at `~/.claude/config/`
- **No Python scripts in repo** — they live in claude-config, making this plugin incomplete as a standalone

## Architecture

```
Telegram → getUpdates polling → tg_parse.py → bash handler → claude -p → tg_send.py → Telegram
```

Secrets loaded from `~/Projects/claude-config/claude-secrets/secrets.env` (primary) or `~/.claude/secrets/secrets.env` (fallback).

## Weak-point inventory

### HIGH severity

- **W1 — Python helpers missing from repo.** `tg_parse.py`, `tg_send.py`, `tg_voice.py` referenced in `telegram-poll.sh` but not present in this repo. Plugin is non-functional as standalone install — these must be bundled.
- **W2 — Voice messages silently drop.** VOICE type received but message "henüz desteklenmiyor" — no Whisper path exists in the current shell script. `tg_voice.py` referenced in SKILL.md but never called.
- **W3 — No install.sh.** Unlike other ccplugins (voice-input, unity-craft), there is no `install.sh` that copies files and creates necessary dirs. Manual setup required.
- **W4 — SCRIPT_DIR hardcode fragility.** `telegram-poll.sh` uses `SCRIPT_DIR` to locate `tg_parse.py`/`tg_send.py` but these files must be co-located. If user installs via `~/.claude/plugins/`, path breaks.

### MEDIUM severity

- **W5 — Single-user CHAT_ID guard only.** No multi-user auth; anyone who gets the bot token can send commands. No rate limiting or allowlist.
- **W6 — `claude -p` timeout hardcoded at 300s.** Long tasks silently killed with no feedback to Telegram.
- **W7 — Offset file persistence.** `OFFSET_FILE` in `~/.watchdog/` — if dir missing, silent skip rather than graceful error.
- **W8 — Image `--image` flag fallback.** `claude -p --image` may not be supported in all Claude CLI versions; fallback exists but produces poor prompt.
- **W9 — No `/restart` command.** When bot hangs or `PROJECT_DIR` needs refresh, only way is SSH + pkill. Should have `/restart` command.

### LOW severity

- **W10 — README lacks quickstart** that actually works without reading claude-config.
- **W11 — plugin.json `repository` URL wrong** — points to `claude-plugins` but repo is `ccplugin-telegram`.
- **W12 — SKILL.md mentions `telegram-ask.sh`** for awaiting replies but this file doesn't exist in repo.
- **W13 — No CHANGELOG.** v1.1.0 shipped with no history of what changed from v1.0.0.

## New-area candidates

Ranked by user value / implementation effort:

1. **Bundle Python helpers into repo** — `tg_parse.py`, `tg_send.py`, `tg_voice.py` should live here. Unblocks standalone install. **Critical, low effort.**
2. **`install.sh`** — copies scripts to `~/.claude/plugins/telegram-bridge/`, wires secrets check. **High value, low effort.**
3. **Voice support via apple_speech or whisper-cpp** — call `tg_voice.py` (or shell-only Whisper) from VOICE branch. **High value, medium effort.**
4. **`/restart` command** — sends signal to reload PROJECT_DIR. **Medium value, low effort.**
5. **Rate-limit + auth guard** — reject messages from non-CHAT_ID senders with a warning. **Medium value, low effort.**
6. **Progress streaming** — send partial Claude output every 60s to avoid "is it dead?" confusion. **Medium value, medium effort.**
7. **`telegram-ask.sh`** — non-interactive wait-for-reply helper. **Medium value, medium effort.**

## 3-run plan

| Run | Addresses | Deliverable |
|-----|-----------|-------------|
| 1 | W1, W3, W4 | Bundle `tg_parse.py`, `tg_send.py`, `tg_voice.py`; add `install.sh`; fix SCRIPT_DIR resolution |
| 2 | W2, W9, W11, W12 | Wire voice support (Apple Speech); add `/restart`; fix plugin.json; add CHANGELOG |
| 3 | W5, W6, W7, W10 | Auth guard; configurable timeout; robust offset dir; polished README quickstart |
