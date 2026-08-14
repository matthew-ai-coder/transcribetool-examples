#!/usr/bin/env bash
set -euo pipefail

API_BASE="${TRANSCRIBETOOL_BASE_URL:-https://transcribetool.com}"
API_KEY="${TRANSCRIBETOOL_API_KEY:?Set TRANSCRIBETOOL_API_KEY}"
SOURCE_JSON="${1:-{\"youtube_url\":\"https://www.youtube.com/watch?v=MNNfat_QP0E\"}}"

curl -X POST "$API_BASE/api/v1/transcript-jobs" \
  -H "x-api-key: $API_KEY" \
  -H "content-type: application/json" \
  -d "{
    \"source\": $SOURCE_JSON,
    \"source_app\": \"github_example\",
    \"modules\": {
      \"summary\": true,
      \"knowledge_extraction\": true
    },
    \"billing\": {
      \"mode\": \"metered\",
      \"max_amount_usd\": 2.00
    }
  }"
