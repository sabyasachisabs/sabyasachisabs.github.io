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
    ("3", "GitHub Projects"),
)

BEYOND_WORK_SUBTITLE = (
    "Outside of cybersecurity, simple things that keep me curious, calm, and continuously learning."
)

BEYOND_WORK_ITEMS = (
    {
        "title": "Avid Reader",
        "emoji": "📖",
        "body": (
            "I enjoy reading books that simplify complex ideas—from technology and cybersecurity, "
            "to personal growth and mindset."
        ),
        "image": (
            "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&q=80&auto=format&fit=crop"
        ),
    },
    {
        "title": "Plant Enthusiast",
        "emoji": "🌿",
        "body": (
            "I enjoy taking care of indoor plants—each one has its own personality, "
            "from low-maintenance to high-drama. My pothos is the extrovert; my snake plant keeps it calm."
        ),
        "image": (
            "https://images.unsplash.com/photo-1466692476869-aef1c0d316fc?w=800&q=80&auto=format&fit=crop"
        ),
    },
    {
        "title": "Curious Traveler",
        "emoji": "✈️",
        "body": (
            "I enjoy exploring cities across the Netherlands and Europe—experiencing culture, "
            "architecture, and everyday life."
        ),
        "image": (
            "https://images.unsplash.com/photo-1512470875652-21a62801adfe?w=800&q=80&auto=format&fit=crop"
        ),
    },
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


DIRECTORY_CATEGORY_ORDER = ("Networking", "Cybersecurity", "Python / AI", "Other")

EXTERNAL_LINK_SVG = (
    '<svg class="directory-open-icon" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true">'
    '<path fill="currentColor" fill-rule="evenodd" d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/>'
    '<path fill="currentColor" fill-rule="evenodd" d="M14.5 3a.5.5 0 0 1 0 1h-4.793l8.147 8.146a.5.5 0 0 1-.708.708L9 4.707V9.5a.5.5 0 0 1-1 0v-6a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 .5.5z"/>'
    "</svg>"
)


def _truncate_summary(text: str, max_len: int = 200) -> str:
    text = text.strip()
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def build_project_directory(repos: list[dict]) -> str:
    collected: list[dict] = []
    for repo in repos:
        name = repo.get("name", "")
        if not name or not repo_allowed(name):
            continue
        collected.append(repo)

    if not collected:
        return '<p class="empty">No matching repositories found yet.</p>'

    def sort_key(r: dict) -> tuple:
        cat = category_for_repo(r["name"])
        try:
            ci = DIRECTORY_CATEGORY_ORDER.index(cat)
        except ValueError:
            ci = 99
        return (ci, r["name"].lower())

    collected.sort(key=sort_key)

    rows: list[str] = []
    for repo in collected:
        name = repo["name"]
        raw_desc = (repo.get("description") or "").strip()
        summary = _truncate_summary(raw_desc)
        summary_cell = html.escape(summary) if summary else '<span class="directory-empty">—</span>'
        cat = category_for_repo(name)
        lang = repo.get("language") or ""
        lang_cell = html.escape(lang) if lang else '<span class="directory-empty">—</span>'
        stars = int(repo.get("stargazers_count") or 0)
        url = repo.get("html_url", "")
        safe_url = html.escape(url)
        safe_name = html.escape(name)
        safe_label = html.escape(f"Open {name} on GitHub")
        safe_cat = html.escape(cat)

        rows.append(
            f"""
        <tr class="directory-row">
          <th scope="row" class="directory-cell directory-cell-name">
            <a class="directory-project-link" href="{safe_url}" target="_blank" rel="noopener noreferrer">{safe_name}</a>
          </th>
          <td class="directory-cell directory-summary">{summary_cell}</td>
          <td class="directory-cell"><span class="directory-pill">{safe_cat}</span></td>
          <td class="directory-cell directory-lang">{lang_cell}</td>
          <td class="directory-cell directory-stars">{stars}</td>
          <td class="directory-cell directory-open">
            <a class="directory-open-link" href="{safe_url}" target="_blank" rel="noopener noreferrer" aria-label="{safe_label}">
              {EXTERNAL_LINK_SVG}
            </a>
          </td>
        </tr>
        """.strip()
        )

    n = len(collected)
    count_label = f"{n} listing" + ("s" if n != 1 else "")
    rows_html = "".join(rows)

    return f"""
    <div class="project-directory">
      <p class="directory-meta">{html.escape(count_label)}</p>
      <div class="directory-table-wrap">
        <table class="directory-table">
          <thead>
            <tr>
              <th scope="col">Project</th>
              <th scope="col">Summary</th>
              <th scope="col">Category</th>
              <th scope="col">Language</th>
              <th scope="col">Stars</th>
              <th scope="col"><span class="visually-hidden">Open repository</span></th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </div>
    </div>
    """


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


def initials_from_name(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper() if name else "?"


def build_beyond_work_cards(items: tuple[dict, ...]) -> str:
    cards: list[str] = []
    for item in items:
        title = html.escape(item["title"])
        emoji = html.escape(str(item.get("emoji") or ""))
        body = html.escape(item["body"])
        img_url = html.escape(item["image"])
        img_alt = html.escape(f"Illustration for {item['title']}")
        cards.append(
            f"""
        <article class="beyond-card">
          <div class="beyond-card-image-wrap">
            <img class="beyond-card-image" src="{img_url}" alt="{img_alt}" loading="lazy" width="400" height="220" />
          </div>
          <div class="beyond-card-body">
            <h3 class="beyond-card-title"><span class="beyond-card-emoji" aria-hidden="true">{emoji}</span> {title}</h3>
            <p class="beyond-card-text">{body}</p>
          </div>
        </article>
        """.strip()
        )
    return "\n".join(cards)


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


def build_html(repos: list[dict]) -> str:
    project_directory = build_project_directory(repos)
    beyond_cards = build_beyond_work_cards(BEYOND_WORK_ITEMS)
    cert_cards = build_certification_cards()
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
    safe_beyond_subtitle = html.escape(BEYOND_WORK_SUBTITLE)

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
        <a href="#beyond-work">Beyond Work</a>
        <a href="#portfolio">Portfolio</a>
        <a href="#certifications">Certifications</a>
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

      <section id="beyond-work" class="section section-beyond">
        <div class="section-head">
          <h2>Beyond Work</h2>
          <p>{safe_beyond_subtitle}</p>
        </div>
        <div class="beyond-grid">
          {beyond_cards}
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

      <section id="certifications" class="section">
        <div class="section-head">
          <h2>Certifications</h2>
          <p>Courses and trainings.</p>
        </div>
        <div class="cert-grid">
          {cert_cards}
        </div>
      </section>

      <section id="portfolio" class="section section-portfolio">
        <div class="section-head">
          <h2>Portfolio</h2>
          <p>Business directory of public GitHub repositories—sorted by category, then name.</p>
        </div>
        {project_directory}
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
