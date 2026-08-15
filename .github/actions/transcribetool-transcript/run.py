import json
import os
import time
import urllib.request
from pathlib import Path

API_BASE = "https://transcribetool.com/api/v1"
API_KEY = os.environ["TRANSCRIBETOOL_API_KEY"]
INPUT_JSON = json.loads(os.environ["TRANSCRIBETOOL_INPUT_JSON"])
ARTIFACT_KIND = os.environ.get("TRANSCRIBETOOL_ARTIFACT_KIND", "").strip()
POLL_INTERVAL = int(os.environ.get("TRANSCRIBETOOL_POLL_INTERVAL_SECONDS", "10"))
GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT")


def request_json(method: str, url: str, payload: dict | None = None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_file(url: str, dest: Path):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_KEY}"})
    with urllib.request.urlopen(req) as resp:
        dest.write_bytes(resp.read())


def write_output(name: str, value: str):
    if not GITHUB_OUTPUT:
        return
    with open(GITHUB_OUTPUT, "a", encoding="utf-8") as f:
        f.write(f"{name}={value}\n")


job = request_json("POST", f"{API_BASE}/transcript-jobs", INPUT_JSON)
job_id = job["job_id"]
status = job.get("status", "queued")
write_output("job_id", job_id)
print(f"Created job: {job_id}")

while status not in {"completed", "failed"}:
    time.sleep(POLL_INTERVAL)
    polled = request_json("GET", f"{API_BASE}/transcript-jobs/{job_id}")
    status = polled.get("status", status)
    print(f"Status: {status}")

write_output("status", status)
if status != "completed":
    raise SystemExit(f"Transcript job ended with status: {status}")

artifact_path = ""
if ARTIFACT_KIND:
    artifact_url = f"{API_BASE}/transcript-jobs/{job_id}/artifacts/{ARTIFACT_KIND}"
    out_dir = Path("transcribetool-artifacts")
    out_dir.mkdir(exist_ok=True)
    dest = out_dir / f"{job_id}-{ARTIFACT_KIND}"
    download_file(artifact_url, dest)
    artifact_path = str(dest)
    print(f"Downloaded artifact: {artifact_path}")

write_output("artifact_path", artifact_path)
