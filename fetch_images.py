#!/usr/bin/env python3
"""Download the current Webflow images once, optimise them, and store local copies in src/img/.

After this runs, build.py serves every image from the site itself, so the new site no longer
depends on the Webflow CDN. Needs network access to cdn.prod.website-files.com.
"""
import io, json, os, sys, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from build import IMAGES, CDN  # noqa: E402

OUT = os.path.join(ROOT, "src", "img")
RAW = os.path.join(ROOT, "src", "img-raw")
os.makedirs(OUT, exist_ok=True)
os.makedirs(RAW, exist_ok=True)

# target widths for responsive photos and illustrations
WIDTHS = {
    "hero": [640, 1024, 1600, 2400], "night": [640, 1024, 1600, 2400],
    "gravel": [480, 800], "mountain": [480, 804],
    "flatbed": [560, 1136], "container": [560, 1136], "tanker": [560, 1136], "reefer": [560, 1136],
    "ltl": [640, 1200, 1826], "ftl": [640, 1200, 1826],
}
SLUGS = {"hero": "hero-truck-mountain-road", "night": "truck-at-dusk", "gravel": "tanker-gravel-road",
         "mountain": "truck-mountain-highway", "flatbed": "fleet-flatbed", "container": "fleet-container-trailer",
         "tanker": "fleet-tanker", "reefer": "fleet-refrigerated", "ltl": "part-load-ltl", "ftl": "full-load-ftl",
         "mark": "patriot-africa-mark", "word": "patriot-africa-wordmark", "favicon": "favicon"}

def fetch(key):
    stem, ext, w, h, _ = IMAGES[key]
    path = os.path.join(RAW, stem + "." + ext)
    if not os.path.exists(path):
        req = urllib.request.Request(CDN + stem + "." + ext, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as fh:
            fh.write(r.read())
    return path, ext

manifest = {}
for key in IMAGES:
    path, ext = fetch(key)
    slug = SLUGS.get(key, key.replace("p-", "partner-"))
    if ext == "svg" or key not in WIDTHS:
        # logos and icons stay in their original format
        name = slug + "." + ext
        with open(path, "rb") as src, open(os.path.join(OUT, name), "wb") as dst:
            dst.write(src.read())
        manifest[key] = [[IMAGES[key][2], name]]
        continue
    im = Image.open(path)
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if has_alpha else "RGB")
    files = []
    for w in WIDTHS[key]:
        w = min(w, im.width)
        h = round(im.height * w / im.width)
        out = im.resize((w, h), Image.LANCZOS)
        name = "%s-%d.webp" % (slug, w)
        quality = 74 if key in ("hero", "night", "gravel", "mountain") else 82
        out.save(os.path.join(OUT, name), "WEBP", quality=quality, method=6)
        files.append([w, name])
    manifest[key] = files
    print(key, [f[1] for f in files])

# social sharing image, 1200 x 630, from the hero photo
hero = Image.open(fetch("hero")[0]).convert("RGB")
tw, th = 1200, 630
scale = max(tw / hero.width, th / hero.height)
hero = hero.resize((round(hero.width * scale), round(hero.height * scale)), Image.LANCZOS)
left = round((hero.width - tw) * 0.62)
top = round((hero.height - th) / 2)
hero.crop((left, top, left + tw, top + th)).save(os.path.join(OUT, "og-image.jpg"), "JPEG", quality=84, optimize=True)

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=1)
print("Saved", len(manifest), "images to", OUT)
