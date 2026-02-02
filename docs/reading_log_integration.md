# Reading Log Integration

This repo updates the README reading list via a GitHub Action that pulls Markdown from the Reading Log Worker.

## Required GitHub Secret

Set the repository secret:
- `READING_LOG_MARKDOWN_URL` = `https://YOUR_WORKER_URL/reading/markdown?limit=5`

## Workflow

Workflow file: `.github/workflows/reading-log.yml`

It runs daily and on manual trigger. When the secret is set, it:
1. Fetches Markdown from the worker.
2. Replaces the block between `<!-- READING-LOG:START -->` and `<!-- READING-LOG:END -->`.
3. Commits the updated README.

## Local Update (optional)

```bash
export READING_LOG_MARKDOWN_URL="https://YOUR_WORKER_URL/reading/markdown?limit=5"
python scripts/update-reading-log.py
```
