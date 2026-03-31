import html
from pathlib import Path

import requests

USERNAME = "sabyasachisabs"
OUTPUT = Path("index.html")
PROFILE_PHOTO_URL = f"https://github.com/{USERNAME}.png"
PROFILE_NAME = "Nehal Solanki"
PROFILE_TAGLINE = "Aspiring Network Security Engineer | Security+ Certified | CCNA Candidate | IAM Experience"
PROFILE_LOCATION = "Randstad, Netherlands"
PROFILE_EMAIL = "Please connect via LinkedIn"
PROFILE_PHONE = "Available on request"
RESUME_LINK = "#"
LINKEDIN_URL = "https://www.linkedin.com/in/nehal-solanki"
TERMINAL_LINES = (
    "Initializing profile context...",
    "Loading security projects...",
    "Mapping certifications and experience timeline...",
    "Status: Online",
)

# Keep empty to include all repos for the selected profile.
ALLOWED_PREFIXES = ()

CERTIFICATIONS = (
    {
        "title": "CompTIA Security+ Certified",
        "issuer": "CompTIA",
        "year": "2025",
        "url": "#",
    },
    {
        "title": "A2/NT2 Nederlands Certified",
        "issuer": "NT2",
        "year": "N/A",
        "url": "#",
    },
    {
        "title": "B1 Nederlands",
        "issuer": "Dutch Language Certification",
        "year": "N/A",
        "url": "#",
    },
    {
        "title": "Deloitte Australia - Cyber Job Simulation",
        "issuer": "Deloitte Australia",
        "year": "N/A",
        "url": "#",
    },
    {
        "title": "Cybersecurity Compliance and Regulatory Essentials for GRC Analysts",
        "issuer": "Professional Training",
        "year": "N/A",
        "url": "#",
    },
    {
        "title": "Performing a Technical Security Audit and Assessment",
        "issuer": "Professional Training",
        "year": "N/A",
        "url": "#",
    },
)

ABOUT_ME = (
    "Security-focused IT professional with enterprise Identity and Access Management "
    "experience and a growing specialization in network and infrastructure security. "
    "Previously worked as an IT Security Administrator at Accenture, supporting "
    "large-scale access management environments. Currently focused on secure network "
    "engineering through hands-on labs in routing, VLAN segmentation, traffic control, "
    "and access control, with long-term interest in Network and Cloud Security roles."
)

SKILLS = (
    "Network Security",
    "Identity and Access Management (IAM)",
    "Access Governance",
    "VLAN Segmentation",
    "Routing and Switching",
    "Active Directory",
    "LDAP",
    "RSA Authentication Manager",
    "BMC Remedy (ITSM)",
    "UNIX Access Administration",
    "Security Audits",
)

TIMELINE = (
    {
        "year": "2024",
        "title": "Python for AI Intern",
        "org": "BlockVerse Institute (Netherlands)",
        "detail": "Completed internship focused on practical Python applications and structured technical learning.",
    },
    {
        "year": "2012-2013",
        "title": "IT Security Administrator - IAM",
        "org": "Accenture (via Qsource Consulting)",
        "detail": "Managed enterprise provisioning, account lifecycle, and access controls for SOX-sensitive systems.",
    },
    {
        "year": "2009-2010",
        "title": "Online Sales Support Specialist",
        "org": "Etech, Inc.",
        "detail": "Led customer support operations and process improvement with consistent quality focus.",
    },
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


def build_certification_cards() -> str:
    cards: list[str] = []
    for cert in CERTIFICATIONS:
        title = html.escape(cert["title"])
        issuer = html.escape(cert["issuer"])
        year = html.escape(cert["year"])
        url = html.escape(cert["url"])
        cards.append(
            f"""
        <article class="cert-card">
          <h3><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a></h3>
          <p>{issuer}</p>
          <span class="cert-year">{year}</span>
        </article>
        """.strip()
        )
    return "\n".join(cards)


def build_skill_badges(items: tuple[str, ...]) -> str:
    return "\n".join(f'<span class="skill-pill">{html.escape(item)}</span>' for item in items)


def build_terminal_lines(lines: tuple[str, ...]) -> str:
    return "\n".join(
        f'<p><span class="prompt">$</span> {html.escape(line)}</p>' for line in lines
    )


def build_timeline_items(items: tuple[dict, ...]) -> str:
    timeline_items: list[str] = []
    for item in items:
        year = html.escape(item["year"])
        title = html.escape(item["title"])
        org = html.escape(item["org"])
        detail = html.escape(item["detail"])
        timeline_items.append(
            f"""
        <article class="timeline-item">
          <div class="timeline-year">{year}</div>
          <div class="timeline-body">
            <h3>{title}</h3>
            <p class="timeline-org">{org}</p>
            <p>{detail}</p>
          </div>
        </article>
        """.strip()
        )
    return "\n".join(timeline_items)


def build_html(repos: list[dict]) -> str:
    cards = build_repo_cards(repos)
    cert_cards = build_certification_cards()
    skill_badges = build_skill_badges(SKILLS)
    terminal_lines = build_terminal_lines(TERMINAL_LINES)
    timeline_items = build_timeline_items(TIMELINE)
    safe_tagline = html.escape(PROFILE_TAGLINE)
    safe_location = html.escape(PROFILE_LOCATION)
    safe_email = html.escape(PROFILE_EMAIL)
    safe_phone = html.escape(PROFILE_PHONE)
    safe_resume = html.escape(RESUME_LINK)
    safe_linkedin = html.escape(LINKEDIN_URL)
    safe_photo = html.escape(PROFILE_PHOTO_URL)

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>sabyasachisabs | Portfolio</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="bg-grid" aria-hidden="true"></div>
    <main class="container">
      <header class="hero panel">
        <div class="hero-top">
          <img class="avatar" src="{safe_photo}" alt="{USERNAME} profile photo" />
          <div>
            <p class="kicker">CYBERSECURITY PORTFOLIO</p>
            <h1 class="glitch" data-text="{PROFILE_NAME}">{PROFILE_NAME}</h1>
            <p class="tagline">{safe_tagline}</p>
          </div>
        </div>
        <div class="hero-meta">
          <span>{safe_location}</span>
          <span>{safe_email}</span>
          <span>{safe_phone}</span>
        </div>
        <div class="hero-links">
          <a href="https://github.com/{USERNAME}" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="{safe_linkedin}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
          <a href="{safe_resume}" target="_blank" rel="noopener noreferrer">Resume</a>
        </div>
        <div class="terminal-box" aria-label="Profile status">
          {terminal_lines}
        </div>
      </header>

      <section class="section panel">
        <h2>Core Skills</h2>
        <div class="skills">{skill_badges}</div>
      </section>

      <section class="section panel">
        <h2>Certifications</h2>
        <div class="cert-grid">
          {cert_cards}
        </div>
      </section>

      <section class="section panel">
        <h2>About Me</h2>
        <p class="about-copy">{html.escape(ABOUT_ME)}</p>
      </section>

      <section class="section panel">
        <h2>Timeline</h2>
        <div class="timeline">
          {timeline_items}
        </div>
      </section>

      <section class="section panel">
        <h2>Projects</h2>
        <div class="grid">
        {cards}
        </div>
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
