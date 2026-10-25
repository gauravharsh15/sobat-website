# getsobat.in

The public website for [Sobat](https://getsobat.in): home page, privacy policy,
terms, newsletter sign-up, and web account deletion (required by Google Play).

Plain HTML, CSS and JavaScript. No build step, no frameworks, no third-party
scripts or fonts. Hosted on GitHub Pages from the `main` branch.

## Pages

| File | What it is |
|---|---|
| `index.html` | Home: what Sobat is, how it works, safety, newsletter sign-up |
| `privacy.html` | Privacy policy. Mirrors `app/privacy-policy.tsx` in the app repo |
| `terms.html` | Terms of service. Mirrors `app/terms.tsx` in the app repo |
| `delete-account.html` | Sign in (phone OTP or Google), then delete the account via `delete_own_account()` |
| `404.html` | Not-found page. Also forwards web-app deep links (`/app/...`) and ride invites (`/r/<ride id>`) to the web app |
| `blog/` | The blog: an index and one folder per post. Generated: don't edit by hand |
| `app/` | The web app (getsobat.in/app), built from the app repo by `npm run web:deploy`. Don't edit by hand |

The legal pages are **drafts**: keep the draft banner and the `[bracketed]`
placeholders until they have real, reviewed values. Keep them in sync with the
app's copies.

## Blog

Posts live in `tools/blog/posts.py` and `tools/blog/posts_rules.py` (anything
citing a rule, a fare or a price goes in the second, with its sources and the
date it was checked). `python3 tools/blog/build.py .` regenerates `blog/` and
`sitemap.xml`; commit the result. Every page gets its own title, description,
canonical URL, Open Graph tags and BlogPosting + BreadcrumbList structured data.
Keep descriptions under 160 characters and titles under about 60.

## Backend

Uses the same Supabase project as the app. `assets/config.js` holds the
project URL and the **publishable** key, which ship inside the app anyway.
Never put a secret key in this repo.

- Newsletter: `subscribe_newsletter(p_email)` from
  `supabase/migrations/002_website.sql` in the app repo. The list can't be read
  through the publishable key; view it in Supabase's Table Editor.
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
