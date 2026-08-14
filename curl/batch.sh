#!/usr/bin/env bash
set -euo pipefail

API_BASE="${TRANSCRIBETOOL_BASE_URL:-https://transcribetool.com}"
API_KEY="${TRANSCRIBETOOL_API_KEY:?Set TRANSCRIBETOOL_API_KEY}"
INPUT_TEXT="${1:-https://youtube.com/playlist?list=YOUR_PLAYLIST_ID}"

printf '\n== Estimate ==\n'
curl -X POST "$API_BASE/api/v1/batch-jobs/estimate" \
  -H "x-api-key: $API_KEY" \
  -H "content-type: application/json" \
  -d "{\"input_text\": \"$INPUT_TEXT\"}"

printf '\n\n== Submit ==\n'
curl -X POST "$API_BASE/api/v1/batch-jobs" \
  -H "x-api-key: $API_KEY" \
  -H "content-type: application/json" \
  -d "{
    \"source_app\": \"github_example\",
    \"input_text\": \"$INPUT_TEXT\"
  }"
