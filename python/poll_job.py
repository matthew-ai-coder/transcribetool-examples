import json
import os
import sys
import time
import urllib.request

API_BASE = os.environ.get("TRANSCRIBETOOL_BASE_URL", "https://transcribetool.com")
API_KEY = os.environ.get("TRANSCRIBETOOL_API_KEY")
JOB_TYPE = sys.argv[1] if len(sys.argv) > 1 else "transcript"
JOB_ID = sys.argv[2] if len(sys.argv) > 2 else None
INTERVAL_MS = int(sys.argv[3]) if len(sys.argv) > 3 else int(os.environ.get("TRANSCRIBETOOL_POLL_INTERVAL_MS", "10000"))
MAX_ATTEMPTS = int(sys.argv[4]) if len(sys.argv) > 4 else int(os.environ.get("TRANSCRIBETOOL_POLL_MAX_ATTEMPTS", "60"))

if not API_KEY:
    raise RuntimeError("Set TRANSCRIBETOOL_API_KEY")
if not JOB_ID:
    raise RuntimeError("Usage: python3 python/poll_job.py <transcript|batch> <job_id> [interval_ms] [max_attempts]")

path = f"/api/v1/batch-jobs/{JOB_ID}" if JOB_TYPE == "batch" else f"/api/v1/transcript-jobs/{JOB_ID}"
terminal_statuses = {"completed", "succeeded", "failed", "error", "cancelled"}
last_payload = None

for attempt in range(1, MAX_ATTEMPTS + 1):
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        headers={"x-api-key": API_KEY},
        method="GET",
    )
    with urllib.request.urlopen(req) as resp:
        text = resp.read().decode("utf-8")
    try:
        last_payload = json.loads(text)
    except json.JSONDecodeError:
        print(text)
        sys.exit(0)

    status = str(last_payload.get("status", "unknown"))
    print(json.dumps({"attempt": attempt, "status": status, "payload": last_payload}, indent=2))

    if status in terminal_statuses:
        sys.exit(1 if status in {"failed", "error", "cancelled"} else 0)

    if attempt < MAX_ATTEMPTS:
        time.sleep(INTERVAL_MS / 1000)

print(json.dumps({
    "error": "poll_timeout",
    "job_type": JOB_TYPE,
    "job_id": JOB_ID,
    "max_attempts": MAX_ATTEMPTS,
    "interval_ms": INTERVAL_MS,
    "last_payload": last_payload,
}, indent=2), file=sys.stderr)
sys.exit(1)
