import html
from pathlib import Path

import requests

USERNAME = "sabyasachisabs"
OUTPUT = Path("index.html")
SITE_BRAND = "Nehal Solanki Portfolio"
LOGO_LETTER = "N"
PROFILE_PHOTO_URL = ""
PROFILE_NAME = "Nehal Solanki"
PROFILE_LOCATION = "Randstad, Netherlands"
LINKEDIN_URL = "https://www.linkedin.com/in/nehal-solanki"
HERO_INTRO = (
    f"I'm {PROFILE_NAME.split()[0]}, a security-focused IT professional based in {PROFILE_LOCATION}. "
    "I combine enterprise Identity and Access Management experience with hands-on network security labs. "
    "I build clear, practical solutions and I'm open to Network, NOC, and entry-level security roles."
)
STATS = (
    ("10+", "Years"),
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
            "https://images.unsplash.com/photo-1592150621744-aca64f48394a?w=800&q=80&auto=format&fit=crop"
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
            "https://images.unsplash.com/photo-1512617835784-a92626c0a554?w=800&q=80&auto=format&fit=crop"
        ),
    },
)

WHERE_I_LIVE_IMAGE = "assets/where-i-live-den-haag.png"
WHERE_I_LIVE_CITY = "Den Haag, Netherlands"
WHERE_I_LIVE_BODY = (
    "I live in the international city of Den Haag, where history meets vibrant life. "
    "I bike along the canal-side paths, join in festivals, and meet people from all over the world "
    "in this dynamic, multicultural city by the sea."
)

# Keep empty to include all repos for the selected profile.
ALLOWED_PREFIXES = ()

TECHNICAL_CERTIFICATIONS = (
    {
        "title": "CompTIA Security+ Certified",
        "issuer": "CompTIA",
        "year": "2025",
        "url": "#",
    },
    {
        "title": "Deloitte Australia - Cyber Job Simulation",
        "issuer": "Deloitte Australia",
        "year": "",
        "url": "#",
    },
    {
        "title": "Cybersecurity Compliance and Regulatory Essentials for GRC Analysts",
        "issuer": "Professional Training",
        "year": "",
        "url": "#",
    },
    {
        "title": "Performing a Technical Security Audit and Assessment",
        "issuer": "Professional Training",
        "year": "",
        "url": "#",
    },
)

LANGUAGE_CERTIFICATIONS = (
    {
        "title": "A2/NT2 Nederlands Certified",
        "issuer": "NT2",
        "year": "",
        "url": "#",
    },
    {
        "title": "B1 Nederlands",
        "issuer": "Dutch Language Certification",
        "year": "",
        "url": "#",
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


def _cert_year_html(year_raw: str) -> str:
    y = (year_raw or "").strip()
    if not y or y.upper() == "N/A":
        return ""
    safe = html.escape(y)
    return f'<span class="cert-year">{safe}</span>'


def build_cert_cards_for(certs: tuple[dict, ...]) -> str:
    cards: list[str] = []
    for cert in certs:
        title = html.escape(cert["title"])
        issuer = html.escape(cert["issuer"])
        url = html.escape(cert["url"])
        year_block = _cert_year_html(str(cert.get("year", "")))
        cards.append(
            f"""
        <article class="cert-card">
          <h3><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a></h3>
          <p>{issuer}</p>
          {year_block}
        </article>
        """.strip()
        )
    return "\n".join(cards)


def build_certifications_section() -> str:
    tech_cards = build_cert_cards_for(TECHNICAL_CERTIFICATIONS)
    lang_cards = build_cert_cards_for(LANGUAGE_CERTIFICATIONS)
    return f"""
        <div class="cert-sections">
          <div class="cert-subsection">
            <h3 class="cert-subsection-title">Technical</h3>
            <div class="cert-grid">
              {tech_cards}
            </div>
          </div>
          <div class="cert-subsection">
            <h3 class="cert-subsection-title">Language</h3>
            <div class="cert-grid">
              {lang_cards}
            </div>
          </div>
        </div>
        """.strip()


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
    cards = build_repo_cards(repos)
    beyond_cards = build_beyond_work_cards(BEYOND_WORK_ITEMS)
    certifications_block = build_certifications_section()
    stat_cards = build_stat_cards(STATS)
    hero_visual = build_hero_image_block(
        PROFILE_PHOTO_URL,
        f"{PROFILE_NAME} portrait",
        initials_from_name(PROFILE_NAME),
    )
    safe_linkedin = html.escape(LINKEDIN_URL)
    safe_brand = html.escape(SITE_BRAND)
    safe_logo_letter = html.escape(LOGO_LETTER)
    safe_hero_intro = html.escape(HERO_INTRO)
    safe_first = html.escape(PROFILE_NAME.split()[0])
    safe_initials = html.escape(initials_from_name(PROFILE_NAME))
    safe_footer_name = html.escape(PROFILE_NAME.split()[0])
    safe_page_title = html.escape(f"{PROFILE_NAME} | Portfolio")
    safe_beyond_subtitle = html.escape(BEYOND_WORK_SUBTITLE)
    safe_where_img = html.escape(WHERE_I_LIVE_IMAGE)
    safe_where_city = html.escape(WHERE_I_LIVE_CITY)
    safe_where_body = html.escape(WHERE_I_LIVE_BODY)
    safe_where_alt = html.escape(
        "Den Haag (The Hague): Binnenhof and Hofvijver with the city skyline"
    )

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
        <a href="#beyond-work">Beyond Work</a>
        <a href="#where-i-live">Where I Live</a>
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

      <section id="where-i-live" class="section section-where">
        <h2 class="where-heading">Where I Live</h2>
        <div class="where-card">
          <div class="where-card-media">
            <img
              class="where-card-image"
              src="{safe_where_img}"
              alt="{safe_where_alt}"
              width="640"
              height="400"
              loading="lazy"
            />
          </div>
          <div class="where-card-body">
            <p class="where-location">
              <span class="where-flag" aria-hidden="true">🇳🇱</span>
              <strong>{safe_where_city}</strong>
            </p>
            <p class="where-description">{safe_where_body}</p>
          </div>
        </div>
      </section>

      <section id="certifications" class="section">
        <div class="section-head">
          <h2>Certifications</h2>
          <p>Courses and trainings—technical credentials and language proficiency.</p>
        </div>
        {certifications_block}
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
