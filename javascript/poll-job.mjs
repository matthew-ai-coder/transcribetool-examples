const API_BASE = process.env.TRANSCRIBETOOL_BASE_URL || "https://transcribetool.com";
const API_KEY = process.env.TRANSCRIBETOOL_API_KEY;
const jobType = process.argv[2] || "transcript"; // transcript | batch
const jobId = process.argv[3];
const intervalMs = Number(process.argv[4] || process.env.TRANSCRIBETOOL_POLL_INTERVAL_MS || 10000);
const maxAttempts = Number(process.argv[5] || process.env.TRANSCRIBETOOL_POLL_MAX_ATTEMPTS || 60);

if (!API_KEY) throw new Error("Set TRANSCRIBETOOL_API_KEY");
if (!jobId) throw new Error("Usage: node javascript/poll-job.mjs <transcript|batch> <jobId> [intervalMs] [maxAttempts]");

const path = jobType === "batch"
  ? `/api/v1/batch-jobs/${jobId}`
  : `/api/v1/transcript-jobs/${jobId}`;

const terminalStatuses = new Set(["completed", "succeeded", "failed", "error", "cancelled"]);
let lastPayload = null;

for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "x-api-key": API_KEY },
  });
  const text = await response.text();
  try {
    lastPayload = JSON.parse(text);
  } catch {
    console.log(text);
    process.exit(response.ok ? 0 : 1);
  }

  const status = String(lastPayload.status || "unknown");
  const output = { attempt, status, payload: lastPayload };
  console.log(JSON.stringify(output, null, 2));

  if (terminalStatuses.has(status)) {
    process.exit(status === "failed" || status === "error" || status === "cancelled" ? 1 : 0);
  }

  if (attempt < maxAttempts) {
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
}

console.error(JSON.stringify({ error: "poll_timeout", jobType, jobId, maxAttempts, intervalMs, lastPayload }, null, 2));
process.exit(1);
