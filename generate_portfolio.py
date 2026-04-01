import html
from pathlib import Path

import requests

USERNAME = "sabyasachisabs"
OUTPUT = Path("index.html")
SITE_BRAND = "Portfolio"
LOGO_LETTER = "N"
PROFILE_PHOTO_URL = ""
PROFILE_NAME = "Nehal Solanki"
PROFILE_TAGLINE = "Aspiring Network Security Engineer | Security+ Certified | CCNA Candidate | IAM Experience"
PROFILE_LOCATION = "Randstad, Netherlands"
PROFILE_EMAIL = "Please connect via LinkedIn"
PROFILE_PHONE = "Available on request"
RESUME_LINK = "#"
LINKEDIN_URL = "https://www.linkedin.com/in/nehal-solanki"
ABOUT_HEADLINE = "Security-focused network and IAM professional"
HERO_INTRO = (
    f"I'm {PROFILE_NAME.split()[0]}, a security-focused IT professional based in {PROFILE_LOCATION}. "
    "I combine enterprise Identity and Access Management experience with hands-on network security labs. "
    "I build clear, practical solutions and I'm open to Network, NOC, and entry-level security roles."
)
STATS = (
    ("10+", "Years in IT"),
    ("6+", "Certifications"),
    ("2", "GitHub Projects"),
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


def initials_from_name(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper() if name else "?"


def build_stat_cards(stats: tuple[tuple[str, str], ...]) -> str:
    cards: list[str] = []
    for value, label in stats:
        cards.append(
            f"""
        <div class="stat-card">
          <span class="stat-value">{html.escape(value)}</span>
          <span class="stat-label">{html.escape(label)}</span>
        </div>
        """.strip()
        )
    return "\n".join(cards)


def build_hero_image_block(photo_url: str, alt: str, initials: str) -> str:
    if photo_url.strip():
        safe_url = html.escape(photo_url)
        safe_alt = html.escape(alt)
        return f"""
        <div class="hero-image-wrap">
          <img src="{safe_url}" alt="{safe_alt}" width="420" height="525" />
        </div>
        """.strip()
    safe_initials = html.escape(initials)
    return f"""
        <div class="hero-image-wrap" aria-hidden="true">
          <div class="hero-placeholder">{safe_initials}</div>
        </div>
        """.strip()


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
    timeline_items = build_timeline_items(TIMELINE)
    stat_cards = build_stat_cards(STATS)
    hero_visual = build_hero_image_block(
        PROFILE_PHOTO_URL,
        f"{PROFILE_NAME} portrait",
        initials_from_name(PROFILE_NAME),
    )
    safe_tagline = html.escape(PROFILE_TAGLINE)
    safe_location = html.escape(PROFILE_LOCATION)
    safe_email = html.escape(PROFILE_EMAIL)
    safe_phone = html.escape(PROFILE_PHONE)
    safe_resume = html.escape(RESUME_LINK)
    safe_linkedin = html.escape(LINKEDIN_URL)
    safe_brand = html.escape(SITE_BRAND)
    safe_logo_letter = html.escape(LOGO_LETTER)
    safe_hero_intro = html.escape(HERO_INTRO)
    safe_about_headline = html.escape(ABOUT_HEADLINE)
    safe_first = html.escape(PROFILE_NAME.split()[0])
    safe_initials = html.escape(initials_from_name(PROFILE_NAME))
    safe_footer_name = html.escape(PROFILE_NAME.split()[0])
    safe_page_title = html.escape(f"{PROFILE_NAME} | Portfolio")

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{safe_page_title}</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="page-bg" aria-hidden="true"></div>
    <header class="site-header">
      <a class="logo" href="#home">
        <span class="logo-mark">{safe_logo_letter}</span>
        {safe_brand}
      </a>
      <nav class="nav" aria-label="Primary">
        <a href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#skills">Skills</a>
        <a href="#portfolio">Portfolio</a>
        <a href="#certifications">Certifications</a>
        <a href="#timeline">Experience</a>
      </nav>
      <a class="btn-contact" href="{safe_linkedin}" target="_blank" rel="noopener noreferrer">Contact</a>
    </header>

    <main class="container">
      <section id="home" class="hero">
        <div class="hero-inner">
          <div class="hero-copy">
            <h1>Hello, I'm {safe_first}</h1>
            <p class="hero-lead">{safe_hero_intro}</p>
            <a class="btn-primary" href="{safe_linkedin}" target="_blank" rel="noopener noreferrer">Say Hello!</a>
          </div>
          <div class="hero-visual">
            {hero_visual}
          </div>
        </div>
        <div class="hero-stats">
          {stat_cards}
        </div>
      </section>

      <section id="about" class="about-card">
        <div class="about-thumb" aria-hidden="true">{safe_initials}</div>
        <div>
          <h2>{safe_about_headline}</h2>
          <p class="about-copy">{html.escape(ABOUT_ME)}</p>
          <p class="about-tagline"><strong>{safe_tagline}</strong></p>
          <p class="about-meta">{safe_location} · {safe_email} · {safe_phone}</p>
          <p class="about-links">
            <a href="https://github.com/{USERNAME}" target="_blank" rel="noopener noreferrer">GitHub</a>
            <span class="about-sep">·</span>
            <a href="{safe_linkedin}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
            <span class="about-sep">·</span>
            <a href="{safe_resume}">Resume</a>
          </p>
        </div>
      </section>

      <section id="skills" class="section">
        <div class="section-head">
          <h2>Core Skills</h2>
          <p>Tools and domains I work with.</p>
        </div>
        <div class="skills">{skill_badges}</div>
      </section>

      <section id="certifications" class="section">
        <div class="section-head">
          <h2>Certifications</h2>
          <p>Credentials and training.</p>
        </div>
        <div class="cert-grid">
          {cert_cards}
        </div>
      </section>

      <section id="timeline" class="section">
        <div class="section-head">
          <h2>Experience</h2>
          <p>Selected roles and milestones.</p>
        </div>
        <div class="timeline">
          {timeline_items}
        </div>
      </section>

      <section id="portfolio" class="section">
        <div class="section-head">
          <h2>Projects</h2>
          <p>Repositories from my GitHub profile.</p>
        </div>
        <div class="grid">
        {cards}
        </div>
      </section>
    </main>
    <footer class="site-footer">
      <p>© {safe_footer_name} · Built with GitHub Pages</p>
    </footer>
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
