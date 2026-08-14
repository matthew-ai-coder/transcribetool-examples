import os
import sys
import urllib.request

API_BASE = os.environ.get("TRANSCRIBETOOL_BASE_URL", "https://transcribetool.com")
API_KEY = os.environ.get("TRANSCRIBETOOL_API_KEY")
TRANSCRIPT_ID = sys.argv[1] if len(sys.argv) > 1 else None
KIND = sys.argv[2] if len(sys.argv) > 2 else "transcript_md"

if not API_KEY:
    raise RuntimeError("Set TRANSCRIBETOOL_API_KEY")
if not TRANSCRIPT_ID:
    raise RuntimeError("Usage: python3 python/download_artifact.py <transcript_id> [kind]")

req = urllib.request.Request(
    f"{API_BASE}/api/v1/transcripts/{TRANSCRIPT_ID}/downloads/{KIND}",
    headers={"x-api-key": API_KEY},
    method="GET",
)

with urllib.request.urlopen(req) as resp:
    print(resp.read().decode("utf-8"))
