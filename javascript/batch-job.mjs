const API_BASE = process.env.TRANSCRIBETOOL_BASE_URL || "https://transcribetool.com";
const API_KEY = process.env.TRANSCRIBETOOL_API_KEY;

if (!API_KEY) {
  throw new Error("Set TRANSCRIBETOOL_API_KEY");
}

const inputText = process.argv[2] || "https://youtube.com/playlist?list=YOUR_PLAYLIST_ID";

const estimate = await fetch(`${API_BASE}/api/v1/batch-jobs/estimate`, {
  method: "POST",
  headers: {
    "x-api-key": API_KEY,
    "content-type": "application/json",
  },
  body: JSON.stringify({ input_text: inputText }),
});

console.log("ESTIMATE");
console.log(await estimate.text());

const submit = await fetch(`${API_BASE}/api/v1/batch-jobs`, {
  method: "POST",
  headers: {
    "x-api-key": API_KEY,
    "content-type": "application/json",
  },
  body: JSON.stringify({
    source_app: "github_example",
    input_text: inputText,
  }),
});

console.log("SUBMIT");
console.log(await submit.text());
