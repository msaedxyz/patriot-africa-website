#!/usr/bin/env python3
"""Build the Patriot Africa site.

python3 build.py            -> site/      full static site for any host (clean URLs, root paths)
python3 build.py --artifact -> artifact/  same pages, packaged for the claude.ai preview

Images: if src/img/ holds local copies (see fetch notes in README), they are used and
copied into the output. Otherwise the pages load the originals from the Webflow CDN.
"""
import json, os, re, shutil, sys
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
ARTIFACT = "--artifact" in sys.argv
OUT = os.path.join(ROOT, "artifact" if ARTIFACT else "site")

# ---------------------------------------------------------------- site config
# Fill these in before launch. Empty values hide the matching buttons and links.
CONFIG = {
    "base_url": "https://www.patriotafrica.com",
    "name": "Patriot Africa",
    "email": "hello@patriotafrica.com",
    "quote_email": "quotes@patriotafrica.com",  # the quote form sends requests here
    "phone": "",            # display form, e.g. "+260 21 2xx xxxx"
    "whatsapp": "",         # digits only with country code, e.g. "260971234567"
    "linkedin": "",         # full company page URL
    "facebook": "https://www.facebook.com/Patriot1Transport/",
    "form_endpoint": "",    # e.g. a Formspree endpoint; empty = the form prepares an email instead
    "netlify_forms": False, # True only when the site is hosted on Netlify
    "ga4": "",              # e.g. "G-XXXXXXX"; empty = no analytics script
}
OFFICES = [
    {"region": "Africa", "label": "Head office", "title": "Ndola, Zambia",
     "lines": ["Patriot Transport & Trading Limited", "82764 Off Trade Fair Road", "Ndola", "Republic of Zambia"],
     "street": "82764 Off Trade Fair Road", "city": "Ndola", "country": "ZM"},
    {"region": "Middle East", "label": "Dubai office", "title": "Dubai, UAE",
     "lines": ["Patriot Transport & Trading Limited", "Business Centre", "Floor 3, Building A3", "Business Park", "Dubai", "United Arab Emirates"],
     "street": "Business Centre, Floor 3, Building A3, Business Park, Dubai South", "city": "Dubai", "country": "AE"},
]
COUNTRIES = ["Zambia", "Democratic Republic of the Congo", "Republic of the Congo", "Tanzania", "Malawi",
             "Zimbabwe", "Mozambique", "Namibia", "Angola", "South Africa"]

# ---------------------------------------------------------------- pages and URLs
PAGES = ["home", "services", "fleet", "coverage", "lobito", "industries", "about", "quote", "privacy", "terms", "404"]
SLUG = {"home": "", "services": "services", "fleet": "fleet", "coverage": "coverage", "lobito": "lobito-corridor",
        "industries": "industries", "about": "about", "quote": "quote", "privacy": "privacy-policy",
        "terms": "terms-conditions", "404": "404"}

def url(page, anchor=""):
    a = ("#" + anchor) if anchor else ""
    if ARTIFACT:
        return ("index.html" if page == "home" else SLUG[page] + ".html") + a
    return ("/" if page == "home" else "/" + SLUG[page]) + a

def canonical(page):
    return CONFIG["base_url"] + ("/" if page == "home" else "/" + SLUG[page])

def asset(path):
    return path if ARTIFACT else "/" + path

# ---------------------------------------------------------------- images
CDN = "https://cdn.prod.website-files.com/6709171f4f520480e161c05a/"
IMAGES = {
    # key: (stem, ext, width, height, cdn variant widths)
    "hero":      ("6709fb08f7f52e9455428a52_hero-background", "jpeg", 3864, 2576, [800, 1080, 1600, 2000, 2600]),
    "night":     ("670cbdea5947824a1a6dc74d_contact-background", "jpg", 3864, 2577, [800, 1080, 1600, 2000, 2600]),
    "gravel":    ("670a1240a08b68a665d9f400_About-image", "jpg", 992, 1496, [500, 800]),
    "mountain":  ("6709fb220638dd9cf657f570_about-img", "jpg", 804, 480, [500]),
    "flatbed":   ("670ca20da4b9a20627f10093_truck-image-01", "jpg", 1136, 500, [500, 800]),
    "container": ("670ca20d8a18a87894ec5f5d_truck-image-02", "jpg", 1136, 500, [500, 800]),
    "tanker":    ("670ca20de9e241b80c545cd9_truck-image-03", "jpg", 1136, 500, [500, 800]),
    "reefer":    ("670ca20dc9db159de3fd0524_truck-image-04", "jpg", 1136, 500, [500, 800]),
    "ltl":       ("670cdedac8056b9cfd80613f_truck-left", "png", 1826, 616, [500, 800, 1080]),
    "ftl":       ("670cdedad1db9beb1110ba85_truck-right", "png", 1826, 616, [500, 800, 1080]),
    "mark":      ("67091c49e3dc9cec9af9fc3f_nav-logo-image", "png", 64, 64, []),
    "word":      ("67091c4992c41614adfb3d1c_nav-logo", "svg", 192, 12, []),
    "favicon":   ("670ce489ca4484754615154d_favicon", "svg", 32, 32, []),
    "p-agl":      ("6709f414767ba2cae19ba4fb_brand-logo-01", "svg", 131, 56, []),
    "p-hass":     ("6709f41484a41ca4548f36b0_brand-logo-02", "svg", 71, 56, []),
    "p-etg":      ("670e00e927c4a1428d624de5_brand-logo-03", "png", 164, 112, []),
    "p-polytra":  ("670e00e98c237ba78d806e52_brand-logo-04", "png", 382, 112, []),
    "p-reload":   ("6709f414376c4d5aa56b99d8_brand-logo-05", "svg", 180, 56, []),
    "p-steinweg": ("6709f4144003f28ffcbdf8b4_brand-logo-06", "svg", 289, 56, []),
    "p-nucleus":  ("670cc89b772ad7e404f1a803_brand-logo-07", "jpg", 201, 112, []),
    "p-msc":      ("670cc8ab0ffec39158964406_brand-logo-08", "png", 127, 112, []),
    "p-fields":   ("fields-energy-logo", "png", 360, 59, []),
}
STATIC_IMG = os.path.join(SRC, "img-static")
STATIC_KEYS = {"p-fields"}
LOCAL_IMG = os.path.join(SRC, "img")
LOCAL_MANIFEST = os.path.join(LOCAL_IMG, "manifest.json")
LOCAL = json.load(open(LOCAL_MANIFEST)) if os.path.exists(LOCAL_MANIFEST) else {}

def img_src(key):
    """Return (src, srcset) for an image key."""
    stem, ext, w, h, variants = IMAGES[key]
    if key in STATIC_KEYS:
        return asset("img/%s.%s" % (stem, ext)), ""
    if key in LOCAL:
        files = LOCAL[key]  # list of [width, filename], ascending
        srcset = ", ".join("%s %dw" % (asset("img/" + f), fw) for fw, f in files)
        return asset("img/" + files[-1][1]), (srcset if len(files) > 1 else "")
    src = CDN + stem + "." + ext
    if variants:
        parts = ["%s%s-p-%d.%s %dw" % (CDN, stem, v, ext, v) for v in variants] + ["%s %dw" % (src, w)]
        return src, ", ".join(parts)
    return src, ""

def img(key, alt, sizes="100vw", cls="", eager=False, priority=False, width=None, height=None):
    stem, ext, w, h, _ = IMAGES[key]
    src, srcset = img_src(key)
    attrs = ['src="%s"' % src]
    if srcset:
        attrs.append('srcset="%s"' % srcset)
        attrs.append('sizes="%s"' % sizes)
    attrs.append('alt="%s"' % escape(alt))
    attrs.append('width="%d" height="%d"' % (width or w, height or h))
    if cls:
        attrs.append('class="%s"' % cls)
    attrs.append('loading="%s"' % ("eager" if eager or priority else "lazy"))
    attrs.append('decoding="async"')
    if priority:
        attrs.append('fetchpriority="high"')
    return "<img %s>" % " ".join(attrs)

def img_abs(key):
    src, _ = img_src(key)
    if src.startswith("http"):
        return src
    return CONFIG["base_url"] + "/" + src.lstrip("/")

# ---------------------------------------------------------------- icons (24px stroke set)
def icon(name, cls=""):
    p = {
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "truck": '<path d="M2 6h11v9H2zM13 9h4l3 3v3h-7"/><circle cx="6" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>',
        "layers": '<path d="M12 3 2 8l10 5 10-5-10-5z"/><path d="m2 13 10 5 10-5"/>',
        "border": '<path d="M4 21V4M4 4h12l-2 4 2 4H4"/><path d="M14 21h6M17 21v-6"/>',
        "mine": '<path d="M3 21 15 9"/><path d="M12 6c3-3 7-3 9 0-3-1-5 0-7 2"/><path d="M6 21h15"/>',
        "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
        "snow": '<path d="M12 2v20M4 6l16 12M20 6 4 18"/><path d="m9 4 3 2 3-2M9 20l3-2 3 2"/>',
        "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
        "phone": '<path d="M5 3h4l2 5-3 2a12 12 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A18 18 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
        "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        "headset": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1"/><rect x="17" y="14" width="4" height="6" rx="1"/><path d="M19 20a3 3 0 0 1-3 2h-3"/>',
        "cargo": '<rect x="3" y="4" width="8" height="8"/><rect x="13" y="4" width="8" height="8"/><rect x="8" y="12" width="8" height="8"/>',
        "menu": '<path d="M3 7h18M3 12h18M3 17h18"/>',
        "close": '<path d="M6 6l12 12M18 6 6 18"/>',
        "check": '<path d="m5 12 5 5 9-10"/>',
        "flask": '<path d="M9 3h6M10 3v6L4 19a1.5 1.5 0 0 0 1.3 2h13.4A1.5 1.5 0 0 0 20 19l-6-10V3"/><path d="M7 15h10"/>',
        "factory": '<path d="M3 21V10l6 4V10l6 4V6h6v15z"/><path d="M7 18h2M12 18h2M17 18h2"/>',
        "crane": '<path d="M6 21V4h2v17M4 21h8M8 4h13l-3 3M8 7h12M18 7v5"/><rect x="16" y="12" width="4" height="3"/>',
        "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
        "wheat": '<path d="M12 21V9"/><path d="M12 9c-3 0-4-2-4-5 3 0 4 2 4 5zM12 9c3 0 4-2 4-5-3 0-4 2-4 5zM12 15c-3 0-4-2-4-5 3 0 4 2 4 5zM12 15c3 0 4-2 4-5-3 0-4 2-4 5z"/>',
        "pill": '<rect x="3" y="8" width="18" height="8" rx="4" transform="rotate(-35 12 12)"/><path d="m9.5 8.5 5 7"/>',
    }[name]
    c = (' class="%s"' % cls) if cls else ""
    return ('<svg%s viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (c, p))

SOCIAL_SVG = {
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.1c0-1.22-.02-2.79-1.7-2.79-1.7 0-1.96 1.33-1.96 2.7V21h-4z"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.87.25-1.46 1.5-1.46h1.6V4.46A21 21 0 0 0 14.3 4.3c-2.3 0-3.8 1.4-3.8 3.95v2.25H8v3h2.5V21z"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.15l-.3-.18-3 .78.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.25-.12-1.46-.72-1.69-.8-.23-.08-.39-.12-.55.12-.16.25-.64.8-.78.96-.14.17-.29.19-.53.06a6.7 6.7 0 0 1-3.3-2.9c-.25-.43.25-.4.71-1.33.08-.16.04-.3-.02-.42l-.75-1.82c-.2-.48-.4-.41-.55-.42h-.47a.9.9 0 0 0-.65.3 2.7 2.7 0 0 0-.85 2c0 1.2.87 2.35.99 2.51.12.17 1.7 2.6 4.13 3.65 1.54.66 2.14.72 2.9.6.47-.07 1.46-.6 1.66-1.17.2-.58.2-1.07.14-1.17-.06-.1-.22-.17-.47-.29z"/></svg>',
}

def whatsapp_url(text="Hello Patriot Africa, I would like a quote."):
    from urllib.parse import quote
    return "https://wa.me/%s?text=%s" % (CONFIG["whatsapp"], quote(text))

# ---------------------------------------------------------------- corridor map
MAP_S = 20.0
def proj(lon, lat):
    return round((lon - 11.5) * MAP_S, 1), round((-lat - 4.0) * MAP_S, 1)

PLACES = {
    # key: (label, lon, lat, kind, label position)
    "ndola": ("Ndola", 28.64, -12.97, "hub", "r"),
    "kapiri": ("", 28.68, -14.0, "way", ""),
    "mpika": ("", 31.45, -11.83, "way", ""),
    "lusaka": ("Lusaka", 28.32, -15.39, "city", "l"),
    "kasumbalesa": ("Kasumbalesa", 27.80, -12.25, "border", "l"),
    "lubumbashi": ("Lubumbashi", 27.48, -11.66, "city", "l"),
    "kolwezi": ("Kolwezi", 25.47, -10.71, "city", "t"),
    "lobito": ("Lobito", 13.54, -12.35, "port", "b"),
    "tunduma": ("Tunduma", 32.77, -9.30, "border", "l"),
    "dar": ("Dar es Salaam", 39.28, -6.79, "port", "bl"),
    "chirundu": ("Chirundu", 28.85, -16.04, "border", "r"),
    "harare": ("Harare", 31.05, -17.83, "city", "r"),
    "mutare": ("Forbes", 32.67, -18.97, "border", "r"),
    "beira": ("Beira", 34.84, -19.84, "port", "r"),
    "beitbridge": ("Beitbridge", 30.0, -22.22, "border", "r"),
    "johannesburg": ("Johannesburg", 28.05, -26.20, "city", "l"),
    "durban": ("Durban", 31.02, -29.86, "port", "r"),
    "kazungula": ("Kazungula", 25.27, -17.79, "border", "b"),
    "katima": ("Katima Mulilo", 24.27, -17.50, "border", "tl"),
    "walvis": ("Walvis Bay", 14.51, -22.96, "port", "b"),
    "mwami": ("Mwami", 32.65, -13.64, "border", "t"),
    "lilongwe": ("Lilongwe", 33.79, -13.96, "city", "r"),
}
ROUTES = [
    # id, name, via, port, waypoints
    ("lobito", "Lobito Corridor", "Kasumbalesa, Lubumbashi, Kolwezi", "Atlantic",
     ["ndola", "kasumbalesa", "lubumbashi", "kolwezi", "lobito"]),
    ("dar", "Dar es Salaam Corridor", "Great North Road, Tunduma", "Indian Ocean",
     ["ndola", "kapiri", "mpika", "tunduma", "dar"]),
    ("beira", "Beira Corridor", "Chirundu, Harare, Forbes", "Indian Ocean",
     ["ndola", "kapiri", "lusaka", "chirundu", "harare", "mutare", "beira"]),
    ("south", "North South Corridor", "Chirundu, Beitbridge, Johannesburg", "Durban",
     ["ndola", "kapiri", "lusaka", "chirundu", "harare", "beitbridge", "johannesburg", "durban"]),
    ("walvis", "Walvis Bay Corridor", "Kazungula, Katima Mulilo", "Atlantic",
     ["ndola", "kapiri", "lusaka", "kazungula", "katima", "walvis"]),
    ("malawi", "Malawi route", "Lusaka, Mwami", "Lilongwe",
     ["ndola", "kapiri", "lusaka", "mwami", "lilongwe"]),
]
COUNTRY_LABELS = [("DRC", 23.2, -7.2), ("ANGOLA", 17.0, -15.6), ("ZAMBIA", 23.6, -14.6), ("TANZANIA", 34.0, -5.6),
                  ("MALAWI", 35.6, -12.0), ("MOZAMBIQUE", 36.6, -16.4), ("ZIMBABWE", 26.6, -20.6),
                  ("BOTSWANA", 22.8, -23.4), ("NAMIBIA", 17.4, -18.6), ("SOUTH AFRICA", 22.4, -29.2)]

def corridor_map(title_id="map-title"):
    out = ['<svg viewBox="0 0 600 560" role="img" aria-labelledby="%s">' % title_id,
           '<title id="%s">Schematic map of Patriot Africa road corridors from Ndola to Lobito, Dar es Salaam, Beira, Durban, Walvis Bay and Lilongwe</title>' % title_id]
    # graticule
    out.append('<g class="grat">')
    for lon in range(15, 41, 5):
        x, _ = proj(lon, 0)
        out.append('<line x1="%s" y1="0" x2="%s" y2="560"/>' % (x, x))
    for lat in range(-5, -31, -5):
        _, y = proj(0, lat)
        out.append('<line x1="0" y1="%s" x2="600" y2="%s"/>' % (y, y))
    out.append('</g>')
    for lon in range(15, 41, 5):
        x, _ = proj(lon, 0)
        out.append('<text class="grat-label" x="%s" y="552" text-anchor="middle">%d°E</text>' % (x, lon))
    for lat in range(-10, -31, -5):
        _, y = proj(0, lat)
        out.append('<text class="grat-label" x="6" y="%s">%d°S</text>' % (y - 4, -lat))
    for name, lon, lat in COUNTRY_LABELS:
        x, y = proj(lon, lat)
        out.append('<text class="grat-label" x="%s" y="%s" text-anchor="middle" style="letter-spacing:.22em">%s</text>' % (x, y, name))
    out.append('<text class="ocean" x="%s" y="%s" text-anchor="middle">ATLANTIC OCEAN</text>' % proj(14.6, -27.5))
    out.append('<text class="ocean" x="%s" y="%s" text-anchor="middle">INDIAN OCEAN</text>' % proj(37.6, -25.0))
    # routes: draw longest first so shared trunk segments stay visible
    for rid, _, _, _, pts in ROUTES:
        d = "M" + " L".join("%s %s" % proj(PLACES[p][1], PLACES[p][2]) for p in pts)
        out.append('<path class="route-shadow" d="%s"/>' % d)
    for rid, _, _, _, pts in ROUTES:
        d = "M" + " L".join("%s %s" % proj(PLACES[p][1], PLACES[p][2]) for p in pts)
        out.append('<path class="route" data-route="%s" d="%s"/>' % (rid, d))
    # nodes and labels
    for key, (label, lon, lat, kind, pos) in PLACES.items():
        if kind == "way":
            continue
        x, y = proj(lon, lat)
        if kind == "port":
            node = '<rect x="%s" y="%s" width="9" height="9"/>' % (x - 4.5, y - 4.5)
        elif kind == "hub":
            node = '<circle cx="%s" cy="%s" r="7.5"/>' % (x, y)
        elif kind == "border":
            node = '<circle cx="%s" cy="%s" r="3.6"/>' % (x, y)
        else:
            node = '<circle cx="%s" cy="%s" r="4.2"/>' % (x, y)
        out.append('<g class="node %s">%s</g>' % (kind, node))
        if not label:
            continue
        cls = "lbl-hub" if kind == "hub" else ("lbl-sm" if kind == "border" else "lbl")
        dx, dy, anchor = {"r": (11, 4, "start"), "l": (-10, 4, "end"), "t": (0, -11, "middle"),
                          "b": (0, 20, "middle"), "bl": (-6, 18, "end"), "tl": (-6, -9, "end")}[pos]
        if kind == "hub":
            dx, dy = 14, 6
        text = label
        out.append('<text class="%s" x="%s" y="%s" text-anchor="%s">%s</text>' % (cls, round(x + dx, 1), round(y + dy, 1), anchor, escape(text)))
    out.append('</svg>')
    return "".join(out)

def corridor_widget(start="lobito", heading_level="h3"):
    items = []
    for rid, name, via, port, _ in ROUTES:
        items.append('<li><button type="button" data-corridor="%s" aria-pressed="false">'
                     '<span class="name">%s</span><span class="via">Via %s</span><span class="port">%s</span></button></li>'
                     % (rid, escape(name), escape(via), escape(port)))
    return ('<div class="corridors" data-corridors data-start="%s">'
            '<div class="map">%s<div class="map-key"><span><i class="k-hub"></i>Ndola base</span><span><i class="k-port"></i>Port</span>'
            '<span><i class="k-border"></i>Border post</span><span>Schematic, not to scale</span></div></div>'
            '<div class="stack"><p class="list-label">Select a corridor</p>'
            '<ul class="corridor-list">%s</ul></div></div>') % (start, corridor_map(), "".join(items))

# ---------------------------------------------------------------- shared partials
NAV = [("services", "Services"), ("fleet", "Fleet"), ("coverage", "Routes"), ("industries", "Industries"), ("about", "About")]

def header(active):
    links = "".join('<li><a href="%s"%s>%s</a></li>' % (url(p), ' aria-current="page"' if p == active or (active == "lobito" and p == "coverage") else "", t) for p, t in NAV)
    mlinks = "".join('<li><a href="%s">%s %s</a></li>' % (url(p), t, icon("arrow")) for p, t in NAV)
    return """<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="%(home)s" aria-label="Patriot Africa home">
      %(mark)s%(word)s
    </a>
    <nav class="nav" aria-label="Main"><ul>%(links)s</ul></nav>
    <a class="btn btn--primary header-cta" href="%(quote)s" data-cta="header">Get a quote</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Menu">%(open)s%(close)s</button>
  </div>
  <div class="mobile-nav wrap" id="mobile-nav">
    <ul>%(mlinks)s</ul>
    <a class="btn btn--primary" href="%(quote)s" data-cta="mobile-menu">Get a quote</a>
  </div>
</header>""" % {
        "home": url("home"), "links": links, "mlinks": mlinks, "quote": url("quote"),
        "mark": img("mark", "", cls="mark", eager=True, width=38, height=38),
        "word": img("word", "Patriot Africa", cls="word", eager=True, width=150, height=9),
        "open": icon("menu", "open"), "close": icon("close", "close"),
    }

def footer():
    offices = "".join('<div><h2>%s</h2><address>%s<a href="mailto:%s">%s</a></address></div>'
                      % (o["region"], "".join('<span%s>%s</span>' % (' class="org"' if i == 0 else "", escape(l)) for i, l in enumerate(o["lines"])),
                         CONFIG["email"], CONFIG["email"])
                      for o in OFFICES)
    social = []
    if CONFIG["linkedin"]:
        social.append('<a href="%s" rel="noopener" target="_blank" aria-label="Patriot Africa on LinkedIn">%s</a>' % (CONFIG["linkedin"], SOCIAL_SVG["linkedin"]))
    if CONFIG["facebook"]:
        social.append('<a href="%s" rel="noopener" target="_blank" aria-label="Patriot Africa on Facebook">%s</a>' % (CONFIG["facebook"], SOCIAL_SVG["facebook"]))
    if CONFIG["whatsapp"]:
        social.append('<a href="%s" rel="noopener" target="_blank" aria-label="Message Patriot Africa on WhatsApp">%s</a>' % (whatsapp_url(), SOCIAL_SVG["whatsapp"]))
    return """<footer class="site-footer">
  <div class="wrap footer-top">
    <div class="footer-brand">
      <a class="brand" href="%(home)s" aria-label="Patriot Africa home">%(mark)s%(word)s</a>
      <p>Road freight from Ndola across Zambia and Southern Africa. Full and part loads for mining, construction, manufacturing and energy.</p>
    </div>
    <div><h2>Company</h2><ul>
      <li><a href="%(about)s">About us</a></li><li><a href="%(services)s">Services</a></li><li><a href="%(fleet)s">Fleet</a></li><li><a href="%(quote)s">Get a quote</a></li>
    </ul></div>
    <div><h2>Routes</h2><ul>
      <li><a href="%(coverage)s">All routes</a></li><li><a href="%(lobito)s">Lobito Corridor</a></li><li><a href="%(industries)s">Industries</a></li>
    </ul></div>
    %(offices)s
  </div>
  <div class="footer-bottom"><div class="wrap">
    <span>© <span id="year">2026</span> Patriot Africa. All rights reserved.</span>
    <span><a href="%(privacy)s">Privacy policy</a> · <a href="%(terms)s">Terms and conditions</a></span>
    <div class="social">%(social)s</div>
  </div></div>
</footer>""" % {
        "home": url("home"), "about": url("about"), "services": url("services"), "fleet": url("fleet"), "quote": url("quote"),
        "coverage": url("coverage"), "lobito": url("lobito"), "industries": url("industries"), "privacy": url("privacy"),
        "terms": url("terms"), "offices": offices, "social": "".join(social),
        "mark": img("mark", "", cls="mark", width=38, height=38), "word": img("word", "Patriot Africa", cls="word", width=150, height=9),
    }

def mobile_cta():
    wa = ""
    if CONFIG["whatsapp"]:
        wa = '<a class="btn btn--wa" href="%s" rel="noopener" target="_blank" data-cta="mobile-bar-wa">%s WhatsApp</a>' % (whatsapp_url(), SOCIAL_SVG["whatsapp"])
    return '<div class="mobile-cta"><a class="btn btn--primary" href="%s" data-cta="mobile-bar">Get a quote</a>%s</div>' % (url("quote"), wa)

def cta_band(title="Tell us what needs to move", lead=None):
    lead = lead or "Send the route, the cargo and the timing. We reply with a detailed, no obligation quote within one business day."
    wa = ""
    if CONFIG["whatsapp"]:
        wa = '<a class="btn btn--light" href="%s" rel="noopener" target="_blank" data-cta="band-wa">%s Message us on WhatsApp</a>' % (whatsapp_url(), SOCIAL_SVG["whatsapp"])
    phone = ('<span>Call <a href="tel:%s">%s</a></span>' % (re.sub(r"[^\d+]", "", CONFIG["phone"]), CONFIG["phone"])) if CONFIG["phone"] else ""
    return """<section class="cta-band" aria-labelledby="cta-title">
  <div class="cta-band__media">%s</div>
  <div class="wrap cta-band__inner">
    <p class="eyebrow">Get a quote</p>
    <h2 id="cta-title">%s</h2>
    <p class="lead">%s</p>
    <div class="btn-row"><a class="btn btn--primary" href="%s" data-cta="band">Request a quote %s</a>%s</div>
    <p class="contact-line"><span>Email <a href="mailto:%s">%s</a></span>%s</p>
  </div>
</section>""" % (img("night", "", sizes="100vw"), title, lead, url("quote"), icon("arrow", "arrow"), wa, CONFIG["email"], CONFIG["email"], phone)

def page_head(title, lead, eyebrow, crumbs, photo=None, extra=""):
    crumb_html = '<ol class="crumbs"><li><a href="%s">Home</a></li>%s</ol>' % (
        url("home"), "".join(('<li><a href="%s">%s</a></li>' % (url(p), t)) if p else ('<li aria-current="page">%s</li>' % t) for p, t in crumbs))
    media = ('<div class="page-head__media">%s</div>' % img(photo, "", sizes="100vw", eager=True)) if photo else ""
    return """<section class="page-head%s">%s<div class="wrap page-head__inner">%s<p class="eyebrow">%s</p><h1>%s</h1><p class="lead">%s</p>%s</div></section>""" % (
        " page-head--photo" if photo else "", media, crumb_html, eyebrow, title, lead, extra)

# ---------------------------------------------------------------- structured data
def org_ld():
    addresses = []
    for o in OFFICES:
        a = {"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"], "addressCountry": o["country"]}
        if o.get("postcode"):
            a["postalCode"] = o["postcode"]
        addresses.append(a)
    same = [u for u in (CONFIG["facebook"], CONFIG["linkedin"]) if u]
    org = {"@context": "https://schema.org", "@type": "Organization", "@id": CONFIG["base_url"] + "/#organization",
           "name": CONFIG["name"], "url": CONFIG["base_url"] + "/", "logo": img_abs("mark"), "email": CONFIG["email"],
           "description": "Road freight and haulage company based in Ndola, Zambia, moving full and part loads across Southern Africa.",
           "address": addresses, "areaServed": [{"@type": "Country", "name": c} for c in COUNTRIES], "sameAs": same}
    if CONFIG["phone"]:
        org["telephone"] = CONFIG["phone"]
    local = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": CONFIG["base_url"] + "/#ndola",
             "name": "Patriot Africa, Ndola", "parentOrganization": {"@id": CONFIG["base_url"] + "/#organization"},
             "image": img_abs("hero"), "email": CONFIG["email"], "url": CONFIG["base_url"] + "/",
             "address": addresses[0], "areaServed": [{"@type": "Country", "name": c} for c in COUNTRIES]}
    if CONFIG["phone"]:
        local["telephone"] = CONFIG["phone"]
    return [org, local]

def breadcrumb_ld(trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": canonical("home")}]
    for i, (p, t) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": t, "item": canonical(p)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]}

def faq_html(faqs):
    return '<div class="faq">%s</div>' % "".join(
        '<details><summary>%s</summary><div class="answer"><p>%s</p></div></details>' % (q, a) for q, a in faqs)

# ---------------------------------------------------------------- document assembly
FONTS = "https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&display=swap"

def version(name):
    """A short content hash added to asset links, so browsers fetch new files after every change."""
    if ARTIFACT:
        return ""
    import hashlib
    return "?v=" + hashlib.sha1(open(os.path.join(SRC, name), "rb").read()).hexdigest()[:10]

def document(page, title, description, body, ld=None, body_class="", og_image="hero", noindex=False):
    ld = ld or []
    is_index = ARTIFACT and page == "home"
    head = []
    head.append("<title>%s</title>" % escape("Patriot Africa Website" if is_index else title))
    if is_index:
        head.append('<meta name="claude:viewport-fit-sides" content="cover">')
    head.append('<meta name="description" content="%s">' % escape(description))
    if not ARTIFACT:
        head.append('<link rel="canonical" href="%s">' % canonical(page))
    if noindex:
        head.append('<meta name="robots" content="noindex">')
    head.append('<meta name="theme-color" content="#0b2540">')
    head.append('<meta property="og:type" content="website">')
    head.append('<meta property="og:site_name" content="Patriot Africa">')
    head.append('<meta property="og:locale" content="en_GB">')
    head.append('<meta property="og:title" content="%s">' % escape(title))
    head.append('<meta property="og:description" content="%s">' % escape(description))
    head.append('<meta property="og:url" content="%s">' % canonical(page))
    head.append('<meta property="og:image" content="%s">' % (CONFIG["base_url"] + "/og-image.jpg" if os.path.exists(os.path.join(LOCAL_IMG, "og-image.jpg")) else img_abs(og_image)))
    head.append('<meta name="twitter:card" content="summary_large_image">')
    head.append('<link rel="icon" href="%s" type="image/svg+xml">' % img_src("favicon")[0])
    if not ARTIFACT and os.path.exists(os.path.join(LOCAL_IMG, "apple-touch-icon.png")):
        head.append('<link rel="apple-touch-icon" href="/apple-touch-icon.png">')
        head.append('<link rel="manifest" href="/site.webmanifest">')
    head.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
    head.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    if not LOCAL:
        head.append('<link rel="preconnect" href="https://cdn.prod.website-files.com" crossorigin>')
    head.append('<link rel="stylesheet" href="%s">' % FONTS)
    head.append('<link rel="stylesheet" href="%s%s">' % (asset("assets/styles.css"), version("styles.css")))
    if CONFIG["ga4"] and not ARTIFACT:
        head.append('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>' % CONFIG["ga4"])
        head.append("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','%s');</script>" % CONFIG["ga4"])
    for block in ld:
        head.append('<script type="application/ld+json">%s</script>' % json.dumps(block, ensure_ascii=False, separators=(",", ":")))

    content = "%s\n<main id=\"main\">%s</main>\n%s\n%s\n<script src=\"%s%s\" defer></script>" % (
        header(page), body, footer(), mobile_cta() if page not in ("quote",) else "", asset("assets/site.js"), version("site.js"))

    if is_index:
        # the claude.ai preview wraps this file in its own document skeleton
        cls = "<script>document.body.classList.add(%s)</script>\n" % ", ".join(json.dumps(c) for c in (body_class + " overlay-header").split())
        return "\n".join(head) + "\n" + cls + content + "\n"
    body_class = (body_class + " overlay-header").strip()
    return ('<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n%s\n</head>\n'
            '<body class="%s">\n%s\n</body>\n</html>\n') % ("\n".join(head), body_class, content)

# ---------------------------------------------------------------- build
def build():
    import content
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    shutil.copy(os.path.join(SRC, "styles.css"), os.path.join(OUT, "assets", "styles.css"))
    shutil.copy(os.path.join(SRC, "site.js"), os.path.join(OUT, "assets", "site.js"))
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    if os.path.isdir(STATIC_IMG):
        for f in os.listdir(STATIC_IMG):
            shutil.copy(os.path.join(STATIC_IMG, f), os.path.join(OUT, "img", f))
    if LOCAL:
        dst = os.path.join(OUT, "img")
        for key, files in LOCAL.items():
            for _, f in files:
                shutil.copy(os.path.join(LOCAL_IMG, f), os.path.join(dst, f))
    written = []
    for page in PAGES:
        html = content.render(page)
        if ARTIFACT:
            name = "index.html" if page == "home" else SLUG[page] + ".html"
        else:
            name = "index.html" if page == "home" else SLUG[page] + ".html"
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(name)
    if not ARTIFACT:
        write_static_extras()
    print("Built %d pages into %s" % (len(written), OUT))

def write_static_extras():
    from datetime import date
    today = date.today().isoformat()
    urls = [p for p in PAGES if p != "404"]
    prio = {"home": "1.0", "quote": "0.9", "services": "0.9", "coverage": "0.8", "lobito": "0.8", "fleet": "0.8",
            "industries": "0.7", "about": "0.6", "privacy": "0.2", "terms": "0.2"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (canonical(p), today, prio[p]))
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % CONFIG["base_url"])
    # redirects keep old Webflow addresses working (Netlify and Cloudflare Pages read this file)
    open(os.path.join(OUT, "_redirects"), "w").write(
        "/contact          /quote             301\n"
        "/contact/         /quote             301\n"
        "/home             /                  301\n")
    open(os.path.join(OUT, "_headers"), "w").write(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n"
        "/assets/*\n  Cache-Control: public, max-age=604800\n\n/img/*\n  Cache-Control: public, max-age=31536000, immutable\n")
    manifest = {"name": "Patriot Africa", "short_name": "Patriot", "start_url": "/", "display": "standalone",
                "background_color": "#ffffff", "theme_color": "#0b2540",
                "icons": [{"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]}
    open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps(manifest, indent=2))
    for extra in ("apple-touch-icon.png", "og-image.jpg"):
        p = os.path.join(LOCAL_IMG, extra)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(OUT, extra))

if __name__ == "__main__":
    sys.path.insert(0, ROOT)
    build()
