# Builds getsobat.in/blog/ and sitemap.xml from posts_rules.py + posts.py.
# Run from the repo root: python3 tools/blog/build.py .
# The output is plain static HTML, committed like every other page. To add a
# post, add a dict to posts.py (or posts_rules.py for anything citing rules
# or prices, with its sources), set DATE, run this, and commit.
import html, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from posts_rules import POSTS as RULES
from posts import POSTS as EVERGREEN

SITE = "https://getsobat.in"
DATE, DATE_LABEL = "2026-10-25", "25 October 2026"
OUT = sys.argv[1]
posts = RULES + EVERGREEN
assert len({p["slug"] for p in posts}) == len(posts), "duplicate slug"
by_slug = {p["slug"]: p for p in posts}

TILE = '<span class="brand-tile"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M18 45 C 32 45, 32 19, 46 19" stroke="#FFFFFF" stroke-width="6.5" fill="none" stroke-linecap="round"/><circle cx="18" cy="45" r="6.6" fill="#FFFFFF"/><circle cx="46" cy="19" r="6.6" fill="#FFB23E"/></svg></span>'

def esc(s): return html.escape(s, quote=True)

def minutes(body):
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return max(2, math.ceil(words / 200))

def head(title, desc, url, og_type, ld):
    return f"""<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{url}">
  <meta property="og:site_name" content="Sobat">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="en_IN">
  <meta property="og:image" content="{SITE}/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{SITE}/assets/og-image.png">
  <meta name="theme-color" content="#F5F4FA">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-192.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/site.css">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="/" aria-label="Sobat home">
        {TILE}
        <span class="brand-word">sobat</span>
      </a>
      <nav class="site-nav" aria-label="Main">
        <a href="/#how">How it works</a>
        <a href="/blog/">Blog</a>
        <a href="/#faq">FAQ</a>
      </nav>
      <a class="button small" href="/app/">Open the app</a>
    </div>
  </header>
"""

FOOT = f"""
  <footer class="site-footer">
    <div class="container">
      <span class="footer-brand">{TILE}© 2026 Sobat · India</span>
      <nav aria-label="Footer">
        <a href="/app/">Open the app</a>
        <a href="/blog/">Blog</a>
        <a href="/privacy.html">Privacy</a>
        <a href="/terms.html">Terms</a>
        <a href="/delete-account.html">Delete account</a>
        <span>hello@getsobat.in</span>
      </nav>
    </div>
  </footer>
</body>
</html>
"""

CTA = """
    <aside class="cta-band post-cta" aria-label="Try Sobat">
      <span class="glow" aria-hidden="true"></span>
      <p class="eyebrow" style="color: #FFC861">Going somewhere?</p>
      <h2>See who's going your way</h2>
      <p>Sobat shows rides already heading where you are. Join one in a tap, or start your own, then meet up, book one cab and split the fare.</p>
      <a class="button light" href="/app/">Open the app <span class="arrow" aria-hidden="true">→</span></a>
    </aside>
"""

ORG = {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Sobat", "url": f"{SITE}/", "logo": f"{SITE}/assets/icon-512.png"}

def card(p):
    url = f"/blog/{p['slug']}/"
    return f"""<a class="post-card" href="{url}">
          <span class="eyebrow">{esc(p['eyebrow'])}</span>
          <h3>{esc(p['h1'][0].upper() + p['h1'][1:])}</h3>
          <p>{esc(p['card'])}</p>
          <span class="more">{minutes(p['body'])} min read <span aria-hidden="true">→</span></span>
        </a>"""

for p in posts:
    url = f"{SITE}/blog/{p['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": f"{url}#article", "headline": p["h1"], "description": p["desc"],
         "datePublished": DATE, "dateModified": DATE, "inLanguage": "en-IN", "mainEntityOfPage": url,
         "image": f"{SITE}/assets/og-image.png", "author": {"@id": f"{SITE}/#org"}, "publisher": {"@id": f"{SITE}/#org"},
         "isPartOf": {"@id": f"{SITE}/blog/#blog"}},
        ORG,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["h1"], "item": url}]},
    ]}
    sources = ""
    if p.get("sources"):
        items = "\n".join(f'          <li><a href="{esc(u)}" rel="noopener" target="_blank">{esc(t)}</a></li>' for t, u in p["sources"])
        sources = f"""
        <h2>Sources</h2>
        <ul class="sources">
{items}
        </ul>"""
    related = "\n        ".join(card(by_slug[s]) for s in p["related"] if s in by_slug)
    page = head(p["title"], p["desc"], url, "article", ld) + f"""
  <main class="container narrow post">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">›</span><a href="/blog/">Blog</a></nav>
    <article>
      <header class="post-head">
        <p class="eyebrow">{esc(p['eyebrow'])}</p>
        <h1>{esc(p['h1'][0].upper() + p['h1'][1:])}</h1>
        <p class="post-meta"><time datetime="{DATE}">{DATE_LABEL}</time> · {minutes(p['body'])} min read</p>
        <p class="lede">{esc(p['lede'])}</p>
      </header>
      <div class="post-body">
{p['body'].strip()}{sources}
      </div>
    </article>
{CTA}
    <section class="related" aria-labelledby="related-h">
      <h2 id="related-h">Keep reading</h2>
      <div class="post-cards">
        {related}
      </div>
    </section>
  </main>
""" + FOOT
    os.makedirs(f"{OUT}/blog/{p['slug']}", exist_ok=True)
    open(f"{OUT}/blog/{p['slug']}/index.html", "w").write(page)

# The index
url = f"{SITE}/blog/"
title = "Sobat Blog: Cab Sharing, Fares and Ride Rules in India"
desc = "Guides to sharing cabs in India: Ola and Uber pricing rules, meter fares, whether carpooling is legal, avoiding scams, staying safe and splitting fares."
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Blog", "@id": f"{url}#blog", "name": "Sobat Blog", "url": url, "description": desc, "inLanguage": "en-IN", "publisher": {"@id": f"{SITE}/#org"},
     "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": f"{SITE}/blog/{p['slug']}/", "datePublished": DATE} for p in posts]},
    ORG,
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": url}]},
]}
cards = "\n        ".join(card(p) for p in posts)
page = head(title, desc, url, "website", ld) + f"""
  <main class="container blog-index">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">›</span><span>Blog</span></nav>
    <header class="post-head">
      <p class="eyebrow">Guides</p>
      <h1>The Sobat blog</h1>
      <p class="lede">Practical guides for getting around by cab in India: what Ola and Uber are allowed to charge, meter fares, whether carpooling is legal, avoiding scams, staying safe and splitting the fare.</p>
    </header>
    <div class="post-cards">
        {cards}
    </div>
{CTA}
  </main>
""" + FOOT
os.makedirs(f"{OUT}/blog", exist_ok=True)
open(f"{OUT}/blog/index.html", "w").write(page)
print("built", len(posts), "posts:", ", ".join(f"{p['slug']} ({minutes(p['body'])} min)" for p in posts))

# The sitemap: home, the blog, every post, the legal pages.
urls = [("/", "1.0"), ("/blog/", "0.8")] + [(f"/blog/{p['slug']}/", "0.7") for p in posts] + \
       [("/privacy.html", "0.3"), ("/terms.html", "0.3"), ("/delete-account.html", "0.3")]
open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{DATE}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls) + "</urlset>\n")
