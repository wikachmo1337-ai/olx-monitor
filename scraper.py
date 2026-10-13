name: scrape
on:
  schedule:
    - cron: "*/5 * * * *"
  workflow_dispatch:
permissions:
  contents: write
concurrency:
  group: scrape
  cancel-in-progress: false
jobs:
  run:
    runs-on: ubuntu-latest
    timeout-minutes: 9
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - name: Check OLX about every minute (4 cycles per job)
        run: |
          git config user.name "olx-bot"
          git config user.email "bot@users.noreply.github.com"
          for i in 1 2 3 4; do
            python scraper.py || true
            git add docs/data.json
            if ! git diff --staged --quiet; then
              git commit -qm "update $(date -u +%H:%M)"
              git pull --rebase -q || true
              git push -q || true
            fi
            if [ "$i" -lt 4 ]; then sleep 20; fi
          done
          exit 0
