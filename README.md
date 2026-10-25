# Patriot Africa website

A static website of 11 pages, built from a small Python script. It needs no database and no plugins. GitHub stores the code, and Cloudflare Pages publishes it.

## Folder layout

| Path | Purpose |
|---|---|
| `site/` | The finished website. Cloudflare Pages publishes this folder. |
| `content.py` | The text of every page |
| `build.py` | Shared parts (header, footer, map, images), the site settings in `CONFIG`, and the build |
| `src/styles.css`, `src/site.js` | The design system and the page scripts |
| `preview.py` | Runs the site on your computer |
| `fetch_images.py` | Optional. Packs local copies of the Webflow images into the site. |

## Preview on your computer

```
python3 preview.py            # this Mac only, at http://localhost:8000
python3 preview.py --lan      # also open to phones on the same Wi-Fi
```

## Change the site

1. Edit the text in `content.py`, the settings in `build.py`, or the styles in `src/styles.css`.
2. Run `python3 build.py`. This rewrites the `site` folder.
3. Check the result with `python3 preview.py`.
4. Commit and push to GitHub. Cloudflare Pages publishes the change in about one minute.

## Cloudflare Pages settings

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | `python3 build.py` |
| Build output directory | `site` |
| Production branch | `main` |

Cloudflare Pages serves `services.html` at `/services`, shows `404.html` for missing pages, and reads `_redirects` and `_headers` in the `site` folder.

## Settings in `build.py`

| Setting | What it does |
|---|---|
| `phone` | Shows a tap to call number on the Quote page and in the quote band |
| `whatsapp` | Adds WhatsApp buttons with a prefilled message (digits only, with country code) |
| `linkedin` | Adds the LinkedIn company page to the footer |
| `quote_email` | The address that receives quote requests (`quotes@patriotafrica.com`) |
| `form_endpoint` | Sends quote requests to a form service such as Formspree, which emails them to `quotes@patriotafrica.com`. Without it, the form prepares an email for the visitor to send. |
| `ga4` | Adds Google Analytics 4. Buttons carry `data-cta` labels for click tracking. |

## Confirm these facts before launch

- 20+ years, 150+ trucks and trailers, 10 countries, 7 industries.
- Satellite tracking, 24/7 customer service and round the clock security.
- The corridors and border posts on the Routes and Lobito Corridor pages.
- Mozambique (Beira corridor), which the current Terms page does not list.
- Permission from each partner to show its logo.
- The brand name, if the company now trades as Meridian.

## After launch

1. Add the site to Google Search Console and submit `https://www.patriotafrica.com/sitemap.xml`.
2. Create a Google Business Profile for the Ndola office with the same address and email as the site.
3. List the company in Zambian and regional logistics directories with the same details.
