import json
import os
import sys
import urllib.request

API_BASE = os.environ.get("TRANSCRIBETOOL_BASE_URL", "https://transcribetool.com")
API_KEY = os.environ.get("TRANSCRIBETOOL_API_KEY")

if not API_KEY:
    raise RuntimeError("Set TRANSCRIBETOOL_API_KEY")

source = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {
    "youtube_url": "https://www.youtube.com/watch?v=MNNfat_QP0E"
}

payload = json.dumps({
    "source": source,
    "source_app": "github_example",
    "modules": {
        "summary": True,
        "knowledge_extraction": True,
    },
    "billing": {
        "mode": "metered",
        "max_amount_usd": 2.0,
    },
}).encode("utf-8")

req = urllib.request.Request(
    f"{API_BASE}/api/v1/transcript-jobs",
    data=payload,
    headers={
        "x-api-key": API_KEY,
        "content-type": "application/json",
    },
    method="POST",
)

with urllib.request.urlopen(req) as resp:
    print(resp.read().decode("utf-8"))
