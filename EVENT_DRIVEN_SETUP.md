# Event-Driven Portfolio Updates

This setup updates your GitHub Pages portfolio repo whenever there is a push in your source repos.

## 1) Portfolio repo workflow

Already configured in this repo:

- `.github/workflows/update-portfolio.yml`
- Includes:
  - `repository_dispatch` trigger (`refresh-portfolio`)
  - hourly schedule fallback
  - manual run trigger

## 2) Create a token once

Create a GitHub personal access token (fine-grained preferred) that can dispatch events to:

- `sabyasachisabs/sabyasachisabs.github.io`

For fine-grained PAT:

- Repository access: only the portfolio repo
- Permissions: `Contents: Read and write` (or equivalent that allows repository dispatch API)

## 3) Add secret to every source repo

In each source repo (`Settings -> Secrets and variables -> Actions`), add:

- Name: `PORTFOLIO_TRIGGER_TOKEN`
- Value: your PAT

## 4) Add source repo workflow

Copy this file into each source repo as:

- `.github/workflows/notify-portfolio.yml`

Use the contents from:

- `.github/workflows/notify-portfolio-template.yml`

Adjust `branches` if your default branch differs.

## 5) Verify end-to-end

1. Push a test commit to a source repo.
2. Check Actions in the source repo (`Notify portfolio`) succeeds.
3. Check Actions in portfolio repo (`Update portfolio`) starts via `repository_dispatch`.
4. Confirm `index.html` commit appears and GitHub Pages redeploys.
