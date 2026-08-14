const API_BASE = process.env.TRANSCRIBETOOL_BASE_URL || "https://transcribetool.com";
const API_KEY = process.env.TRANSCRIBETOOL_API_KEY;
const jobType = process.argv[2] || "transcript"; // transcript | batch
const jobId = process.argv[3];

if (!API_KEY) throw new Error("Set TRANSCRIBETOOL_API_KEY");
if (!jobId) throw new Error("Usage: node javascript/poll-job.mjs <transcript|batch> <jobId>");

const path = jobType === "batch"
  ? `/api/v1/batch-jobs/${jobId}`
  : `/api/v1/transcript-jobs/${jobId}`;

const response = await fetch(`${API_BASE}${path}`, {
  headers: { "x-api-key": API_KEY },
});

console.log(await response.text());
