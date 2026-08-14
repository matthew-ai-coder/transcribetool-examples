const API_BASE = process.env.TRANSCRIBETOOL_BASE_URL || "https://transcribetool.com";
const API_KEY = process.env.TRANSCRIBETOOL_API_KEY;
const transcriptId = process.argv[2];
const kind = process.argv[3] || "transcript_md";

if (!API_KEY) throw new Error("Set TRANSCRIBETOOL_API_KEY");
if (!transcriptId) throw new Error("Usage: node javascript/download-artifact.mjs <transcriptId> [kind]");

const response = await fetch(`${API_BASE}/api/v1/transcripts/${transcriptId}/downloads/${kind}`, {
  headers: { "x-api-key": API_KEY },
});

if (!response.ok) {
  console.error(await response.text());
  process.exit(1);
}

const text = await response.text();
console.log(text);
