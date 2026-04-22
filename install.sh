#!/bin/bash
# install.sh — ccplugin-telegram installer
set -e

PLUGIN_NAME="telegram-bridge"
INSTALL_DIR="$HOME/.claude/plugins/$PLUGIN_NAME"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🤖 ccplugin-telegram installer"
echo ""

# Secrets check
SECRETS_FILE="$HOME/Projects/claude-config/claude-secrets/secrets.env"
FALLBACK_SECRETS="$HOME/.claude/secrets/secrets.env"

has_token=false
for sf in "$SECRETS_FILE" "$FALLBACK_SECRETS"; do
  if [ -f "$sf" ] && grep -q "TELEGRAM_BOT_TOKEN" "$sf" 2>/dev/null; then
    has_token=true
    break
  fi
done

if ! $has_token; then
  echo "⚠️  TELEGRAM_BOT_TOKEN not found in secrets."
  echo "   Add to $FALLBACK_SECRETS:"
  echo "   export TELEGRAM_BOT_TOKEN=\"<your-token>\""
  echo "   export TELEGRAM_CHAT_ID=\"<your-chat-id>\""
  echo ""
  echo "   Get token: https://t.me/BotFather"
  echo "   Get chat ID: https://t.me/userinfobot"
  echo ""
fi

# Install files
echo "📁 Installing to $INSTALL_DIR"
mkdir -p "$INSTALL_DIR/skills/telegram-bridge" "$INSTALL_DIR/commands" "$INSTALL_DIR/.claude-plugin"

# Copy scripts
cp "$SCRIPT_DIR/telegram-poll.sh" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/tg_parse.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/tg_send.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/tg_voice.py" "$INSTALL_DIR/"
[ -f "$SCRIPT_DIR/telegram-ask.sh" ] && cp "$SCRIPT_DIR/telegram-ask.sh" "$INSTALL_DIR/"
[ -f "$SCRIPT_DIR/apple_speech.swift" ] && cp "$SCRIPT_DIR/apple_speech.swift" "$INSTALL_DIR/"

# Copy plugin metadata
cp "$SCRIPT_DIR/commands/tgbot.md" "$INSTALL_DIR/commands/"
cp "$SCRIPT_DIR/skills/telegram-bridge/SKILL.md" "$INSTALL_DIR/skills/telegram-bridge/"
cp "$SCRIPT_DIR/.claude-plugin/plugin.json" "$INSTALL_DIR/.claude-plugin/"

chmod +x "$INSTALL_DIR/telegram-poll.sh"
[ -f "$INSTALL_DIR/telegram-ask.sh" ] && chmod +x "$INSTALL_DIR/telegram-ask.sh"

# Watchdog dir
mkdir -p "$HOME/.watchdog"

echo ""
echo "✅ Installed! Next steps:"
echo "   1. Ensure TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID are in secrets"
echo "   2. Start bot: /tgbot start"
echo "   3. Message your bot on Telegram"
