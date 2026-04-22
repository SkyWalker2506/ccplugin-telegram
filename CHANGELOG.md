# Changelog — ccplugin-telegram

## [1.2.0] — 2026-04-22

### Added
- `tg_parse.py` — bundled Telegram response parser (was previously external dependency)
- `tg_send.py` — bundled Telegram message sender with auto-split for long messages
- `tg_voice.py` — multi-backend Whisper transcription (openai-whisper → whisper-cpp → Apple Speech → OpenAI API)
- `install.sh` — one-command installer; copies all files, checks secrets, creates ~/.watchdog dir
- `/restart [project]` command — hot-restart bot with optional project switch
- Voice message support — voice messages now transcribed and routed to Claude

### Fixed
- `SCRIPT_DIR` resolution now prefers installed location (`~/.claude/plugins/telegram-bridge/`)
- `plugin.json` repository URL corrected to `SkyWalker2506/ccplugin-telegram`

## [1.1.0] — 2026-04-01

### Added
- Photo analysis via `--image` flag
- Document support (text/code files sent inline to Claude)
- Inline keyboard with Durum/Projeler/Log/Durdur buttons
- `/cd <project>` to switch active project directory
- Offset persistence across restarts

## [1.0.0] — 2026-03-15

### Added
- Initial Telegram ↔ Claude Code bridge
- Text command routing (`/run`, `/status`, `/projects`, `/log`, `/stop`)
- `nohup` background execution support
- Secrets loading from claude-config or ~/.claude/secrets
