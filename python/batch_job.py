import json
import os
import sys
import urllib.request

API_BASE = os.environ.get("TRANSCRIBETOOL_BASE_URL", "https://transcribetool.com")
API_KEY = os.environ.get("TRANSCRIBETOOL_API_KEY")

if not API_KEY:
    raise RuntimeError("Set TRANSCRIBETOOL_API_KEY")

input_text = sys.argv[1] if len(sys.argv) > 1 else "https://youtube.com/playlist?list=YOUR_PLAYLIST_ID"

for path, payload in [
    ("/api/v1/batch-jobs/estimate", {"input_text": input_text}),
    ("/api/v1/batch-jobs", {"source_app": "github_example", "input_text": input_text}),
]:
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": API_KEY,
            "content-type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        print(path)
        print(resp.read().decode("utf-8"))
