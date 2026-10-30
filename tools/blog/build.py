# Builds getsobat.in into a folder for GitHub Pages: copies the hand-written
# pages and assets, then generates the blog (/blog/), route pages
# (/routes/), the home page's latest posts, sitemap.xml, robots.txt,
# redirects and the IndexNow key file from the content published in the
# admin console (Supabase: site_export() in the app repo's 002_website.sql).
#
# .github/workflows/site.yml runs it on every push, when an owner publishes,
# and every 30 minutes (for scheduled posts). Locally:
#   pip install markdown-it-py==3.0.0
#   python3 tools/blog/build.py _site                      reads Supabase
#   python3 tools/blog/build.py _site --export saved.json  reads a saved export
# It never builds a site without posts: an empty or failed export stops it.
#
# Markdown is CommonMark plus tables, with no raw HTML. Three conventions,
# mirrored by the admin's preview (lib/markdown.ts in the app repo):
#   "Table: …" just above a table is its caption; a quote starting
#   "[!NOTE]" is a note box; any other quote is a callout box.
import hashlib, html, json, math, os, re, shutil, sys, urllib.request
from datetime import datetime, timedelta, timezone
from markdown_it import MarkdownIt

SITE = "https://getsobat.in"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IST = timezone(timedelta(hours=5, minutes=30))
GENERATED = {"blog", "routes", "sitemap.xml", "robots.txt"}
SKIP = {".git", ".github", "tools", "README.md", "_site"} | GENERATED

args = sys.argv[1:]
OUT = os.path.abspath(args[0]) if args and not args[0].startswith("--") else os.path.join(ROOT, "_site")
opt = lambda name: args[args.index(name) + 1] if name in args else None

# ── Content
def fetch_export():
    if opt("--export"):
        return json.load(open(opt("--export")))
    cfg = open(os.path.join(ROOT, "assets", "config.js")).read()
    url = re.search(r'supabaseUrl:\s*"([^"]+)"', cfg).group(1)
    key = re.search(r'publishableKey:\s*"([^"]+)"', cfg).group(1)
    req = urllib.request.Request(f"{url}/rest/v1/rpc/site_export", data=b"{}", method="POST",
                                 headers={"apikey": key, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))

data = fetch_export()
settings = data.get("settings") or {}
items = data.get("items") or []
posts = [p for p in items if p["kind"] == "post"]
routes = [p for p in items if p["kind"] == "route"]
media = data.get("media") or {}
redirects = data.get("redirects") or []
if not posts:
    sys.exit("No published posts in the export: refusing to build a site without its blog.")

# ── Markdown
MD = MarkdownIt("commonmark", {"html": False}).enable(["table", "strikethrough"])

def boxes(h):
    out, i = [], 0
    for m in re.finditer(r"<blockquote>\n|</blockquote>", h):
        out.append(h[i:m.start()])
        i = m.end()
        if m.group(0).startswith("<blockquote"):
            note = re.match(r"<p>\[!NOTE\](?:</p>\n<p>|\s*)", h[i:])
            if note:
                i += note.end()
                out.append('<div class="note">\n<p>')
            else:
                out.append('<div class="callout">\n')
        else:
            out.append("</div>")
    out.append(h[i:])
    # A one-paragraph note is the site's <p class="note">.
    return re.sub(r'<div class="note">\n<p>((?:(?!</?p>).)*)</p>\n</div>', r'<p class="note">\1</p>', "".join(out), flags=re.S)

def finish(h):
    h = boxes(h)
    h = h.replace("<table>", '<div class="table-wrap">\n<table class="table">').replace("</table>", "</table>\n</div>")
    h = re.sub(r'<p>Table: ((?:(?!</p>).)*)</p>\n<div class="table-wrap">\n<table class="table">',
               r'<div class="table-wrap">\n<table class="table">\n<caption>\1</caption>', h)
    h = re.sub(r'<a href="(https?://(?!getsobat\.in|www\.getsobat\.in)[^"]*)"', r'<a href="\1" rel="noopener" target="_blank"', h)
    def img(m):
        size = media.get(html.unescape(m.group(1))) or {}
        wh = ' width="%s" height="%s"' % (size["width"], size["height"]) if size.get("width") and size.get("height") else ""
        return '<img src="%s"%s%s loading="lazy" decoding="async"' % (m.group(1), m.group(2), wh)
    return re.sub(r'<img src="([^"]*)"((?: [a-z]+="[^"]*")*)', img, h)

def split_h1(md):
    m = re.search(r"^# +(.+?)\s*#*\s*$", md, re.M)
    if not m:
        return "", md
    return m.group(1), md[:m.start()] + md[m.end():]

def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def when(s):
    # Postgres may send 1–6 decimals; Python 3.9 wants 3 or 6.
    s = re.sub(r"\.(\d+)", lambda m: "." + (m.group(1) + "000000")[:6], s.replace("Z", "+00:00"))
    return datetime.fromisoformat(s).astimezone(IST)

for p in items:
    h1_md, body_md = split_h1(p["body_md"])
    p["h1_html"] = MD.renderInline(h1_md) if h1_md else html.escape(p["title"])
    p["h1"] = plain(p["h1_html"])
    p["body_html"] = finish(MD.render(body_md)).strip()
    p["minutes"] = max(2, math.ceil(len(re.sub(r"<[^>]+>", " ", p["body_html"]).split()) / 200))
    p["date"], p["modified"] = when(p["date_published"]), when(p["date_modified"])
    p["url"] = SITE + p["path"]

# ── Page parts
TILE = '<span class="brand-tile"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M18 45 C 32 45, 32 19, 46 19" stroke="#FFFFFF" stroke-width="6.5" fill="none" stroke-linecap="round"/><circle cx="18" cy="45" r="6.6" fill="#FFFFFF"/><circle cx="46" cy="19" r="6.6" fill="#FFB23E"/></svg></span>'
OG_IMAGE = settings.get("default_og_image") or f"{SITE}/assets/og-image.png"
ORG = {"@type": "Organization", "@id": f"{SITE}/#org", "name": settings.get("org_name") or "Sobat", "url": f"{SITE}/",
       "logo": settings.get("org_logo") or f"{SITE}/assets/icon-512.png"}
if settings.get("org_email"):
    ORG["email"] = settings["org_email"]
if settings.get("same_as"):
    ORG["sameAs"] = settings["same_as"]

def esc(s):
    return html.escape(s or "", quote=True)

def label(d):
    return "%d %s" % (d.day, d.strftime("%B %Y"))

def cap(s):
    return s[:1].upper() + s[1:]

def nav():
    links = ['<a href="/#how">How it works</a>', '<a href="/blog/">Blog</a>']
    if routes:
        links.append('<a href="/routes/">Routes</a>')
    links.append('<a href="/#faq">FAQ</a>')
    return "\n        ".join(links)

def head(title, desc, url, og_type, ld, image=None, noindex=False, canonical=None):
    image = image or OG_IMAGE
    size = '\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">' if image == OG_IMAGE else ""
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    return f"""<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">{robots}
  <link rel="canonical" href="{esc(canonical or url)}">
  <meta property="og:site_name" content="Sobat">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="en_IN">
  <meta property="og:image" content="{esc(image)}">{size}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{esc(image)}">
  <meta name="theme-color" content="#F5F4FA">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-192.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="stylesheet" href="/assets/site.css">
  <script src="/assets/stats.js" defer></script>
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
        {nav()}
      </nav>
      <a class="button small" href="/app/">Open the app</a>
    </div>
  </header>
"""

FOOT = """
  <footer class="site-footer">
    <div class="container">
      <span class="footer-brand">%s© %d Sobat · India</span>
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
""" % (TILE, datetime.now(IST).year)

CTA = """
    <aside class="cta-band post-cta" aria-label="Try Sobat">
      <span class="glow" aria-hidden="true"></span>
      <p class="eyebrow" style="color: #FFC861">Going somewhere?</p>
      <h2>See who's going your way</h2>
      <p>Sobat shows rides already heading where you are. Join one in a tap, or start your own, then meet up, book one cab and split the fare.</p>
      <a class="button light" href="/app/">Open the app <span class="arrow" aria-hidden="true">→</span></a>
    </aside>
"""

def card(p, more=None):
    more = more or "%d min read" % p["minutes"]
    return f"""<a class="post-card" href="{p['path']}">
          <span class="eyebrow">{esc(p['eyebrow'])}</span>
          <h3>{esc(cap(p['h1']))}</h3>
          <p>{esc(p['summary'])}</p>
          <span class="more">{more} <span aria-hidden="true">→</span></span>
        </a>"""

SECTION = {"post": ("Blog", "/blog/"), "route": ("Routes", "/routes/")}
pages = {}  # path → html, for the manifest

def write(path, page):
    pages[path] = page
    rel = path.lstrip("/")
    target = os.path.join(OUT, rel, "index.html") if path.endswith("/") else os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    open(target, "w").write(page)

# ── Build
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
def ignore(d, names):
    top = os.path.abspath(d) == ROOT
    return [n for n in names if (top and n in SKIP) or n == ".DS_Store" or os.path.join(os.path.abspath(d), n) == OUT]
shutil.copytree(ROOT, OUT, ignore=ignore)

for p in items:
    section, section_path = SECTION[p["kind"]]
    same = posts if p["kind"] == "post" else routes
    by_slug = {x["slug"]: x for x in same}
    related = [by_slug[s] for s in p.get("related") or [] if s in by_slug and s != p["slug"]]
    if not related:
        related = [x for x in same if x is not p][:3]
    article = {"@type": "BlogPosting" if p["kind"] == "post" else "Article", "@id": f"{p['url']}#article", "headline": cap(p["h1"]),
               "description": p["meta_description"], "datePublished": p["date"].date().isoformat(), "dateModified": p["modified"].date().isoformat(),
               "inLanguage": "en-IN", "mainEntityOfPage": p["url"], "image": p.get("cover_url") or OG_IMAGE,
               "author": {"@id": f"{SITE}/#org"}, "publisher": {"@id": f"{SITE}/#org"}}
    if p["kind"] == "post":
        article["isPartOf"] = {"@id": f"{SITE}/blog/#blog"}
    ld = {"@context": "https://schema.org", "@graph": [article, ORG, {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": section, "item": f"{SITE}{section_path}"},
        {"@type": "ListItem", "position": 3, "name": cap(p["h1"]), "item": p["url"]}]}]}
    sources = ""
    if p.get("sources"):
        rows = "\n".join('          <li><a href="%s" rel="noopener" target="_blank">%s</a></li>' % (esc(s["url"]), esc(s["title"])) for s in p["sources"])
        sources = "\n        <h2>Sources</h2>\n        <ul class=\"sources\">\n%s\n        </ul>" % rows
    cover = ""
    if p.get("cover_url"):
        size = media.get(p["cover_url"]) or {}
        wh = ' width="%s" height="%s"' % (size["width"], size["height"]) if size.get("width") else ""
        cover = '\n      <figure class="post-cover"><img src="%s" alt="%s"%s decoding="async"></figure>' % (esc(p["cover_url"]), esc(p.get("cover_alt")), wh)
    lede = '\n        <p class="lede">%s</p>' % esc(p["lede"]) if p.get("lede") else ""
    keep = "\n        ".join(card(x) for x in related)
    related_html = f"""
    <section class="related" aria-labelledby="related-h">
      <h2 id="related-h">Keep reading</h2>
      <div class="post-cards">
        {keep}
      </div>
    </section>""" if related else ""
    page = head(p["title"], p["meta_description"], p["url"], "article", ld, p.get("cover_url"), p.get("noindex"), p.get("canonical")) + f"""
  <main class="container narrow post">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">›</span><a href="{section_path}">{section}</a></nav>
    <article>
      <header class="post-head">
        <p class="eyebrow">{esc(p['eyebrow'])}</p>
        <h1>{cap(p['h1_html'])}</h1>
        <p class="post-meta"><time datetime="{p['date'].date().isoformat()}">{label(p['date'])}</time> · {p['minutes']} min read</p>{lede}
      </header>{cover}
      <div class="post-body">
{p['body_html']}{sources}
      </div>
    </article>
{CTA}{related_html}
  </main>
""" + FOOT
    write(p["path"], page)

def index_page(kind, list_, title, desc, h1, lede, eyebrow):
    section, path = SECTION[kind]
    url = SITE + path
    if kind == "post":
        top = {"@type": "Blog", "@id": f"{url}#blog", "name": "Sobat Blog",
               "blogPost": [{"@type": "BlogPosting", "headline": cap(p["h1"]), "url": p["url"], "datePublished": p["date"].date().isoformat()} for p in list_]}
    else:
        top = {"@type": "CollectionPage", "@id": f"{url}#page", "name": title}
    top.update({"url": url, "description": desc, "inLanguage": "en-IN", "publisher": {"@id": f"{SITE}/#org"}})
    ld = {"@context": "https://schema.org", "@graph": [top, ORG, {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": section, "item": url}]}]}
    cards = "\n        ".join(card(p) for p in list_ if not p.get("noindex"))
    write(path, head(title, desc, url, "website", ld) + f"""
  <main class="container blog-index">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">›</span><span>{section}</span></nav>
    <header class="post-head">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
    </header>
    <div class="post-cards">
        {cards}
    </div>
{CTA}
  </main>
""" + FOOT)

index_page("post", posts, "Sobat Blog: Cab Sharing, Fares and Ride Rules in India",
           "Guides to sharing cabs in India: Ola and Uber pricing rules, meter fares, whether carpooling is legal, avoiding scams, staying safe and splitting fares.",
           "The Sobat blog", "Practical guides for getting around by cab in India: what Ola and Uber are allowed to charge, meter fares, whether carpooling is legal, avoiding scams, staying safe and splitting the fare.", "Guides")
if routes:
    index_page("route", routes, "Shared Cab Routes in India | Sobat",
               "Share a cab on routes people travel every day: where riders meet, what the cab costs and what each person pays when you split it.",
               "Share a cab on your route", "Routes people ride every day: where to meet, what the cab costs, and what each person pays when you share it.", "Routes")

# Home: the latest posts, the Organization data and the default social image.
home_path = os.path.join(OUT, "index.html")
home = open(home_path).read()
latest = [p for p in posts if not p.get("noindex")][: int(settings.get("home_latest", 3))]
home = re.sub(r"(<!-- latest-posts -->).*?(\s*<!-- /latest-posts -->)",
              lambda m: m.group(1) + "\n        " + "\n        ".join(card(p, "Read") for p in latest) + m.group(2), home, flags=re.S)
def org_ld(m):
    ld = json.loads(m.group(2))
    ld["@graph"] = [ORG if n.get("@type") == "Organization" else n for n in ld.get("@graph", [])]
    return m.group(1) + "\n" + json.dumps(ld, ensure_ascii=False, indent=2) + "\n  " + m.group(3)
home = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', org_ld, home, count=1, flags=re.S)
home = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*', lambda m: m.group(1) + esc(OG_IMAGE), home)
open(home_path, "w").write(home)
pages["/"] = home

# Redirects: a page at each old address that sends people (and search
# engines) to the new one, and the same list for 404.html.
for r in redirects:
    src, dst = r["from"], r["to"]
    if src in pages or not (src.endswith("/") or src.endswith(".html")):
        continue
    target = esc(dst if dst.startswith("https://") else SITE + dst)
    write(src, f"""<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <title>Moved</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{target}">
  <meta http-equiv="refresh" content="0; url={target}">
  <script>location.replace({json.dumps(html.unescape(target))});</script>
</head>
<body><p>This page has moved: <a href="{target}">{target}</a>.</p></body>
</html>
""")
four = os.path.join(OUT, "404.html")
# Read before opening to write: opening with "w" empties the file first.
page404 = open(four).read().replace("var REDIRECTS = {};", "var REDIRECTS = " + json.dumps({r["from"]: r["to"] for r in redirects}) + ";")
open(four, "w").write(page404)

# robots.txt, the sitemap and the IndexNow key.
disallow = "".join("Disallow: %s\n" % d for d in settings.get("robots_disallow", ["/app/", "/tools/"]))
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\n%s\nSitemap: %s/sitemap.xml\n" % (disallow, SITE))
listed = [p for p in items if not p.get("noindex") and not p.get("canonical")]
day = lambda ps: max(p["modified"] for p in ps).date().isoformat()
urls = [("/", day(items), "1.0"), ("/blog/", day(posts), "0.8")] + ([("/routes/", day(routes), "0.8")] if routes else []) + \
       [(p["path"], p["modified"].date().isoformat(), "0.7") for p in listed] + \
       [("/privacy.html", None, "0.3"), ("/terms.html", None, "0.3"), ("/delete-account.html", None, "0.3")]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join("  <url><loc>%s%s</loc>%s<priority>%s</priority></url>\n" % (SITE, u, "<lastmod>%s</lastmod>" % d if d else "", pr) for u, d, pr in urls) + "</urlset>\n")
key = settings.get("indexnow_key")
if key:
    open(os.path.join(OUT, key + ".txt"), "w").write(key)

# What changed since the live site (site-manifest.json), for the workflow:
# whether to deploy, and which addresses to send to IndexNow.
manifest = {path: hashlib.sha1(page.encode()).hexdigest() for path, page in sorted(pages.items())}
json.dump(manifest, open(os.path.join(OUT, "site-manifest.json"), "w"), indent=1)
print("built %d posts, %d routes, %d redirects into %s" % (len(posts), len(routes), len(redirects), OUT))
if opt("--changes"):
    try:
        before = json.load(urllib.request.urlopen(SITE + "/site-manifest.json?b=" + manifest["/"], timeout=20))
    except Exception:
        before = {}
    changed = sorted(p for p in set(manifest) | set(before) if manifest.get(p) != before.get(p))
    deploy = bool(changed) or opt("--event") != "schedule"
    body = json.dumps({"host": "getsobat.in", "key": key, "keyLocation": "%s/%s.txt" % (SITE, key), "urlList": [SITE + p for p in changed]}) if key and changed else ""
    with open(opt("--changes"), "a") as f:
        f.write("deploy=%s\nindexnow=%s\n" % ("true" if deploy else "false", body))
    print("changed: %d (%s); deploy: %s" % (len(changed), ", ".join(changed[:10]), deploy))
