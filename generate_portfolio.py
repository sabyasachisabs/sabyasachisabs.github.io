import html
from pathlib import Path

import requests

USERNAME = "sabyasachisabs"
OUTPUT = Path("index.html")

# Keep empty to include all repos for the selected profile.
ALLOWED_PREFIXES = (
    "v0-cybersecurity-cv",
    "dutchlingo-playground",
)


def repo_allowed(repo_name: str) -> bool:
    if not ALLOWED_PREFIXES:
        return True
    return any(repo_name.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def category_for_repo(repo_name: str) -> str:
    if repo_name.startswith("Network_Engineering_Labs"):
        return "Networking"
    if repo_name.startswith("Cybersecurity_Labs"):
        return "Cybersecurity"
    if repo_name.startswith("Python-for-AI-Labs"):
        return "Python / AI"
    return "Other"


def fetch_repos(username: str) -> list[dict]:
    url = f"https://api.github.com/users/{username}/repos"
    params = {
        "type": "owner",
        "sort": "updated",
        "per_page": 100,
    }
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def build_repo_cards(repos: list[dict]) -> str:
    cards: list[str] = []

    for repo in repos:
        name = repo.get("name", "")
        if not name or not repo_allowed(name):
            continue

        desc = html.escape(repo.get("description") or "No description provided.")
        repo_url = html.escape(repo.get("html_url", ""))
        language = html.escape(repo.get("language") or "N/A")
        stars = repo.get("stargazers_count", 0)
        category = html.escape(category_for_repo(name))
        safe_name = html.escape(name)

        cards.append(
            f"""
        <article class="repo-card">
          <h2><a href="{repo_url}" target="_blank" rel="noopener noreferrer">{safe_name}</a></h2>
          <p class="description">{desc}</p>
          <div class="meta">
            <span class="badge">{category}</span>
            <span>{language}</span>
            <span>★ {stars}</span>
          </div>
        </article>
        """.strip()
        )

    if not cards:
        return '<p class="empty">No matching repositories found yet.</p>'

    return "\n".join(cards)


def build_html(repos: list[dict]) -> str:
    cards = build_repo_cards(repos)

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>sabyasachisabs | Portfolio</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <main class="container">
      <header class="hero">
        <h1>sabyasachisabs</h1>
        <p>GitHub project portfolio.</p>
        <a href="https://github.com/{USERNAME}" target="_blank" rel="noopener noreferrer">
          GitHub Profile
        </a>
      </header>

      <section class="grid">
        {cards}
      </section>
    </main>
  </body>
</html>
"""


def main() -> None:
    repos = fetch_repos(USERNAME)
    content = build_html(repos)
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Generated {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()
