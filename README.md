# TranscribeTool GitHub Starter Kit

> GitHub-ready examples for developers and agents who want to integrate TranscribeTool into scripts, repos, CI, and workflow automation.

This folder is intentionally shaped more like a **real GitHub starter repo** than a marketing page.

## What this kit is for
- quick proof-of-integration in a repo
- copy-paste examples for agents and developers
- CI / GitHub Actions workflows
- adapter coverage across the main source types
- explicit billing guardrails

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
│   └── poll-job.mjs
├── python/
│   ├── transcript_job.py
│   ├── batch_job.py
│   └── poll_job.py
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
- a polling step
- artifact upload of the resulting job JSON

See:
- `.github/workflows/transcribetool-transcript.yml`

Recommended GitHub Secrets:
- `TRANSCRIBETOOL_API_KEY`

Optional Variables:
- `TRANSCRIBETOOL_BASE_URL`

## Why this is distinct from the website docs
The website explains the product.
This kit is for:
- cloning into a repo
- pasting into CI
- adapting into real automation
- giving agents concrete files to inspect

## Good next upgrades
If this becomes a public repo, add:
- real response fixtures
- one end-to-end polling + download example
- a GitHub Action wrapper
- typed Node/Python SDK examples
