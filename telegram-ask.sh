#!/bin/bash
# telegram-ask.sh — Send a question to Telegram, wait for reply
# Usage: bash telegram-ask.sh "Your question?" [timeout_seconds]
# Outputs the reply text to stdout; non-zero exit if timeout/error.
# Useful in agentic flows where Claude needs user input.

QUESTION="${1:?Usage: telegram-ask.sh <question> [timeout]}"
TIMEOUT="${2:-120}"

SECRETS_FILE="$HOME/Projects/claude-config/claude-secrets/secrets.env"
FALLBACK_SECRETS="$HOME/.claude/secrets/secrets.env"
set -a
[ -f "$SECRETS_FILE" ] && source "$SECRETS_FILE"
[ -z "$TELEGRAM_BOT_TOKEN" ] && [ -f "$FALLBACK_SECRETS" ] && source "$FALLBACK_SECRETS"
set +a

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
  echo "❌ TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set" >&2
  exit 1
fi

API="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Send the question
python3 "$SCRIPT_DIR/tg_send.py" "$TELEGRAM_BOT_TOKEN" "$TELEGRAM_CHAT_ID" \
  "❓ *Claude is asking:*
$QUESTION

_(Reply within ${TIMEOUT}s)_"

# Get current latest update_id to use as baseline
LATEST=$(curl -s "$API/getUpdates?offset=-1" | python3 -c "
import json,sys
r=json.load(sys.stdin).get('result',[])
print(r[-1]['update_id']+1 if r else 0)
" 2>/dev/null)
OFFSET="${LATEST:-0}"

DEADLINE=$((SECONDS + TIMEOUT))
while [ $SECONDS -lt $DEADLINE ]; do
  RESPONSE=$(curl -s --max-time 8 "$API/getUpdates?offset=$OFFSET&timeout=3&allowed_updates=message" 2>/dev/null)
  [ -z "$RESPONSE" ] && sleep 1 && continue

  RESULT=$(echo "$RESPONSE" | python3 -c "
import json,sys
data=json.load(sys.stdin)
results=data.get('result',[])
for upd in results:
    msg=upd.get('message',{})
    chat_id=str(msg.get('chat',{}).get('id',''))
    text=msg.get('text','')
    uid=upd.get('update_id',0)
    if chat_id=='$TELEGRAM_CHAT_ID' and text:
        print(uid+1)
        print(text)
        break
" 2>/dev/null)

  if [ -n "$RESULT" ]; then
    NEW_OFFSET=$(echo "$RESULT" | head -1)
    REPLY=$(echo "$RESULT" | tail -n +2)
    # Ack update
    curl -s "$API/getUpdates?offset=$NEW_OFFSET" -o /dev/null
    echo "$REPLY"
    exit 0
  fi

  sleep 2
done

echo "❌ No reply within ${TIMEOUT}s" >&2
exit 1
