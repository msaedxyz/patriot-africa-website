"""Page content for the Patriot Africa site. Text keeps the original site copy where it worked."""
from urllib.parse import quote as q
from build import (CONFIG, OFFICES, COUNTRIES, ROUTES, url, img, icon, document, page_head, cta_band, corridor_widget,
                   org_ld, breadcrumb_ld, faq_ld, faq_html, whatsapp_url, SOCIAL_SVG, escape)

ARROW = icon("arrow", "arrow")

# ---------------------------------------------------------------- shared data
SERVICES = [
    ("ftl", "FTL", "truck", "Full truckload", "A dedicated truck for your consignment, loaded at your site and driven straight to the destination with no stops to load other cargo."),
    ("ltl", "LTL", "layers", "Part load", "Pay only for the deck space you use. We combine compatible consignments on one truck, which suits smaller or regular shipments."),
    ("cross-border", "XB", "border", "Cross border haulage", "Freight between Zambia and the DRC, Tanzania, Malawi, Zimbabwe, Mozambique, Namibia, Angola and South Africa."),
    ("bulk", "BULK", "mine", "Bulk and mining cargo", "Metals, minerals, concentrates, grain and other dry bulk, plus heavy equipment and consumables for mine sites."),
    ("liquid", "LIQ", "drop", "Liquid cargo", "Tankers for fuel, chemicals and other liquid freight, including hazardous materials."),
    ("cold", "TEMP", "snow", "Temperature controlled", "Refrigerated trailers for food, pharmaceuticals and other perishable or sensitive goods."),
]

FLEET = [
    # key, image, name, category, summary, best for, cargo
    ("flatbed", "flatbed", "Flatbed", "Standard", "An open deck that loads from the top or the sides with a crane or forklift.",
     "Large, heavy or oversized loads", "Steel, machinery, mining equipment, building materials"),
    ("container", "container", "Container trailer", "Standard", "A skeletal or flat trailer that carries ISO containers between ports, depots and sites.",
     "A wide range of general cargo", "Containerised freight to and from Dar es Salaam, Beira, Durban and Walvis Bay"),
    ("tanker", "tanker", "Tanker", "Specialised", "A purpose built tank trailer for bulk liquids.",
     "Liquids and hazardous materials", "Fuel, lubricants, chemicals"),
    ("reefer", "reefer", "Refrigerated", "Specialised", "An insulated trailer with its own refrigeration unit that holds a set temperature for the whole trip.",
     "Temperature sensitive goods", "Food, pharmaceuticals, perishables"),
]
FLEET_TABLE = [
    ("Flatbed", "Standard", "Large, heavy or oversized loads", "Steel, machinery, building materials"),
    ("Interlink", "Standard", "High volumes on two linked trailers", "Bagged and bulk minerals, grain, cement"),
    ("Box trailer", "Standard", "Enclosed, secure transport of dry goods", "Packaged goods, spare parts, consumer goods"),
    ("Curtain side", "Standard", "Palletised cargo that loads from the side", "Pallets, bagged products, mixed cargo"),
    ("Rigid truck", "Standard", "Shorter routes and site deliveries", "General freight, local distribution"),
    ("Container trailer", "Standard", "Containers between ports, depots and sites", "Containerised import and export freight"),
    ("Tanker", "Specialised", "Liquids and hazardous materials", "Fuel, lubricants, chemicals"),
    ("Refrigerated", "Specialised", "Temperature sensitive goods", "Food, pharmaceuticals, perishables"),
    ("Side loader", "Specialised", "Lifting containers on and off without a crane at site", "Containers to mines and remote sites"),
]

INDUSTRIES = [
    ("mining", "mine", "Mining and metals", "Copper, cobalt and other metals out of the Copperbelt, and the equipment, spares and consumables that keep mine sites running.",
     ["Copper cathode", "Concentrates", "Mine consumables", "Heavy equipment"], ["Flatbed", "Interlink", "Side loader"]),
    ("construction", "crane", "Construction and infrastructure", "Steel, cement and machinery for road, energy and building projects, delivered to the site when the programme needs them.",
     ["Structural steel", "Cement", "Machinery", "Prefabricated units"], ["Flatbed", "Interlink", "Curtain side"]),
    ("manufacturing", "factory", "Manufacturing and industrial", "Raw materials into the plant and finished goods out to customers, on a regular schedule.",
     ["Raw materials", "Tools and machinery", "Industrial equipment"], ["Box trailer", "Curtain side", "Container trailer"]),
    ("energy", "bolt", "Energy and fuel", "Fuel and lubricants by tanker, and equipment for power and energy projects.",
     ["Fuel", "Lubricants", "Project equipment"], ["Tanker", "Flatbed"]),
    ("agriculture", "wheat", "Agriculture", "Grain, fertiliser and agricultural produce between farms, mills, depots and borders.",
     ["Grain", "Fertiliser", "Produce"], ["Interlink", "Curtain side", "Refrigerated"]),
    ("food-pharma", "pill", "Food and pharmaceuticals", "Temperature controlled transport for food and medicines that must stay within a set range from loading to delivery.",
     ["Chilled food", "Frozen food", "Pharmaceuticals"], ["Refrigerated", "Box trailer"]),
    ("chemicals", "flask", "Chemicals", "Liquid and packaged chemicals, including hazardous materials, in equipment built for the purpose.",
     ["Liquid chemicals", "Hazardous materials", "Packaged chemicals"], ["Tanker", "Box trailer"]),
]

WHY = [
    ("cargo", "Specialised logistics", "Handling for raw materials and sensitive cargo, with the right trailer chosen for each load."),
    ("pin", "Real time tracking", "Satellite powered shipment visibility, so you know where your cargo is between borders."),
    ("headset", "Customer support", "A 24/7 customer service team that you can reach while your cargo is on the road."),
    ("shield", "24/7 security", "Round the clock protection for your cargo, on the road and at rest."),
]

PARTNERS = [("p-reload", "Reload Logistics"), ("p-steinweg", "C. Steinweg Group"), ("p-nucleus", "Nucleus Mining Logistics"),
            ("p-msc", "MSC"), ("p-agl", "AGL Africa Global Logistics"), ("p-hass", "HASS"), ("p-etg", "ETG Curechem"),
            ("p-polytra", "Polytra")]

def pills(items, cls="pill"):
    return "".join('<span class="%s">%s</span>' % (cls, escape(i)) for i in items)

def stats_html():
    return """<div class="hero__proof" role="list">
  <div class="proof" role="listitem"><b>20<span>+</span></b><small>Years on the road</small></div>
  <div class="proof" role="listitem"><b>150<span>+</span></b><small>Trucks and trailers</small></div>
  <div class="proof" role="listitem"><b>10</b><small>Countries served</small></div>
  <div class="proof" role="listitem"><b>7</b><small>Key industries</small></div>
</div>"""

def partners_html():
    items = "".join('<li>%s</li>' % img(k, name, width=None) for k, name in PARTNERS)
    return """<section class="partners" aria-label="Partners">
  <div class="wrap partners__inner"><p class="mono">Partners we work with</p><ul>%s</ul></div>
</section>""" % items

def wa_button(cls="btn--light", label="WhatsApp", cta="hero-wa"):
    if not CONFIG["whatsapp"]:
        return ""
    return '<a class="btn %s" href="%s" rel="noopener" target="_blank" data-cta="%s">%s %s</a>' % (cls, whatsapp_url(), cta, SOCIAL_SVG["whatsapp"], label)

def fleet_tabs():
    tabs, panels = [], []
    for i, (key, im, name, cat, summary, best, cargo) in enumerate(FLEET):
        tabs.append('<button type="button" role="tab" id="tab-%s" aria-controls="panel-%s" aria-selected="%s">%s</button>'
                    % (key, key, "true" if i == 0 else "false", name))
        panels.append("""<div class="fleet-panel" role="tabpanel" id="panel-%(key)s" aria-labelledby="tab-%(key)s">
  <div class="rig"><span class="tag">%(cat)s</span>%(img)s</div>
  <div class="spec">
    <h3>%(name)s</h3><p>%(summary)s</p>
    <dl><dt>Best for</dt><dd>%(best)s</dd><dt>Typical cargo</dt><dd>%(cargo)s</dd><dt>Category</dt><dd>%(cat)s fleet</dd></dl>
    <a class="link-arrow" href="%(quote)s">Quote with a %(lname)s %(arrow)s</a>
  </div>
</div>""" % {"key": key, "cat": cat, "name": name, "summary": summary, "best": best, "cargo": cargo,
             "img": img(im, "Side view of a Patriot Africa %s truck" % name.lower(), sizes="(min-width: 960px) 680px, 100vw"),
             "quote": url("quote"), "lname": name.lower(), "arrow": ARROW})
    return '<div class="fleet" data-tabs><div class="fleet-tabs" role="tablist" aria-label="Truck types">%s</div>%s</div>' % ("".join(tabs), "".join(panels))

def loads_html():
    return """<div class="loads">
  <article class="load load--ltl">
    <div class="load__art">%s</div>
    <div class="load__body">
      <p class="eyebrow">LTL</p><h3>Part load</h3>
      <p>Less than truckload. Your consignment shares a truck with other compatible cargo, so you pay only for the space you use.</p>
      <ul class="ticks"><li>Smaller or regular shipments</li><li>Lower cost per consignment</li><li>Palletised, bagged and packaged goods</li></ul>
    </div>
  </article>
  <article class="load load--ftl">
    <div class="load__art">%s</div>
    <div class="load__body">
      <p class="eyebrow">FTL</p><h3>Full load</h3>
      <p>Full truckload. A dedicated truck carries only your cargo, from your gate to the destination, on your schedule.</p>
      <ul class="ticks"><li>Large, heavy or high value consignments</li><li>Fewer handling points</li><li>Direct transit across borders</li></ul>
    </div>
  </article>
</div>""" % (img("ltl", "Illustration of a truck carrying several different containers, which shows a part load", sizes="(min-width: 880px) 720px, 110vw"),
             img("ftl", "Illustration of a truck carrying one long container, which shows a full load", sizes="(min-width: 880px) 720px, 110vw"))

# ---------------------------------------------------------------- home
def home():
    svc = "".join("""<a class="svc" href="%s" data-reveal>
  <span class="ico">%s</span><span class="code">%s</span><h3>%s</h3><p>%s</p><span class="link-arrow">Learn more %s</span>
</a>""" % (url("services", k), icon(ic), code, t, d, ARROW) for k, code, ic, t, d in SERVICES)

    ind = "".join("""<a class="ind ind--link" href="%s" data-reveal>
  <span class="code">%s</span><h3>%s</h3><p>%s</p></a>""" % (url("industries", k), ", ".join(cargo[:2]), name, d.split(". ")[0].rstrip(".") + ".")
        for k, ic, name, d, cargo, eq in INDUSTRIES)

    why = "".join('<div>%s<h3>%s</h3><p>%s</p></div>' % (icon(ic), t, d) for ic, t, d in WHY)

    routes = ["Ndola", "Lubumbashi", "Kolwezi", "Lobito", "Dar es Salaam", "Beira", "Harare", "Johannesburg", "Durban", "Walvis Bay", "Lilongwe"]
    strip = "".join('<li><b>Ndola</b><span class="dash"></span>%s</li>' % r for r in routes[1:])

    body = """
<section class="hero" aria-labelledby="hero-title">
  <div class="hero__media">%(hero)s</div>
  <div class="wrap hero__inner">
    <p class="tagline">Moving you forward one mile at a time</p>
    <h1 id="hero-title">Road freight across Zambia and Southern Africa</h1>
    <p class="lead">Full and part loads for mining, construction, manufacturing and energy. Our own fleet runs from Ndola across ten countries and to the region's main ports.</p>
    <div class="btn-row">
      <a class="btn btn--primary" href="%(quote)s" data-cta="hero">Get a quote %(arrow)s</a>
      <a class="btn btn--light" href="%(fleet)s" data-cta="hero-fleet">See our fleet</a>
      %(wa)s
    </div>
    %(stats)s
  </div>
</section>
<div class="routes-strip" aria-label="Routes from Ndola"><div class="wrap"><ul>%(strip)s</ul></div></div>
%(partners)s

<section class="section" aria-labelledby="about-title">
  <div class="wrap split">
    <div class="copy" data-reveal>
      <p class="eyebrow">Who we are</p>
      <h2 class="h2" id="about-title">Your partner in logistics</h2>
      <p>We are a team of logistics specialists who have moved cargo across Africa's most demanding roads for more than two decades. That experience lets us deliver efficient, tailored transport for mining, manufacturing, construction and energy. Whether it is raw materials or industrial cargo, we get your goods to their destination safely and on time.</p>
      <p>Our approach rests on long relationships. We plan each load with you, keep you informed on the road, and stay invested in the growth of the businesses we serve.</p>
      <ul class="facts">
        <li><b>Ndola, Zambia</b><span>Head office and depot</span></li>
        <li><b>London, UK</b><span>Commercial office</span></li>
        <li><b>Full and part loads</b><span>FTL and LTL</span></li>
        <li><b>Bulk, liquid, general</b><span>and temperature controlled</span></li>
      </ul>
      <p><a class="link-arrow" href="%(about)s">More about us %(arrow)s</a></p>
    </div>
    <div class="photo-pair" data-reveal>
      <figure>%(gravel)s</figure>
      <figure>%(mountain)s</figure>
    </div>
  </div>
</section>

<section class="section section--dust" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div class="stack"><p class="eyebrow">Services</p><h2 class="h2" id="svc-title">Freight services built around your cargo</h2></div>
      <p class="lead">From one pallet to a convoy of interlinks, we match the truck, the route and the timing to what you need to move.</p>
    </div>
    <div class="svc-grid">%(svc)s</div>
  </div>
</section>

<section class="section" aria-labelledby="loads-title">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div class="stack"><p class="eyebrow">Load types</p><h2 class="h2" id="loads-title">Full load or part load</h2></div>
      <p class="lead">Whether it is less than truckload or full truckload, we have the right option to keep your business moving.</p>
    </div>
    %(loads)s
  </div>
</section>

<section class="section section--dust" aria-labelledby="fleet-title">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div class="stack"><p class="eyebrow">Our fleet</p><h2 class="h2" id="fleet-title">Built for every cargo</h2></div>
      <p class="lead">Flatbed, interlink, box and curtain side trailers and rigid trucks form the core of the fleet. Tankers, refrigerated trailers and side loaders cover specialised cargo.</p>
    </div>
    %(tabs)s
    <p style="margin-top:2rem"><a class="link-arrow" href="%(fleet)s">See the full fleet %(arrow)s</a></p>
  </div>
</section>

<section class="section section--plain" aria-labelledby="reach-title">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div class="stack"><p class="eyebrow">Our reach</p><h2 class="h2" id="reach-title">On the move across Southern Africa</h2></div>
      <p class="lead">From Ndola we run the region's main trade corridors: north into the DRC, east to the Indian Ocean, south to South Africa and west to the Atlantic.</p>
    </div>
    %(corridors)s
    <p style="margin-top:2rem"><a class="link-arrow" href="%(coverage)s">Routes and coverage %(arrow)s</a></p>
  </div>
</section>

<section class="section section--dust" aria-labelledby="ind-title">
  <div class="wrap">
    <div class="ind-grid ind-grid--4">
      <div class="stack" style="align-content:start"><p class="eyebrow">Industries</p><h2 class="h2" id="ind-title">The sectors we serve</h2>
        <p class="muted">Seven industries, each with its own cargo, equipment and timing.</p>
        <a class="link-arrow" href="%(industries)s">All industries %(arrow)s</a></div>
      %(ind)s
    </div>
  </div>
</section>

<section class="section section--forest" aria-labelledby="why-title">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Why choose us</p><h2 class="h2" id="why-title">What you can expect on every load</h2></div>
    <div class="why">%(why)s</div>
  </div>
</section>
%(cta)s
""" % {
        "hero": img("hero", "Patriot Africa truck with twin trailers on a mountain highway at sunrise", sizes="100vw", priority=True),
        "quote": url("quote"), "fleet": url("fleet"), "about": url("about"), "coverage": url("coverage"), "industries": url("industries"),
        "arrow": ARROW, "wa": wa_button(), "stats": stats_html(), "strip": strip, "partners": partners_html(),
        "gravel": img("gravel", "Patriot Africa tanker raising dust on a gravel road", sizes="(min-width: 960px) 340px, 55vw"),
        "mountain": img("mountain", "Blue Patriot Africa truck on a highway below mountains", sizes="(min-width: 960px) 260px, 42vw"),
        "svc": svc, "loads": loads_html(), "tabs": fleet_tabs(), "corridors": corridor_widget("lobito"), "ind": ind, "why": why, "cta": cta_band(),
    }
    return document("home", "Road Freight and Haulage in Zambia and Southern Africa | Patriot Africa",
                    "Patriot Africa moves full and part loads from Ndola to ten countries in Southern Africa. Trucking for mining, construction, manufacturing and energy. Get a quote in one business day.",
                    body, ld=org_ld(), body_class="is-home")

# ---------------------------------------------------------------- services
SERVICE_DETAIL = {
    "ftl": ("A dedicated truck, loaded once and driven direct.",
            ["Large or heavy consignments", "High value cargo that should not be handled twice", "Fixed delivery windows at sites and ports"],
            ["Flatbed", "Interlink", "Box trailer", "Curtain side", "Container trailer"]),
    "ltl": ("Share the truck, share the cost.",
            ["Smaller or regular shipments", "Palletised, bagged or packaged goods", "Customers who want lower cost per consignment"],
            ["Curtain side", "Box trailer", "Rigid truck"]),
    "cross-border": ("One carrier from loading point to destination, across every border on the route.",
                     ["Copperbelt to Lubumbashi and Kolwezi", "Port routes to Dar es Salaam, Beira, Durban, Walvis Bay and Lobito", "Malawi, Zimbabwe and Namibia"],
                     ["Every vehicle in the fleet"]),
    "bulk": ("Raw materials and mine supply, moved in volume.",
             ["Metals, minerals and concentrates", "Grain and other dry bulk", "Mine equipment, spares and consumables"],
             ["Interlink", "Flatbed", "Side loader"]),
    "liquid": ("Tankers for fuel, chemicals and other liquids.",
               ["Fuel and lubricants", "Liquid chemicals", "Hazardous materials"],
               ["Tanker"]),
    "cold": ("A set temperature from loading to delivery.",
             ["Chilled and frozen food", "Pharmaceuticals", "Other perishable or sensitive goods"],
             ["Refrigerated trailer", "Box trailer"]),
}
SERVICE_FAQ = [
    ("What is the difference between FTL and LTL?",
     "FTL means full truckload. A truck carries only your cargo and drives direct. LTL means less than truckload. Your cargo shares a truck with other compatible consignments and you pay for the space you use."),
    ("Which countries do you cover?",
     "We move cargo within Zambia and to the Democratic Republic of the Congo, the Republic of the Congo, Tanzania, Malawi, Zimbabwe, Mozambique, Namibia, Angola and South Africa."),
    ("How quickly will I get a quote?",
     "Send the quote form and we reply with a detailed, no obligation estimate within one business day."),
    ("What do you need from me to price a load?",
     "The collection point and destination, the type of cargo, the approximate weight and size, the date you need it moved, and any special handling such as hazardous classification or a temperature range."),
    ("Do you move hazardous materials?",
     "Yes. Our tankers are built for liquids and hazardous materials. Give us the UN number and hazard class on the quote form so we can plan the right equipment and documents."),
    ("Can I track my shipment?",
     "Yes. The fleet uses satellite powered tracking, and our customer service team can tell you where your cargo is at any time."),
]

def services():
    blocks = []
    imgs = {"ftl": "ftl", "ltl": "ltl", "bulk": "flatbed", "liquid": "tanker", "cold": "reefer", "cross-border": "container"}
    for k, code, ic, title, desc in SERVICES:
        sub, suits, equip = SERVICE_DETAIL[k]
        art = img(imgs[k], "Illustration of a %s truck" % title.lower(), sizes="(min-width: 960px) 620px, 100vw")
        blocks.append("""<article class="detail" id="%(k)s" data-reveal>
  <div class="detail__head"><p class="eyebrow">%(code)s</p><h2>%(title)s</h2><p class="muted">%(sub)s</p>
    <p><a class="btn btn--primary" href="%(quote)s?cargo=%(qc)s" data-cta="svc-%(k)s">Quote for %(ltitle)s</a></p></div>
  <div class="detail__body">
    <figure class="detail__figure rig-mini">%(art)s</figure>
    <p>%(desc)s</p>
    <div class="two-col">
      <div class="box"><h3>Suits</h3><ul class="ticks">%(suits)s</ul></div>
      <div class="box"><h3>Equipment</h3><ul class="ticks">%(equip)s</ul></div>
    </div>
  </div>
</article>""" % {"k": k, "code": code, "title": title, "ltitle": title.lower(), "sub": sub, "desc": desc, "art": art,
                 "quote": url("quote"), "qc": q(title), "suits": "".join("<li>%s</li>" % s for s in suits),
                 "equip": "".join("<li>%s</li>" % s for s in equip)})
    jump = "".join('<a class="pill" style="text-decoration:none" href="#%s">%s</a>' % (k, t) for k, _, _, t, _ in SERVICES)
    body = page_head("Freight services across Southern Africa",
                     "Full loads, part loads and specialised transport for bulk, liquid and temperature controlled cargo, within Zambia and across its borders.",
                     "Services", [(None, "Services")], photo="hero",
                     extra='<div class="btn-row"><a class="btn btn--primary" href="%s" data-cta="svc-head">Get a quote %s</a></div>' % (url("quote"), ARROW)) + """
<section class="section">
  <div class="wrap">
    <nav aria-label="Services on this page" class="choice" style="margin-bottom:3rem">%s</nav>
    %s
  </div>
</section>
<section class="section section--dust" aria-labelledby="faq-title">
  <div class="wrap split" style="align-items:start">
    <div class="stack"><p class="eyebrow">Questions</p><h2 class="h2" id="faq-title">Frequently asked questions</h2>
      <p class="muted">Cannot find what you need? Our team will answer any question about services, routes or logistics. Email <a href="mailto:%s">%s</a>.</p></div>
    %s
  </div>
</section>
%s""" % (jump, "".join(blocks), CONFIG["email"], CONFIG["email"], faq_html(SERVICE_FAQ), cta_band())
    svc_ld = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": t, "description": d, "serviceType": "Road freight",
                                                            "provider": {"@id": CONFIG["base_url"] + "/#organization"},
                                                            "areaServed": [{"@type": "Country", "name": c} for c in COUNTRIES]}}
        for i, (k, _, _, t, d) in enumerate(SERVICES)]}
    return document("services", "Freight Services: FTL, LTL and Cross Border Haulage | Patriot Africa",
                    "Full truckload, part load, cross border haulage, bulk and mining cargo, tankers and refrigerated transport across Zambia, the DRC and Southern Africa.",
                    body, ld=[breadcrumb_ld([("services", "Services")]), svc_ld, faq_ld(SERVICE_FAQ)])

# ---------------------------------------------------------------- fleet
def fleet():
    rows = "".join('<tr><th scope="row">%s</th><td><span class="pill%s">%s</span></td><td>%s</td><td>%s</td></tr>'
                   % (n, " pill--spec" if c == "Specialised" else "", c, b, t) for n, c, b, t in FLEET_TABLE)
    body = page_head("A fleet built for every cargo",
                     "More than 150 trucks and trailers, from flatbeds and interlinks to tankers and refrigerated units. Every vehicle carries satellite tracking.",
                     "Fleet", [(None, "Fleet")]) + """
<section class="section section--dust">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div class="stack"><p class="eyebrow">Main equipment</p><h2 class="h2">Choose the right truck</h2></div>
      <p class="lead">Select a truck type to see what it carries best. Not sure which you need? Describe the cargo on the quote form and we will advise.</p>
    </div>
    %s
  </div>
</section>
<section class="section" aria-labelledby="all-title">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div class="stack"><p class="eyebrow">Full fleet</p><h2 class="h2" id="all-title">Standard and specialised vehicles</h2></div>
      <p class="lead">Standard trucks and trailers form the backbone of the fleet. Purpose built trailers and articulated trucks cover cargo with specific needs.</p>
    </div>
    <div class="table-wrap"><table class="fleet-table">
      <caption class="sr-only">Patriot Africa fleet by vehicle type</caption>
      <thead><tr><th scope="col">Vehicle</th><th scope="col">Category</th><th scope="col">Best for</th><th scope="col">Typical cargo</th></tr></thead>
      <tbody>%s</tbody>
    </table></div>
  </div>
</section>
<section class="section section--dust">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Load types</p><h2 class="h2">Full load or part load</h2></div>
    %s
  </div>
</section>
%s""" % (fleet_tabs(), rows, loads_html(), cta_band("Not sure which truck you need?", "Describe the cargo and the route. We will choose the right vehicle and send a detailed quote within one business day."))
    return document("fleet", "Our Fleet: Flatbed, Interlink, Tanker and Refrigerated Trucks | Patriot Africa",
                    "More than 150 trucks and trailers: flatbed, interlink, box, curtain side, rigid, container, tanker, refrigerated and side loader. Satellite tracked across Southern Africa.",
                    body, ld=[breadcrumb_ld([("fleet", "Fleet")])])

# ---------------------------------------------------------------- coverage
CORRIDOR_CARDS = [
    ("DRC Copperbelt", "Ndola · Kasumbalesa · Lubumbashi · Kolwezi", "The busiest cross border route in the region. Mine supply in, metals and concentrates out.", False),
    ("Lobito Corridor", "Copperbelt · Kolwezi · Lobito", "Road haulage for the projects and traders that use the Atlantic route through Angola.", True),
    ("Dar es Salaam", "Ndola · Great North Road · Tunduma", "The main Indian Ocean gateway for Zambian imports and exports.", False),
    ("Beira", "Lusaka · Chirundu · Harare · Forbes", "The shortest sea route east, through Zimbabwe to Mozambique.", False),
    ("North South", "Chirundu · Beitbridge · Johannesburg · Durban", "Road freight to and from South Africa's industrial centre and its largest port.", False),
    ("Walvis Bay", "Kazungula · Katima Mulilo · Walvis Bay", "The Atlantic route through Namibia on the Trans Caprivi Highway.", False),
    ("Malawi", "Lusaka · Mwami · Lilongwe", "Regular freight between Zambia and Malawi.", False),
    ("Within Zambia", "Copperbelt · Lusaka · North Western", "Domestic haulage between mines, plants, depots and towns.", False),
]

def coverage():
    cards = []
    for name, line, d, feat in CORRIDOR_CARDS:
        link = ('<a class="link-arrow" href="%s" >Lobito Corridor haulage %s</a>' % (url("lobito"), ARROW)) if feat else ""
        cards.append('<article class="cor-card%s" data-reveal><div class="line"><i></i>%s</div><h3>%s</h3><p>%s</p>%s</article>'
                     % (" cor-card--feature" if feat else "", line, name, d, link))
    chips = "".join("<li>%s</li>" % c for c in COUNTRIES)
    body = page_head("Routes and coverage",
                     "From our base in Ndola we move cargo within Zambia and to nine other countries, with road access to six ports on two oceans.",
                     "Our reach", [(None, "Routes")]) + """
<section class="section section--plain" aria-labelledby="map-h">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div class="stack"><p class="eyebrow">Corridor map</p><h2 class="h2" id="map-h">Our main corridors</h2></div>
      <p class="lead">Select a corridor to see the route and the border posts it crosses.</p>
    </div>
    %s
  </div>
</section>
<section class="section section--dust" aria-labelledby="cor-h">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Corridors</p><h2 class="h2" id="cor-h">Where we run</h2></div>
    <div class="cor-cards cor-cards--4">%s</div>
  </div>
</section>
<section class="section" aria-labelledby="countries-h">
  <div class="wrap split" style="align-items:start">
    <div class="stack"><p class="eyebrow">Countries</p><h2 class="h2" id="countries-h">Ten countries, one carrier</h2>
      <p class="muted">Each route we run connects the region's industries to their markets and ports. Wherever your cargo needs to go, we plan it with the same care.</p></div>
    <ul class="countries">%s</ul>
  </div>
</section>
%s""" % (corridor_widget("lobito"), "".join(cards), chips, cta_band("Need a route we have not listed?", "Tell us the origin and destination. If the road goes there, we will plan it and send a quote within one business day."))
    return document("coverage", "Routes and Coverage: Zambia, DRC and Southern Africa Corridors | Patriot Africa",
                    "Road freight from Ndola on the region's main corridors: Lubumbashi and Kolwezi, Lobito, Dar es Salaam, Beira, Durban, Walvis Bay and Lilongwe.",
                    body, ld=[breadcrumb_ld([("coverage", "Routes")])])

# ---------------------------------------------------------------- lobito corridor
LOBITO_FAQ = [
    ("What is the Lobito Corridor?",
     "The Lobito Corridor is the trade route that links the copper and cobalt mines of Zambia and the DRC to the Atlantic port of Lobito in Angola, by rail and by road."),
    ("Which loads do you move on the corridor?",
     "Road haulage only. We move construction materials, steel, machinery and mine supply towards the projects, and metals and concentrates towards the rail terminals and the port."),
    ("Do you run short road legs as well as full routes?",
     "Yes. We quote full road routes from the Copperbelt to Lobito, and shorter road legs between mine sites, rail terminals and border posts."),
    ("How do I get a quote?",
     "Send the quote form with the collection point, the destination, the cargo and the timing. We reply with a detailed quote within one business day."),
]

def lobito():
    who = [("Mines", "Inbound equipment, spares and consumables, and outbound metals and concentrates."),
           ("EPC contractors", "Steel, machinery and materials delivered to site on the project programme."),
           ("Commodity traders", "Road legs that connect mine output to rail terminals and the port."),
           ("Construction firms", "Materials and plant for road, rail and building works along the route."),
           ("Freight forwarders", "A reliable road carrier for the legs your clients need moved.")]
    cells = "".join('<div class="ind" data-reveal><h3>%s</h3><p>%s</p></div>' % (t, d) for t, d in who)
    body = page_head("Road haulage on the Lobito Corridor",
                     "The Lobito Corridor links the Copperbelt of Zambia and the DRC to the Atlantic port of Lobito in Angola. We provide road haulage for the companies that build and use it.",
                     "Lobito Corridor", [("coverage", "Routes"), (None, "Lobito Corridor")], photo="gravel",
                     extra='<div class="btn-row"><a class="btn btn--primary" href="%s?destination=Lobito" data-cta="lobito-head">Quote a Lobito load %s</a>%s</div>' % (url("quote"), ARROW, wa_button(cta="lobito-wa"))) + """
<section class="section section--dust" aria-labelledby="who-h">
  <div class="wrap">
    <div class="ind-grid ind-grid--3">
      <div class="stack" style="align-content:start"><p class="eyebrow">Who we work with</p><h2 class="h2" id="who-h">Haulage for the corridor's builders and users</h2></div>
      %s
    </div>
  </div>
</section>
<section class="section section--plain" aria-labelledby="route-h">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div class="stack"><p class="eyebrow">The route</p><h2 class="h2" id="route-h">From the Copperbelt to the Atlantic</h2></div>
      <p class="lead">Our road route leaves Ndola, crosses into the DRC at Kasumbalesa and runs through Lubumbashi and Kolwezi towards Angola and the port of Lobito.</p>
    </div>
    %s
  </div>
</section>
<section class="section section--dust" aria-labelledby="move-h">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Cargo</p><h2 class="h2" id="move-h">What we move</h2></div>
    <div class="two-col">
      <div class="box"><h3>Towards the projects</h3><ul class="ticks"><li>Structural steel and rail materials</li><li>Construction machinery and plant</li><li>Cement and building materials</li><li>Mine equipment, spares and consumables</li></ul></div>
      <div class="box"><h3>Towards the port</h3><ul class="ticks"><li>Copper cathode</li><li>Concentrates</li><li>Other metals and minerals</li><li>Containerised cargo</li></ul></div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="lfaq-h">
  <div class="wrap split" style="align-items:start">
    <div class="stack"><p class="eyebrow">Questions</p><h2 class="h2" id="lfaq-h">Lobito Corridor questions</h2></div>
    %s
  </div>
</section>
%s""" % (cells, corridor_widget("lobito"), faq_html(LOBITO_FAQ), cta_band("Planning a load on the Lobito Corridor?", "Send the collection point, the destination and the cargo. We reply with a detailed quote within one business day."))
    return document("lobito", "Lobito Corridor Trucking and Road Haulage | Patriot Africa",
                    "Road haulage on the Lobito Corridor from the Zambian and DRC Copperbelt to Lobito, Angola. For mines, EPC contractors, commodity traders, construction firms and forwarders.",
                    body, ld=[breadcrumb_ld([("coverage", "Routes"), ("lobito", "Lobito Corridor")]), faq_ld(LOBITO_FAQ)], og_image="gravel")

# ---------------------------------------------------------------- industries
def industries():
    blocks = []
    for k, ic, name, d, cargo, eq in INDUSTRIES:
        blocks.append("""<article class="detail" id="%s" data-reveal>
  <div class="detail__head"><span class="ind-ico">%s</span>
    <h2>%s</h2><p class="muted">%s</p></div>
  <div class="detail__body">
    <div class="two-col">
      <div class="box"><h3>Typical cargo</h3><div class="cargo" style="display:flex;flex-wrap:wrap;gap:.4rem">%s</div></div>
      <div class="box"><h3>Equipment</h3><div class="cargo" style="display:flex;flex-wrap:wrap;gap:.4rem">%s</div></div>
    </div>
    <p><a class="link-arrow" href="%s?cargo=%s">Get a quote for %s %s</a></p>
  </div>
</article>""" % (k, icon(ic), name, d, pills(cargo), pills(eq, "pill pill--spec"),
                 url("quote"), q(name), name.lower(), ARROW))
    body = page_head("The industries we serve",
                     "Mining, construction, manufacturing, energy, agriculture, food and pharmaceuticals, and chemicals. Each has its own cargo, equipment and timing, and we plan for all three.",
                     "Industries", [(None, "Industries")], photo="gravel") + """
<section class="section"><div class="wrap">%s</div></section>
<section class="section section--dust" aria-labelledby="cust-h">
  <div class="wrap split" style="align-items:start">
    <div class="stack"><p class="eyebrow">Also working with</p><h2 class="h2" id="cust-h">Traders and forwarders</h2></div>
    <div class="stack"><p class="lead">Commodity traders and freight forwarders use us as their road carrier for the legs between mines, plants, depots, borders and ports.</p>
      <p><a class="link-arrow" href="%s">See our routes %s</a></p></div>
  </div>
</section>
%s""" % ("".join(blocks), url("coverage"), ARROW, cta_band())
    return document("industries", "Industries: Mining, Construction, Energy and Agriculture Logistics | Patriot Africa",
                    "Road freight for mining and metals, construction, manufacturing, energy and fuel, agriculture, food and pharmaceuticals, and chemicals across Southern Africa.",
                    body, ld=[breadcrumb_ld([("industries", "Industries")])])

# ---------------------------------------------------------------- about
def about():
    offices = "".join('<div class="box"><h3>%s</h3><address style="font-style:normal;display:grid;gap:.15rem"><b style="font-family:var(--f-display);font-stretch:112%%;font-size:1.1rem">%s</b>%s</address><p><a class="link-arrow" href="mailto:%s">%s</a></p></div>'
                      % (o["label"], o["lines"][-1] if o["country"] == "ZM" else "London", "".join("<span>%s</span>" % l for l in o["lines"]), CONFIG["email"], CONFIG["email"]) for o in OFFICES)
    values = [("Relationships", "We build long partnerships. Many of our customers have moved cargo with us for years, and we plan each load with them."),
              ("Safety", "Safe drivers, maintained vehicles and secure cargo come before speed on every route."),
              ("Reliability", "We commit to a delivery time and we tell you early if anything on the road changes it.")]
    body = page_head("Moving Africa forward, one mile at a time",
                     "For more than twenty years our team has moved cargo across Africa's most demanding roads, from our base in Ndola on the Zambian Copperbelt.",
                     "About us", [(None, "About")], photo="mountain") + """
<section class="section">
  <div class="wrap split">
    <div class="copy">
      <p class="eyebrow">Who we are</p>
      <h2 class="h2">Your partner in logistics</h2>
      <p>We are a team of logistics specialists who have moved diverse cargo across Africa's challenging landscapes for more than two decades. Our experience lets us deliver efficient, tailored transport for vital sectors, including mining, manufacturing, construction and energy. Whether it is raw materials or industrial cargo, we get your goods to their destination safely and on time.</p>
      <p>At the core of our approach is the long relationship. Our service does more than move goods. It supports progress across the continent. With us as your logistics partner, you gain a carrier that is invested in your growth.</p>
    </div>
    <div class="photo-pair"><figure>%s</figure><figure>%s</figure></div>
  </div>
</section>
<section class="section section--forest section--tight" aria-label="Patriot Africa in numbers">
  <div class="wrap">%s</div>
</section>
<section class="section" aria-labelledby="values-h">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">How we work</p><h2 class="h2" id="values-h">What we stand for</h2></div>
    <div class="ind-grid ind-grid--3">%s</div>
  </div>
</section>
%s
<section class="section section--dust" aria-labelledby="off-h">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Offices</p><h2 class="h2" id="off-h">Where to find us</h2></div>
    <div class="two-col">%s</div>
  </div>
</section>
%s""" % (img("gravel", "Patriot Africa tanker on a gravel road", sizes="(min-width: 960px) 340px, 55vw"),
         img("night", "Patriot Africa truck with headlights on at dusk", sizes="(min-width: 960px) 260px, 42vw"),
         stats_html().replace('class="hero__proof"', 'class="hero__proof" style="margin-top:0"'),
         "".join('<div class="ind"><h3>%s</h3><p>%s</p></div>' % v for v in values),
         partners_html(), offices, cta_band())
    return document("about", "About Patriot Africa: Road Freight Specialists in Ndola, Zambia",
                    "More than twenty years of road freight across Southern Africa. Patriot Africa is based in Ndola, Zambia, with an office in London.",
                    body, ld=[breadcrumb_ld([("about", "About")])] + org_ld(), og_image="mountain")

# ---------------------------------------------------------------- quote
CARGO_OPTIONS = ["General freight", "Raw materials (metals, minerals)", "Industrial goods and machinery", "Dry bulk",
                 "Liquid cargo", "Temperature controlled", "Mixed cargo", "Oversized or heavy load", "Containers", "Other"]

def quote():
    import build
    use_netlify = CONFIG.get("netlify_forms") and not build.ARTIFACT and not CONFIG["form_endpoint"]
    endpoint = "/" if use_netlify else ("" if build.ARTIFACT else CONFIG["form_endpoint"])
    netlify = 'data-netlify="true" netlify-honeypot="company_url" ' if use_netlify else ""
    hidden = ('<input type="hidden" name="form-name" value="quote">'
              '<p class="hp" hidden><label>Leave this empty <input name="company_url" tabindex="-1" autocomplete="off"></label></p>') if use_netlify else (
             '<p class="hp" hidden><label>Leave this empty <input name="_gotcha" tabindex="-1" autocomplete="off"></label></p>' if endpoint else "")
    opts = "".join('<option>%s</option>' % c for c in CARGO_OPTIONS)
    phone_box = ""
    if CONFIG["phone"]:
        phone_box = '<p class="copyable"><a href="tel:%s">%s</a></p>' % (CONFIG["phone"].replace(" ", ""), CONFIG["phone"])
    wa_box = ('<p>%s</p>' % wa_button("btn--wa", "Message us on WhatsApp", "quote-wa")) if CONFIG["whatsapp"] else ""
    offices = "".join('<address><b>%s</b>%s</address>' % (o["region"], "".join("<span>%s</span>" % l for l in o["lines"])) for o in OFFICES)
    body = page_head("Get a free quote",
                     "Tell us what needs to move. We reply with a detailed, no obligation estimate within one business day.",
                     "Contact us", [(None, "Get a quote")], photo="night") + """
<section class="section section--dust">
  <div class="wrap quote-layout">
    <div class="consign">
      <div class="consign__top"><span>Consignment enquiry</span><span>Reply within one business day</span></div>
      <form id="quote-form" name="quote" method="POST" %(netlify)snovalidate data-email="%(email)s" data-endpoint="%(endpoint)s">
        %(hidden)s
        <fieldset>
          <legend><span>01</span>Route</legend>
          <div class="fields fields--2">
            <div class="field"><label for="origin">Collection point</label><input id="origin" name="origin" required data-label="the collection point" placeholder="e.g. Kitwe, Zambia" autocomplete="off"></div>
            <div class="field"><label for="destination">Destination</label><input id="destination" name="destination" required data-label="the destination" placeholder="e.g. Lubumbashi, DRC" autocomplete="off"></div>
          </div>
          <div class="field"><label for="date">Collection date <span class="opt">(optional)</span></label><input id="date" name="date" type="date"></div>
        </fieldset>
        <fieldset>
          <legend><span>02</span>Cargo</legend>
          <div class="fields fields--2">
            <div class="field"><label for="cargo">Cargo type</label><select id="cargo" name="cargo" required data-label="Cargo type"><option value="">Select cargo type</option>%(opts)s</select></div>
            <div class="field"><label for="weight">Approximate weight in tonnes <span class="opt">(optional)</span></label><input id="weight" name="weight" type="number" min="0" step="0.1" inputmode="decimal" placeholder="e.g. 32"></div>
          </div>
          <div class="field"><span style="font-size:.9rem;font-weight:600" id="load-label">Load type</span>
            <div class="choice" role="radiogroup" aria-labelledby="load-label">
              <label><input type="radio" name="load" value="Full load" id="load-full"><span>Full load (FTL)</span></label>
              <label><input type="radio" name="load" value="Part load" id="load-part"><span>Part load (LTL)</span></label>
              <label><input type="radio" name="load" value="Not sure" id="load-unsure" checked><span>Not sure</span></label>
            </div></div>
          <div class="field"><span style="font-size:.9rem;font-weight:600" id="haz-label">Hazardous cargo</span>
            <div class="choice" role="radiogroup" aria-labelledby="haz-label">
              <label><input type="radio" name="hazardous" value="No" id="haz-no" checked><span>No</span></label>
              <label><input type="radio" name="hazardous" value="Yes" id="haz-yes"><span>Yes</span></label>
            </div></div>
          <div class="field"><label for="notes">Anything else we should know <span class="opt">(optional)</span></label>
            <textarea id="notes" name="notes" placeholder="Dimensions, number of loads, UN number and class for hazardous cargo, temperature range, site access"></textarea></div>
        </fieldset>
        <fieldset>
          <legend><span>03</span>Your details</legend>
          <div class="fields fields--2">
            <div class="field"><label for="name">Full name</label><input id="name" name="name" required data-label="Your name" autocomplete="name"></div>
            <div class="field"><label for="company">Company <span class="opt">(optional)</span></label><input id="company" name="company" autocomplete="organization"></div>
            <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required data-label="Your email" autocomplete="email"></div>
            <div class="field"><label for="phone">Phone or WhatsApp <span class="opt">(optional)</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="Include the country code"></div>
          </div>
        </fieldset>
        <div class="form-foot">
          <p>We use these details only to reply to your request. Read our <a href="%(privacy)s">privacy policy</a>.</p>
          <button class="btn btn--primary" type="submit" data-cta="quote-submit">Send quote request %(arrow)s</button>
        </div>
      </form>
      <div class="result" id="quote-result" hidden tabindex="-1">
        <div data-sent hidden class="stack"><p class="eyebrow">Received</p><h2>Thank you. Your request is with our team.</h2>
          <p class="muted">We will reply with a detailed quote within one business day.</p></div>
        <div data-unsent class="stack"><p class="eyebrow">One more step</p><h2>Send your request to our team</h2>
          <p class="muted">Your request is ready below. Open it in your email app, or copy it and send it to <b>%(email)s</b>.</p></div>
        <pre id="quote-summary"></pre>
        <div class="btn-row">
          <a class="btn btn--primary" id="quote-mail" href="mailto:%(email)s">Open in email %(arrow)s</a>
          <button class="btn btn--ghost" type="button" data-copy="" data-copy-target="quote-summary">Copy request</button>
          <button class="btn btn--ghost" type="button" id="quote-again">Edit request</button>
        </div>
      </div>
    </div>
    <aside class="aside" aria-label="Contact details">
      <div class="box"><h3>Quote requests</h3><p class="copyable"><a href="mailto:%(email)s">%(email)s</a><button class="copy-btn" type="button" data-copy="%(email)s">Copy</button></p>%(phone)s%(wa)s</div>
      <div class="box"><h3>What happens next</h3><ol class="ticks" style="list-style:none">
        <li>We check the route, the cargo and the timing.</li>
        <li>We choose the right truck and confirm availability.</li>
        <li>We send a detailed quote within one business day.</li></ol></div>
      <div class="box"><h3>Offices</h3><div style="display:grid;gap:1rem">%(offices)s</div></div>
    </aside>
  </div>
</section>""" % {"email": CONFIG["quote_email"], "endpoint": endpoint, "netlify": netlify, "hidden": hidden, "opts": opts, "privacy": url("privacy"), "arrow": ARROW,
                  "phone": phone_box, "wa": wa_box, "offices": offices}
    return document("quote", "Get a Freight Quote | Patriot Africa",
                    "Request a road freight quote for Zambia, the DRC and Southern Africa. Send your route, cargo and dates and get a detailed quote within one business day.",
                    body, ld=[breadcrumb_ld([("quote", "Get a quote")])], og_image="night")

# ---------------------------------------------------------------- legal
def privacy():
    body = page_head("Privacy policy", "How Patriot Africa collects and uses personal data on this website.", "Legal", [(None, "Privacy policy")]) + """
<section class="section"><div class="wrap"><div class="prose">
<p>This privacy policy explains how Patriot Africa and its affiliated entities ("we", "us", "our") collect and use personal data on our website and on any mobile application that displays this policy. We care about the privacy of your personal information and we are committed to protecting it. This policy explains how we collect, use, disclose and safeguard your information when you visit https://patriotafrica.com. Please read it carefully. If you do not agree with this policy, please do not use the site.</p>
<h2>1. What information do we collect?</h2>
<p>We collect personal information that you give us voluntarily, such as:</p>
<ul><li>Name</li><li>Company name</li><li>Email address</li><li>Phone number</li><li>Details of the cargo and route in a quote request</li></ul>
<p>We collect this information when you fill out a form on the website or contact us directly.</p>
<h2>2. How do we use your information?</h2>
<p>We use the personal information you give us to communicate with you about the logistics services you ask about. This includes replying to your enquiry, discussing your cargo transport needs and preparing quotes. We may also tell you about updates, offers or changes to our services that may be relevant to your business.</p>
<p>We process your personal data on the following lawful grounds:</p>
<ul><li>Consent. When you send a quote request, you consent to us processing your data to reply to it and to provide the services you ask for.</li>
<li>Performance of a contract. If you engage our services, we need to process your personal data to perform that contract.</li></ul>
<p>Where applicable, we comply with the UK GDPR and other data protection laws when we process your information.</p>
<h2>3. How long do we keep your information?</h2>
<p>We keep your personal information for as long as we need it for the purposes in this policy, including providing our services and meeting legal obligations. The period depends on the nature of the information, legal requirements and our business needs. When we no longer need your information, we delete or anonymise it securely. If you want us to delete your information sooner, contact us and we will handle your request in line with applicable law.</p>
<h2>4. What are your privacy rights?</h2>
<p>You have the right to access, update or delete the personal information we hold about you. You can ask us to restrict or stop processing your data, or object to how we use it. If you consented to marketing messages, you can withdraw that consent at any time. You can also ask for a copy of your personal data or ask us to transfer it to another provider. To use any of these rights, contact us with the details below. We will respond in line with applicable data protection law.</p>
<h2>5. How do we keep your information safe?</h2>
<p>We use appropriate technical and organisational measures to protect your personal information from unauthorised access, loss, misuse or alteration. These include secure servers, encryption and access controls. No method of transmission or storage is completely secure, so we cannot guarantee absolute protection, but we review and improve our security practices continuously.</p>
<h2>6. International data transfers</h2>
<p>We may transfer your personal data to, and process it in, countries outside your country of residence. When we do, we put appropriate safeguards in place to protect it, in line with applicable data protection law.</p>
<h2>7. Cookies</h2>
<p>This website does not use advertising cookies. If we add analytics, we will update this policy and ask for your consent where the law requires it.</p>
<h2>Contact us</h2>
<p>If you have questions about this policy or how we handle your personal data, or if you want to use your rights under data protection law, contact us:</p>
<ul><li>Email: <a href="mailto:%s">%s</a></li><li>Post: 85 Great Portland Street, First Floor, London W1W 7LT, United Kingdom</li></ul>
</div></div></section>""" % (CONFIG["email"], CONFIG["email"])
    return document("privacy", "Privacy Policy | Patriot Africa", "How Patriot Africa collects, uses and protects personal data submitted through this website.",
                    body, ld=[breadcrumb_ld([("privacy", "Privacy policy")])])

def terms():
    body = page_head("Terms and conditions", "The terms that govern your use of this website. Last updated 1 September 2024.", "Legal", [(None, "Terms and conditions")]) + """
<section class="section"><div class="wrap"><div class="prose">
<p>These terms and conditions ("Terms") govern your use of the website at https://patriotafrica.com ("Site") and the services provided by Patriot Africa ("we", "us", "our"). By using the Site, you agree to these Terms. If you do not agree, please do not use the Site.</p>
<h2>1. Acceptance of terms</h2>
<p>By using this Site, you confirm that you are at least 18 years old or that you use the Site under the supervision of a parent or guardian.</p>
<h2>2. Services offered</h2>
<p>The Site gives information about the logistics and cargo transport services of Patriot Africa. These include transport within Zambia and to the Democratic Republic of the Congo, the Republic of the Congo, Namibia, South Africa, Tanzania, Malawi, Angola and Zimbabwe.</p>
<h2>3. Changes to terms</h2>
<p>We may change these Terms at any time. Changes take effect when we post them on the Site. If you continue to use the Site after a change, you accept the new Terms.</p>
<h2>4. Use of the site</h2>
<p>You agree to use the Site lawfully and in a way that does not infringe the rights of others or restrict anyone else's use of the Site. You agree not to use the Site to:</p>
<ul><li>Send any material that is unlawful, harmful, threatening, abusive, harassing, defamatory, vulgar, obscene or otherwise objectionable.</li>
<li>Impersonate any person or entity, or misrepresent your connection with any person or entity.</li></ul>
<h2>5. Intellectual property</h2>
<p>All content on this Site, including text, graphics, logos and software, belongs to Patriot Africa or its licensors and is protected by copyright, trademark and other intellectual property laws. You may not reproduce, distribute or create derivative works from any content without our written consent.</p>
<h2>6. Third party links</h2>
<p>The Site may contain links to third party websites. We do not control and are not responsible for their content, privacy policies or practices, or for any loss caused by your use of them.</p>
<h2>7. Limitation of liability</h2>
<p>To the fullest extent the law allows, Patriot Africa is not liable for any direct, indirect, incidental, special, consequential or punitive damages, including loss of profits, data or other intangible losses, that result from:</p>
<ul><li>Your access to, use of, or inability to access or use the Site.</li><li>Any conduct or content of any third party on the Site.</li><li>Unauthorised access to, use of or alteration of your transmissions or content.</li></ul>
<h2>8. Indemnification</h2>
<p>You agree to indemnify and hold harmless Patriot Africa and its affiliates, licensors and service providers from any claims, liabilities, damages, losses, costs and expenses, including reasonable legal fees, that arise from your use of the Site, your breach of these Terms or your violation of the rights of another party.</p>
<h2>9. Governing law</h2>
<p>The laws of Zambia govern these Terms, without regard to conflict of law principles. You agree to the exclusive jurisdiction of the courts of Zambia for any dispute.</p>
<h2>Contact us</h2>
<ul><li>Email: <a href="mailto:%s">%s</a></li><li>Post: 85 Great Portland Street, First Floor, London W1W 7LT, United Kingdom</li></ul>
</div></div></section>""" % (CONFIG["email"], CONFIG["email"])
    return document("terms", "Terms and Conditions | Patriot Africa", "The terms and conditions that govern use of the Patriot Africa website.",
                    body, ld=[breadcrumb_ld([("terms", "Terms and conditions")])])

def notfound():
    body = page_head("This page is off the route", "The page you asked for does not exist or has moved.", "Error 404", [(None, "Page not found")],
                     extra='<div class="btn-row"><a class="btn btn--primary" href="%s">Go to the home page</a><a class="btn btn--light" href="%s">Get a quote</a></div>' % (url("home"), url("quote")))
    return document("404", "Page Not Found | Patriot Africa", "The page you asked for does not exist or has moved.", body, noindex=True)

def render(page):
    return {"home": home, "services": services, "fleet": fleet, "coverage": coverage, "lobito": lobito, "industries": industries,
            "about": about, "quote": quote, "privacy": privacy, "terms": terms, "404": notfound}[page]()
