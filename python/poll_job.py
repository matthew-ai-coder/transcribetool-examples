import os
import sys
import urllib.request

API_BASE = os.environ.get("TRANSCRIBETOOL_BASE_URL", "https://transcribetool.com")
API_KEY = os.environ.get("TRANSCRIBETOOL_API_KEY")
JOB_TYPE = sys.argv[1] if len(sys.argv) > 1 else "transcript"
JOB_ID = sys.argv[2] if len(sys.argv) > 2 else None

if not API_KEY:
    raise RuntimeError("Set TRANSCRIBETOOL_API_KEY")
if not JOB_ID:
    raise RuntimeError("Usage: python3 python/poll_job.py <transcript|batch> <job_id>")

path = f"/api/v1/batch-jobs/{JOB_ID}" if JOB_TYPE == "batch" else f"/api/v1/transcript-jobs/{JOB_ID}"
req = urllib.request.Request(
    f"{API_BASE}{path}",
    headers={"x-api-key": API_KEY},
    method="GET",
)

with urllib.request.urlopen(req) as resp:
    print(resp.read().decode("utf-8"))
