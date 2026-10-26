# getsobat.in

The public website for [Sobat](https://getsobat.in): home page, privacy policy,
terms, newsletter sign-up, and web account deletion (required by Google Play).

Plain HTML, CSS and JavaScript, no frameworks. The hand-written pages live in
this repo; the blog, route pages, sitemap and robots.txt are generated from
content managed in the admin console (stored in Supabase) by
`tools/blog/build.py`, which the **Site** workflow
(`.github/workflows/site.yml`) runs and deploys to GitHub Pages
(Settings → Pages → Source: **GitHub Actions**).

## Pages

| File | What it is |
|---|---|
| `index.html` | Home: what Sobat is, how it works, safety, newsletter sign-up |
| `privacy.html` | Privacy policy. Mirrors `app/privacy-policy.tsx` in the app repo |
| `terms.html` | Terms of service. Mirrors `app/terms.tsx` in the app repo |
| `delete-account.html` | Sign in (phone OTP or Google), then delete the account via `delete_own_account()` |
| `404.html` | Not-found page. Also forwards web-app deep links (`/app/...`) and ride invites (`/r/<ride id>`) to the web app |
| `blog/`, `routes/`, `sitemap.xml`, `robots.txt` | Generated at build time from the admin console's content; not in this repo |
| `app/` | The web app (getsobat.in/app), built from the app repo by `npm run web:deploy`. Don't edit by hand |

The legal pages are **drafts**: keep the draft banner and the `[bracketed]`
placeholders until they have real, reviewed values. Keep them in sync with the
app's copies.

## Blog, route pages and SEO

Posts and route pages are written in the admin console (getsobat.in/app →
the admin path → Site), in Markdown, with live preview and SEO checks.
Editors save drafts; owners publish. Publishing starts the Site workflow,
which runs `python3 tools/blog/build.py _site` (pulls `site_export()` from
Supabase with the publishable key), deploys, then tells IndexNow (Bing and
others) which addresses changed. The workflow also runs on every push and
every 30 minutes (scheduled posts; skipped when nothing changed).

- Live about 2–5 minutes after Publish. GitHub Pages caches pages for up to
  10 minutes, so a page someone already had open can lag that long.
- The build refuses to run with no published posts, so a database problem
  can't wipe the blog.
- Site-wide SEO (default sharing image, Organization data, robots rules,
  redirects) is under Site → Settings. Old addresses get a forwarding page
  and an entry in `404.html` (`var REDIRECTS`).
- The home page's latest posts go between `<!-- latest-posts -->` markers in
  `index.html`.
- Local build: `pip install markdown-it-py==3.0.0`, then
  `python3 tools/blog/build.py _site` and open `_site/` with any static server.
- `assets/stats.js` is Sobat's own page counter (no cookies, no IPs), shown
  under Site → Analytics.

## Backend

Uses the same Supabase project as the app. `assets/config.js` holds the
project URL and the **publishable** key, which ship inside the app anyway.
Never put a secret key in this repo.

- Newsletter: the `newsletter` Edge Function (Turnstile check), which calls
  `subscribe_newsletter(p_email)` from `supabase/migrations/002_website.sql`
  in the app repo. The list is in the admin console (Lists).
- Content: `site_export()` (published pages only) from the same file.
- Page counter: `track_page_view()` from the same file.
- Deletion: the app's existing `delete_own_account()` function.

## One-time setup

1. **DNS at GoDaddy** for `getsobat.in`:
   - `A` records for `@` pointing to `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153`
   - `CNAME` record for `www` pointing to `gauravharsh15.github.io`
2. **GitHub Pages**: custom domain `getsobat.in`, then tick "Enforce HTTPS" once
   the certificate is ready.
3. **Supabase → Authentication → URL Configuration → Redirect URLs**: add
   `https://getsobat.in/delete-account.html` (and the github.io URL while
   testing) so Google sign-in can return to the deletion page.
4. **Supabase SQL Editor**: run `002_website.sql` from the app repo once.
