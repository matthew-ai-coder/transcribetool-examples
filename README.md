# TranscribeTool GitHub Starter Kit

> Production-oriented examples for integrating TranscribeTool into repositories, CI pipelines, scheduled workflows, and agent-driven media operations.

**Links**
- Product site: https://transcribetool.com/
- API overview: https://transcribetool.com/api
- GitHub examples page: https://transcribetool.com/github-examples

This repo is intentionally shaped like a **real GitHub starter surface**: clear environment setup, runnable scripts, polling utilities, artifact download flows, and a GitHub Actions workflow template.

## What this kit supports
- production-facing transcript job submission
- batch transcription workflows
- CI and GitHub Actions integration
- adapter coverage across the main source types
- explicit billing guardrails and operational clarity

## Included
```text
examples/github/
├── .env.example
├── .gitignore
├── .github/
│   └── workflows/
│       └── transcribetool-transcript.yml
├── curl/
│   ├── transcript-job.sh
│   └── batch.sh
├── javascript/
│   ├── transcript-job.mjs
│   ├── batch-job.mjs
│   ├── poll-job.mjs
│   └── download-artifact.mjs
├── python/
│   ├── transcript_job.py
│   ├── batch_job.py
│   ├── poll_job.py
│   └── download_artifact.py
└── README.md
```

## Quickstart
1. Copy `.env.example` to `.env`
2. Set `TRANSCRIBETOOL_API_KEY`
3. Run one example

### JavaScript
```bash
export TRANSCRIBETOOL_API_KEY=YOUR_API_KEY
node javascript/transcript-job.mjs '{"youtube_url":"https://www.youtube.com/watch?v=MNNfat_QP0E"}'
```

### Python
```bash
export TRANSCRIBETOOL_API_KEY=YOUR_API_KEY
python3 python/transcript_job.py '{"podcast_episode_url":"https://podcasts.apple.com/us/podcast/the-daily/id1200361736?i=1000720066149"}'
```

### Curl
```bash
export TRANSCRIBETOOL_API_KEY=YOUR_API_KEY
bash curl/transcript-job.sh '{"vimeo_url":"https://vimeo.com/76979871"}'
```

## Supported adapter shapes
### Single transcript jobs
- `youtube_url`
- `vimeo_url`
- `bilibili_url`
- `tiktok_url`
- `media_id`
- `podcast_episode_url`
- explicit podcast metadata:
  - `podcast_rss_url`
  - `podcast_audio_url`
  - `title`
  - `feed_title`
  - `published_at`

### Batch workflows
- YouTube videos / playlists / channels
- Vimeo video URLs
- Bilibili video URLs
- TikTok video URLs
- Apple and Spotify podcast URLs
- direct podcast RSS feeds
- `media_ids`
- `topic_request`

## Billing guardrail pattern
Use a spend cap in every integration:

```json
{
  "billing": {
    "mode": "metered",
    "max_amount_usd": 2.00
  }
}
```

Transcript work is billed **per second** and only **successfully completed transcript time** is charged.

## GitHub Actions usage
This starter kit includes:
- a workflow-dispatch example
- a transcript submit step
- polling until terminal state
- artifact upload of the resulting job JSON

See:
- `.github/workflows/transcribetool-transcript.yml`

Recommended GitHub Secrets:
- `TRANSCRIBETOOL_API_KEY`

Optional Variables:
- `TRANSCRIBETOOL_BASE_URL`

## Why this is distinct from the website docs
The website explains the product category and API surface.
This kit is for actual integration work:
- cloning into a repo
- wiring into CI
- adapting into scheduled or event-driven automation
- giving agents and developers concrete files to inspect and reuse

## Operational notes
- prefer async transcript and batch routes for long-running work
- keep `billing.max_amount_usd` explicit in production workflows
- poll until terminal state before downstream automation assumes completion
- download artifacts only after a successful terminal state
- treat these examples as starter integration patterns, then harden them for your own retry, alerting, and artifact-handling requirements

## Artifact download examples
### JavaScript
```bash
node javascript/download-artifact.mjs trn_your_transcript_id transcript_md
```

### Python
```bash
python3 python/download_artifact.py trn_your_transcript_id transcript_md
```

## Recommended next upgrades
- add real response fixtures
- add one end-to-end polling + download example
- add a reusable GitHub Action wrapper
- add typed Node and Python SDK examples
