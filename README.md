# Brownlee Sand & Gravel website

Static, mobile-first site. Passes the W3C Nu HTML/CSS validator. No database, no plugins, fast and cheap to host.

## What's already filled in (from the Facebook page)
- Phone (705) 622-3373, email brownleesandandgravel@outlook.com
- 35 Pinetree Road, Kirkland Lake, ON P2N 3M6
- Services and areas: Kirkland Lake, Temiskaming Shores, Timmins, Larder Lake, Matheson, Cobalt
- 23 pages (rebuilt from a competitor teardown): Home, 4 service pages, 6 town pages, Gravel Calculator, FAQ, About, Gallery, Contact, 404
- SEO built in: unique titles and descriptions, canonical links, breadcrumbs, LocalBusiness + Service + FAQPage + BreadcrumbList schema, Open Graph image, sitemap.xml, robots.txt, internal links between services and towns
- Conversion: quick-quote form in the hero, click-to-call everywhere, sticky mobile call bar, gravel calculator

## Confirm with Matt before launch
- Slinger reach "70-100 ft" and "35-40 minute" job time come from his Facebook posts. Confirm they are accurate claims.
- Business hours (placeholder text now) and whether he offers winter plowing (one flyer showed a snowplough).
- Real domain: change `SITE_URL` at the top of `build.py`.

## 1. Add the photos and logo
The Facebook photos were saved from Chrome to your Downloads folder:
- `brownlee-website-photos.zip`: the 24 picks for the site, already named (hero.jpg = home banner, logo.jpg = logo in header, favicon and schema).
- `brownlee-photos.zip`: all 88 page photos plus their Facebook captions.

Unzip `brownlee-website-photos.zip` into the `photos/` folder, then run `python3 build.py`. Each photo is converted to AVIF, WebP and JPG at 480/800/1200/1800 px with alt text, and placed on the home page, service pages, town pages and gallery. An optional `photos/captions.csv` (filename,alt text) overrides the default alt text.

## 2. Build
```
pip install pillow
python3 build.py
```
Output goes to `dist/`. Re-run any time you change a photo, text or setting.

## 3. Go live (pick one)
- **Any cPanel/shared host:** upload everything inside `dist/` to `public_html/`. The included `.htaccess` adds caching and compression.
- **Netlify / Cloudflare Pages (free):** drag the `dist/` folder into the dashboard, then add the custom domain.
- After launch: submit `https://YOURDOMAIN/sitemap.xml` in Google Search Console, and claim/verify the Google Business Profile with the same name, address and phone (NAP) as the site.

## 4. Make the quote form send real emails
The form currently opens the visitor's email app (`mailto:`). For reliable delivery, create a free form at formspree.io or Netlify Forms and set `FORM_ACTION` in `build.py` to that URL, then rebuild.

## 5. WordPress option
If Matt wants to edit pages himself, use WordPress with a lightweight theme (GeneratePress or Kadence) plus these plugins: Rank Math (SEO + schema), ShortPixel or Imagify (AVIF/WebP), WP Rocket or LiteSpeed Cache, WPForms Lite. Copy the text from the pages here. Keep one page per service and per town, since those drive local search.

## SEO next steps
- Post job photos with the town name in the caption, on Facebook and the Gallery.
- Ask happy customers for Google reviews and add them to the Home page.
- Link the website from the Facebook page "Website" field and the Google Business Profile.

## Reviews
Add real customer quotes to `REVIEWS` at the top of `build.py`, e.g. `REVIEWS = [("Sam, Timmins", "Matt had it done in under an hour.")]`. The section only appears once you add some. Do not publish invented reviews.

## Search Console and analytics
Set `GSC_TOKEN` and `GA_ID` in `build.py`, rebuild, upload, then submit the sitemap.

## Design system v4 (from measured competitor styles)
- Fonts (Google Fonts): Archivo ExtraBold, semi-expanded, sentence case with tight tracking for headings; Figtree 400-700 for body, nav and buttons.
- Colours (navy + safety yellow, Keller-style, matches the logo): navy #011D3F, mid navy #003B73, safety yellow #FDC600 (hover #FFD633), light surface #EEF2F6, text #0B1B2E, muted #4A5D73, borders #DCE3EA. Yellow is only used as a background or on navy, never as text on white, so every combination passes contrast checks.
- Radius 8 / 14 / 20 px; soft layered shadows; 1240 px container; 112 px section spacing on desktop.
- Breadcrumbs: shown as a pill inside each page header (home icon, chevrons, current page in yellow), with BreadcrumbList schema.
- Motion: hero text rises in on load, slow photo zoom, animated slinger arc, service/town ticker, sections fade up on scroll, stat counters, card lift and image zoom on hover, button shine. All motion turns off for visitors who set reduced motion.
- Navigation: navy top bar, white sticky header that shrinks on scroll, Services mega menu, Service Areas menu, About menu, phone button and gold quote button. Mobile: full-screen menu and a Call / Text / Quote bar.
- Lighthouse (home, local): Performance 93, Accessibility 100 (colour contrast passes), Best Practices 96, SEO 100. W3C HTML and CSS: 0 errors.
