const API_BASE = process.env.TRANSCRIBETOOL_BASE_URL || "https://transcribetool.com";
const API_KEY = process.env.TRANSCRIBETOOL_API_KEY;

if (!API_KEY) {
  throw new Error("Set TRANSCRIBETOOL_API_KEY");
}

const source = process.argv[2]
  ? JSON.parse(process.argv[2])
  : { youtube_url: "https://www.youtube.com/watch?v=MNNfat_QP0E" };

const response = await fetch(`${API_BASE}/api/v1/transcript-jobs`, {
  method: "POST",
  headers: {
    "x-api-key": API_KEY,
    "content-type": "application/json",
  },
  body: JSON.stringify({
    source,
    source_app: "github_example",
    modules: {
      summary: true,
      knowledge_extraction: true,
    },
    billing: {
      mode: "metered",
      max_amount_usd: 2.0,
    },
  }),
});

console.log(await response.text());
