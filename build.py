#!/usr/bin/env python3
"""Brownlee Sand & Gravel - static site generator.

  1. Unzip brownlee-website-photos.zip so the photos sit in  photos/
     (hero.jpg = home banner, logo.jpg = logo; other names are used on service/town pages).
  2. python3 build.py
  3. Upload everything inside  dist/  to your host.

Needs Python 3.9+ and Pillow:  pip install pillow
"""
import csv, html, json, shutil, sys
from pathlib import Path
from datetime import date

# ---------------- CONFIG ----------------
SITE_URL = "https://www.brownleesandandgravel.ca"   # <- change to the real domain
BUSINESS = "Brownlee Sand & Gravel"
OWNER = "Matt Brownlee"
PHONE_DISPLAY = "(705) 622-3373"
PHONE_TEL = "+17056223373"
EMAIL = "brownleesandandgravel@outlook.com"
STREET, CITY, REGION, POSTAL, COUNTRY = "35 Pinetree Road", "Kirkland Lake", "ON", "P2N 3M6", "CA"
FACEBOOK = "https://www.facebook.com/61585175754713"
HOURS = "Call or text to book. Evenings and weekends by arrangement."
FORM_ACTION = "mailto:" + EMAIL      # replace with a Formspree / Netlify Forms URL for direct sending
GA_ID = ""                           # optional Google Analytics ID, e.g. G-XXXXXXX
GSC_TOKEN = ""                       # optional Google Search Console verification token
SEASONAL = "Fall booking: sand &amp; salt shed filling and driveway gravel"   # seasonal message in the top bar
REVIEWS = []                         # add real ones only: [("Customer name, Town", "What they said")]
# ----------------------------------------

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
PHOTOS = ROOT / "photos"
TODAY = date.today().isoformat()
BID = SITE_URL + "/#business"

def esc(s): return html.escape(s, quote=True)

# Default alt text for the photo set pulled from the Facebook page (captions.csv overrides).
ALT = {
 "hero": "Matt Brownlee running the stone slinger on a foundation job: two loads of gravel spread in about 35-40 minutes",
 "logo": "Brownlee Sand & Gravel Slinger Services logo",
 "slinging-topsoil-yard": "Stone slinger throwing topsoil across a residential yard",
 "slinging-lawn": "Topsoil arcing from the slinger conveyor onto an open field",
 "gravel-beside-house": "A quick Saturday morning gravel sling into the narrow space beside a house",
 "crushed-stone": "Stone slung over a drainage mat",
 "driveway-gravel": "Brownlee stone slinger truck ready for the next job",
 "excavation-aggregate": "Slinger placing aggregate along an excavation",
 "gravel-near-home": "Slinger placing material from the roadside",
 "house-job": "Slinger truck backfilling a building foundation",
 "large-site-sling": "Slinger throwing gravel across a large work site",
 "loader-filling-truck": "Loader filling the slinger truck with gravel",
 "slinger-truck-job": "Brownlee stone slinger truck on a gravel lot",
 "tight-spot-gravel": "Operator slinging gravel along a residential street",
 "topsoil-bed": "Freshly placed topsoil bed beside a tree line",
 "topsoil-load": "Topsoil delivered in a pile, ready to spread",
 "trench-drainage-stone": "Stone slung into a trench for drainage",
 "waterfront-placement": "Slinger placing material at a waterfront property",
 "winter-truck": "The Brownlee slinger truck in winter, the week before Matt picked it up",
 "beach-sand-slinging": "Beach sand slung onto a waterfront for a cottage owner",
}

# ---------- content ----------
TOWNS = {
 "kirkland-lake": dict(name="Kirkland Lake", photo="house-job", near="Swastika, Chaput Hughes and Kenogami", lead="Home base. Matt is based on Pinetree Road, so Kirkland Lake jobs get the fastest quotes and the shortest drive.",
    uses=["Driveway and laneway gravel", "Foundation and basement backfill", "Septic bed and drainage stone", "Topsoil and sand for lawns and gardens"]),
 "temiskaming-shores": dict(name="Temiskaming Shores", photo="waterfront-placement", near="New Liskeard, Haileybury and Dymond", lead="Regular runs to New Liskeard, Haileybury and Dymond for homeowners, cottages, farms and contractors.",
    uses=["Farm lane and yard gravel", "Building pads and shop floors", "Waterfront and cottage material", "Topsoil for lawn repair and new beds"]),
 "timmins": dict(name="Timmins", photo="large-site-sling", near="South Porcupine, Schumacher and Porcupine", lead="Slinger service for Timmins job sites where a dump truck can't spread the load where it's needed.",
    uses=["Driveway and parking area stone", "Backfill around foundations and footings", "Crushed stone for drainage and weeping tile", "Sand for bedding and fill"]),
 "larder-lake": dict(name="Larder Lake", photo="tight-spot-gravel", near="Virginiatown, Kearns and the Highway 66 corridor", lead="Bulk gravel, sand and topsoil placed at Larder Lake homes, camps and lots, including spots with tight access.",
    uses=["Camp road and parking gravel", "Septic and drainage stone", "Topsoil for new lawns", "Sand fill and bedding"]),
 "matheson": dict(name="Matheson", photo="excavation-aggregate", near="Black River-Matheson, Ramore and Holtyre", lead="Gravel and topsoil placement for farms, lanes and building sites around Matheson.",
    uses=["Farm laneway and yard gravel", "Shop and barn pads", "Culvert and drainage stone", "Topsoil and fill"]),
 "cobalt": dict(name="Cobalt", photo="gravel-beside-house", near="Coleman, Latchford and Silver Centre", lead="Precise stone and sand placement for Cobalt properties, including sloped and hard-to-reach lots.",
    uses=["Hillside and sloped-lot gravel", "Foundation backfill", "Patio and walkway base stone", "Topsoil for landscaping"]),
}

SERVICES = {
 "stone-slinger": dict(name="Stone Slinger Service", short="Stone slinger placement", photo="slinging-topsoil-yard", head="slinger-truck-job",
   blurb="A conveyor truck that places gravel, sand, topsoil and stone up to 100 ft away, exactly where you need it.",
   h1="Stone slinger service in Kirkland Lake and Northern Ontario",
   desc="Stone slinger truck placing gravel, sand, topsoil and stone up to 100 ft away in Kirkland Lake, Timmins and Temiskaming Shores. Most jobs done in about an hour.",
   body=["Most people have never seen a stone slinger. Think of it as a giant conveyor belt mounted on a truck. The operator aims it with a remote, so gravel, sand, topsoil or stone lands behind the house, over a fence, into a garage build or down a long laneway, up to 100 ft from the truck.",
         "A load of topsoil, gravel or crusher fines can take hours or days to move by hand. With the slinger, most jobs are done in about an hour. On one foundation job, two loads of gravel were spread in about 35-40 minutes.",
         "Pricing is different from a dump truck. A dump truck drops material in one spot and leaves, so you still pay for labour, equipment and time to move it. The slinger places it where it belongs the first time."],
   points=["Places material up to 100 ft away", "Most jobs done in about an hour", "Tight spots, slopes, over fences", "Truck stays on the road or driveway"]),
 "gravel-driveways": dict(name="Gravel & Driveways", short="Gravel and driveways", photo="gravel-beside-house",
   blurb="Fresh driveway gravel, crushed stone and crusher fines, delivered and placed with less raking and spreading.",
   h1="Driveway gravel and crushed stone in Kirkland Lake and area",
   desc="Driveway gravel, crushed limestone and crusher fines delivered and slung into place in Kirkland Lake, Timmins and Temiskaming Shores. Less raking.",
   body=["Your driveway doesn't always need to be rebuilt. Sometimes it just needs a fresh layer of gravel. We deliver and place fresh gravel right where you need it, so there's far less raking and spreading.",
         "We supply gravel, crushed limestone and crusher fines for driveways, laneways, parking areas, walkways and patio bases. Use the gravel calculator for a quick estimate, then call or text for a quote."],
   points=["Driveway and laneway refresh", "Crushed limestone and crusher fines", "Parking areas and walkways", "Patio and paver base"]),
 "topsoil-sand-mulch": dict(name="Topsoil, Sand & Mulch", short="Topsoil, sand and mulch", photo="topsoil-bed",
   blurb="Topsoil for lawns and gardens, screened sand and mulch, in a pile or spread out. Your choice.",
   h1="Topsoil, sand and mulch delivery and spreading",
   desc="Topsoil, screened sand and mulch delivered in a pile or slung and spread where you want it in Kirkland Lake, Temiskaming Shores, Timmins and area.",
   body=["Material in a pile or spread out, your choice. Need a load delivered? We can place it in a pile. Need it installed? We can sling and spread it exactly where you want it.",
         "Topsoil season starts as soon as the ground dries up in spring, and the schedule fills fast. Book early for lawn repair, new gardens and yard fixes. Screened sand, mulch and wood shavings are available too."],
   points=["Topsoil for lawns and gardens", "Screened sand", "Mulch and wood shavings", "Pile drop or spread in place"]),
 "foundation-backfill": dict(name="Foundations & Garage Pads", short="Foundations and garage pads", photo="house-job",
   blurb="Foundation gravel, backfill, garage pads and house raising, placed fast without tearing up the yard.",
   h1="Foundation gravel, backfill and garage pads",
   desc="Foundation gravel, backfill, garage pads and house raising material placed by stone slinger in Kirkland Lake, Timmins and Northern Ontario.",
   body=["Building a house or garage, or raising a house? Don't spend hours moving gravel by hand. The slinger places material exactly where you need it, fast and clean.",
         "We can sling material right into a garage build or over a foundation wall, and backfill foundations without driving a loader across your yard."],
   points=["Foundation gravel", "Garage and shop pads", "House raising", "Backfill without yard damage"]),
 "drainage-stone": dict(name="Drainage Stone", short="Drainage and weeping tile stone", photo="trench-drainage-stone",
   blurb="Clear stone placed around foundations, over weeping tile, along trenches and into hard-to-reach spots.",
   h1="Drainage stone for weeping tile and French drains",
   desc="Drainage stone placed over weeping tile, around foundations and in French drain trenches by stone slinger in Kirkland Lake and Northern Ontario.",
   body=["Installing weeping tile, French drains or drainage stone? Don't fight with wheelbarrows and skid steers. Let the slinger do the work.",
         "We place drainage stone right where you need it: around foundations, over weeping tile, along trenches and into hard-to-reach areas."],
   points=["Weeping tile stone", "French drains", "Around foundations", "Long and narrow trenches"]),
 "beach-sand-waterfront": dict(name="Beach Sand & Waterfront", short="Beach sand and cottages", photo="waterfront-placement",
   blurb="Beach sand restoration for cottages and camps, and material slung right onto a barge for water-access lots.",
   h1="Beach sand restoration and waterfront material",
   desc="Beach sand delivery and slinging for waterfront properties, cottages and camps, plus barge loading for water-access cottages in Northern Ontario.",
   body=["Did winter ice and run-off wash your beach away? We deliver and sling clean beach sand for waterfront properties, cottages and camps.",
         "Water-access cottage? If the only way in is by boat and you have a barge bringing in material, no problem. We can sling aggregate or soil right onto the barge."],
   points=["Clean beach sand", "Cottages and camps", "Barge loading for water-access lots", "Placement from shore"]),
 "sand-salt-shed-filling": dict(name="Sand & Salt Shed Filling", short="Sand and salt shed filling", photo="large-site-sling",
   blurb="Sand, salt and gravel placed deep into storage sheds for contractors, municipalities and snow removal companies.",
   h1="Sand and salt shed filling for contractors and municipalities",
   desc="Stone slinger sand and salt shed filling for contractors, municipalities, property managers and snow removal companies in Northern Ontario.",
   body=["Don't wait until the first storm to find out your salt shed needs filling. The slinger places sand, salt, gravel and other materials right where you need them, so shed filling is faster and easier.",
         "We work with contractors, municipalities, property managers and snow removal companies. Book in the fall before the rush."],
   points=["Sand and salt sheds", "Contractors and municipalities", "Property managers", "Snow removal companies"]),
 "bulk-delivery-half-loads": dict(name="Delivery & Half Loads", short="Bulk delivery and half loads", photo="topsoil-load",
   blurb="Don't need a full load? Half loads of topsoil, gravel, sand and crusher fines, supplied and delivered.",
   h1="Bulk delivery and half loads in Northern Ontario",
   desc="Bulk and half-load delivery of topsoil, gravel, sand and crusher fines to Kirkland Lake, Temiskaming Shores, Timmins, Larder Lake, Matheson and Cobalt.",
   body=["One call, one truck, one stop shop. We supply the material, deliver it and place it.",
         "Don't need a full load? We book half loads of topsoil, gravel, sand and crusher fines, so you get the material you need without paying for a full truckload. Even better, we can sling it right where you want it."],
   points=["Half loads available", "Topsoil, gravel, sand, crusher fines", "Supplied, delivered and placed", "Six towns and surrounding areas"]),
}

FAQS = [
 ("What is a stone slinger?", "Think of it as a giant conveyor belt mounted on a truck. It places gravel, sand, topsoil and stone up to 100 feet away with precision, instead of dumping it in one pile."),
 ("How long does a job take?", "Most jobs are done in about an hour. On one foundation job, two loads of gravel were spread in about 35-40 minutes."),
 ("Do you sell half loads?", "Yes. We book half loads of topsoil, gravel, sand and crusher fines, so you don't pay for a full truckload you don't need."),
 ("Why does a slinger cost more than a dump truck?", "A dump truck drops material in one spot and leaves. You still pay for labour, equipment and time to move it. The slinger places it where it belongs, so the total job usually costs less."),
 ("What materials do you supply?", "Topsoil, gravel, crushed limestone, crusher fines, screened sand, beach sand, mulch and wood shavings. Call or text to check what's in stock."),
 ("Can you load a barge for a water-access cottage?", "Yes. If your only way in is by boat, we can sling aggregate or soil right onto the barge."),
 ("Do you fill sand and salt sheds?", "Yes. We fill sand and salt sheds for contractors, municipalities, property managers and snow removal companies."),
 ("Which areas do you serve?", "Kirkland Lake, Temiskaming Shores, Timmins, Larder Lake, Matheson, Cobalt and surrounding Northern Ontario."),
 ("How do I get a quote?", "Call or text (705) 622-3373, message us on Facebook, or send the form with your town, the material and the size of the job. Quotes are free."),
 ("Will the truck damage my lawn?", "No. The truck stays on the road or driveway and the conveyor reaches out, so there are no tire ruts across your yard."),
]

NAV = [("/services/", "Services"), ("/service-areas/", "Areas"), ("/gallery/", "Our Work"), ("/gravel-calculator/", "Calculator"), ("/faq/", "FAQ"), ("/contact/", "Contact")]

# ---------- photos ----------
PH = {}          # stem -> picture data
LOGO = None

def process_photos():
    global LOGO
    if not PHOTOS.exists(): return
    try:
        from PIL import Image, ImageOps
    except ImportError:
        sys.exit("Install Pillow first:  pip install pillow")
    caps = {}
    cf = PHOTOS / "captions.csv"
    if cf.exists():
        with cf.open(newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                if len(row) >= 2 and row[1].strip(): caps[Path(row[0].strip()).stem] = row[1].strip()
    img_dir = DIST / "images"; img_dir.mkdir(parents=True, exist_ok=True)
    (DIST / "assets").mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in PHOTOS.rglob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
    for p in files:
        stem = p.stem.lower().replace(" ", "-")
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        if stem == "logo":
            for s in (96, 192, 512):
                im.resize((s, round(im.height * s / im.width)), Image.LANCZOS).save(DIST / "assets" / f"logo-{s}.png", "PNG", optimize=True)
            LOGO = True
            continue
        widths = [w for w in (480, 800, 1200, 1800) if w <= im.width] or [im.width]
        for w in widths:
            r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            r.save(img_dir / f"{stem}-{w}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
            r.save(img_dir / f"{stem}-{w}.webp", "WEBP", quality=80, method=6)
            r.save(img_dir / f"{stem}-{w}.avif", "AVIF", quality=55)
        big = widths[-1]
        PH[stem] = dict(stem=stem, widths=widths, w=big, h=round(im.height * big / im.width),
                        alt=caps.get(stem, ALT.get(stem, "Brownlee Sand & Gravel stone slinger job in Northern Ontario")))
        if stem == "hero":
            ImageOps.fit(im, (1200, 630), Image.LANCZOS).save(DIST / "assets" / "og.jpg", "JPEG", quality=85, optimize=True)

def pic(stem, sizes="(min-width:900px) 33vw, 100vw", eager=False, cls=""):
    ph = PH.get(stem)
    if not ph: return ""
    def ss(ext): return ", ".join(f"/images/{ph['stem']}-{w}.{ext} {w}w" for w in ph["widths"])
    mid = ph["widths"][min(1, len(ph["widths"]) - 1)]
    load = 'decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}"><source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img{c} src="/images/{ph["stem"]}-{mid}.jpg" srcset="{ss("jpg")}" sizes="{sizes}" width="{ph["w"]}" height="{ph["h"]}" alt="{esc(ph["alt"])}" {load}></picture>')

def gallery_stems():
    order = ["hero", "slinging-topsoil-yard", "large-site-sling", "gravel-beside-house", "tight-spot-gravel", "waterfront-placement",
             "slinging-lawn", "beach-sand-slinging", "house-job", "topsoil-bed", "excavation-aggregate", "trench-drainage-stone", "gravel-near-home", "loader-filling-truck", "crushed-stone", "topsoil-load", "slinger-truck-job", "driveway-gravel", "winter-truck"]
    rest = sorted(s for s in PH if s not in order)
    return [s for s in order if s in PH] + rest

def make_og_card():
    p = DIST / "assets" / "og.jpg"
    if p.exists(): return
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    im = Image.new("RGB", (1200, 630), (1, 29, 63)); d = ImageDraw.Draw(im)
    d.rectangle([0, 600, 1200, 630], fill=(253, 198, 0))
    def font(sz):
        for f in ("DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"):
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
        return ImageFont.load_default()
    d.text((80, 140), "BROWNLEE", font=font(120), fill=(255, 255, 255))
    d.text((80, 275), "SAND & GRAVEL", font=font(72), fill=(253, 198, 0))
    d.text((80, 400), "Stone slinger service  |  Kirkland Lake, ON", font=font(40), fill=(220, 228, 234))
    d.text((80, 480), PHONE_DISPLAY, font=font(56), fill=(255, 255, 255))
    (DIST / "assets").mkdir(parents=True, exist_ok=True)
    im.save(p, "JPEG", quality=88)

# ---------- schema ----------
def j(d): return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"

def business_schema():
    return {"@context": "https://schema.org", "@type": ["LocalBusiness", "HomeAndConstructionBusiness"], "@id": BID,
        "name": BUSINESS, "url": SITE_URL + "/", "telephone": PHONE_TEL, "email": EMAIL,
        "image": SITE_URL + "/assets/og.jpg", "logo": SITE_URL + ("/assets/logo-512.png" if LOGO else "/assets/favicon.svg"), "priceRange": "$$",
        "description": "Stone slinger service: gravel, sand, topsoil, drainage stone, beach sand and mulch supplied, delivered and placed up to 100 ft away in Kirkland Lake, Temiskaming Shores, Timmins and Northern Ontario.",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY, "addressRegion": REGION, "postalCode": POSTAL, "addressCountry": COUNTRY},
        "areaServed": [{"@type": "City", "name": t["name"]} for t in TOWNS.values()],
        "sameAs": [FACEBOOK], "founder": {"@type": "Person", "name": OWNER},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "description": s["blurb"]}} for s in SERVICES.values()]}}

def crumbs_schema(crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + p} for i, (p, n) in enumerate(crumbs)]}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

# ---------- shared pieces ----------
TRUCK = """<svg class="truck" viewBox="0 0 640 360" role="img" aria-label="Illustration of a stone slinger truck throwing gravel">
<rect width="640" height="360" fill="#0f2a4a"/><path d="M0 270 L130 236 L250 262 L380 222 L520 258 L640 230 V360 H0Z" fill="#0b2038"/><rect y="292" width="640" height="68" fill="#081726"/>
<g fill="#f5b800"><circle cx="470" cy="112" r="6"/><circle cx="494" cy="128" r="5"/><circle cx="516" cy="154" r="6"/><circle cx="534" cy="184" r="5"/><circle cx="550" cy="222" r="6"/><circle cx="560" cy="258" r="5"/><circle cx="505" cy="140" r="3"/><circle cx="527" cy="170" r="3"/></g>
<g transform="translate(40 150)"><rect x="0" y="96" width="330" height="30" rx="4" fill="#c9d1d6"/><path d="M18 40 H210 L240 96 H18Z" fill="#e6ebee"/><path d="M40 20 H190 L205 40 H40Z" fill="#aab4bb"/>
<rect x="238" y="48" width="86" height="64" rx="8" fill="#f5b800"/><rect x="258" y="58" width="52" height="28" rx="4" fill="#cfe6f2"/>
<path d="M150 30 L400 -36" stroke="#081726" stroke-width="16" stroke-linecap="round"/><path d="M150 30 L400 -36" stroke="#8b98a2" stroke-width="8" stroke-linecap="round"/>
<g fill="#081726"><circle cx="60" cy="128" r="22"/><circle cx="118" cy="128" r="22"/><circle cx="272" cy="128" r="22"/></g><g fill="#8b98a2"><circle cx="60" cy="128" r="9"/><circle cx="118" cy="128" r="9"/><circle cx="272" cy="128" r="9"/></g></g></svg>"""

SVC_DESC = {
 "stone-slinger": "Placed up to 100 ft away",
 "gravel-driveways": "Driveway refresh, crusher fines",
 "topsoil-sand-mulch": "Pile drop or spread in place",
 "foundation-backfill": "Backfill, pads, house raising",
 "drainage-stone": "Weeping tile, French drains",
 "beach-sand-waterfront": "Beach sand, barge loading",
 "sand-salt-shed-filling": "Contractors and municipalities",
 "bulk-delivery-half-loads": "Half loads available",
}

ICON = {
 "phone": '<svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>',
 "chev": '<svg viewBox="0 0 24 24" aria-hidden="true" class="chev"><path fill="none" stroke="currentColor" stroke-width="2.5" d="M6 9l6 6 6-6"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><path fill="currentColor" d="M14 8h3V4h-3c-2.8 0-4 1.7-4 4.3V10H7v4h3v8h4v-8h3l1-4h-4V8.6c0-.4.2-.6.6-.6z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><path fill="currentColor" d="M4 4h16a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H8l-4 4V5a1 1 0 0 1 1-1z"/></svg>',
 "quote": '<svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><path fill="currentColor" d="M6 2h9l5 5v14a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1zm8 1.5V8h4.5zM8 12h8v2H8zm0 4h8v2H8z"/></svg>',
}
SMS = "sms:" + PHONE_TEL

def brand(size=56):
    mark = (f'<img class="brand-logo" src="/assets/logo-192.png" width="{size}" height="{size}" alt="">' if LOGO
            else '<span class="brand-mark" aria-hidden="true">B</span>')
    return f'<a class="brand" href="/">{mark}<span class="brand-text">Brownlee<small>Sand &amp; Gravel</small></span></a>'

def nav_html(path):
    def cur(h): return ' aria-current="page"' if path == h or (h != "/" and path.startswith(h)) else ""
    svc_items = "".join(f'<li><a href="/services/{s}/"{cur("/services/"+s+"/")}><strong>{v["name"]}</strong><span>{SVC_DESC[s]}</span></a></li>' for s, v in SERVICES.items())
    town_items = "".join(f'<li><a href="/service-areas/{s}/"{cur("/service-areas/"+s+"/")}><strong>{t["name"]}</strong><span>{"Home base" if s=="kirkland-lake" else t["near"].split(",")[0]}</span></a></li>' for s, t in TOWNS.items())
    svc_on = ' data-on' if path.startswith("/services/") else ""
    area_on = ' data-on' if path.startswith("/service-areas/") else ""
    about_on = ' data-on' if path in ("/about/", "/faq/", "/contact/") else ""
    return f"""<nav class="nav" id="site-nav" aria-label="Main">
<ul class="nav-list">
<li class="nav-item"><a class="nav-link" href="/services/stone-slinger/"{cur("/services/stone-slinger/")}>Stone Slinger</a></li>
<li class="nav-item has-drop"{svc_on}><button class="nav-link drop-btn" type="button" aria-expanded="false" aria-controls="dd-services">Services{ICON["chev"]}</button>
 <div class="drop mega" id="dd-services"><div class="mega-grid"><ul class="drop-list two">{svc_items}</ul>
 <div class="mega-card"><p class="mc-k">Not sure what you need?</p><p>Text Matt a photo of the job and get a fast answer.</p><a class="btn btn-gold btn-sm" href="{SMS}">Text a photo</a><p class="mc-ph"><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p></div></div>
 <p class="drop-foot"><a href="/services/">View all services</a></p></div></li>
<li class="nav-item has-drop"{area_on}><button class="nav-link drop-btn" type="button" aria-expanded="false" aria-controls="dd-areas">Service Areas{ICON["chev"]}</button>
 <div class="drop" id="dd-areas"><ul class="drop-list">{town_items}</ul><p class="drop-foot">Not listed? We travel. <a href="/service-areas/">All areas</a></p></div></li>
<li class="nav-item"><a class="nav-link" href="/gallery/"{cur("/gallery/")}>Projects</a></li>
<li class="nav-item"><a class="nav-link" href="/gravel-calculator/"{cur("/gravel-calculator/")}>Calculator</a></li>
<li class="nav-item has-drop"{about_on}><button class="nav-link drop-btn" type="button" aria-expanded="false" aria-controls="dd-about">About{ICON["chev"]}</button>
 <div class="drop small" id="dd-about"><ul class="drop-list"><li><a href="/about/"{cur("/about/")}><strong>About Matt</strong><span>Owner-operator</span></a></li><li><a href="/faq/"{cur("/faq/")}><strong>FAQ</strong><span>Reach, timing, pricing</span></a></li><li><a href="/contact/"{cur("/contact/")}><strong>Contact</strong><span>Call, text or email</span></a></li></ul></div></li>
</ul>
<div class="nav-cta"><a class="btn btn-phone" href="tel:{PHONE_TEL}">{ICON["phone"]}<span>{PHONE_DISPLAY}</span></a><a class="btn btn-gold" href="#quote">Get a free quote</a></div>
</nav>"""

def layout(path, title, desc, body, crumbs=None, schemas=None):
    sch = [business_schema()]
    bc = ""
    if crumbs:
        sch.append(crumbs_schema(crumbs))
        home_ico = '<svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><path fill="currentColor" d="M12 3 2 11h3v9h6v-6h2v6h6v-9h3z"/></svg>'
        items = "".join((f'<li><a href="{p}">{home_ico if i == 0 else ""}<span>{n}</span></a></li>' if i < len(crumbs) - 1 else f'<li><span aria-current="page">{n}</span></li>') for i, (p, n) in enumerate(crumbs))
        bc = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{items}</ol></nav>'
        if '<div class="wrap head-inner">' in body:
            body = body.replace('<div class="wrap head-inner">', '<div class="wrap head-inner">' + bc, 1)
            bc = ""
    sch += schemas or []
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>' if GA_ID else "")
    gsc = f'<meta name="google-site-verification" content="{GSC_TOKEN}">' if GSC_TOKEN else ""
    icon = '<link rel="icon" href="/assets/logo-96.png" type="image/png"><link rel="apple-touch-icon" href="/assets/logo-192.png">' if LOGO else '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">'
    towns = "".join(f'<li><a href="/service-areas/{s}/">{t["name"]}</a></li>' for s, t in TOWNS.items())
    svcs = "".join(f'<li><a href="/services/{s}/">{v["name"]}</a></li>' for s, v in SERVICES.items())
    return f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}{path}">
<meta name="theme-color" content="#011D3F">
<meta name="geo.region" content="CA-ON"><meta name="geo.placename" content="{CITY}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BUSINESS}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE_URL}{path}"><meta property="og:image" content="{SITE_URL}/assets/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{BUSINESS} stone slinger truck">
<meta property="og:locale" content="en_CA"><meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{SITE_URL}/assets/og.jpg">
{gsc}{icon}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,600..900&amp;family=Figtree:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/style.css">
{"".join(j(s) for s in sch)}
{ga}
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="utility"><div class="wrap util-row"><p class="u-left">{ICON["pin"]}Owner-operated &middot; Kirkland Lake &amp; area</p><p class="u-mid">{SEASONAL}</p>
<p class="u-right"><a href="{FACEBOOK}" rel="noopener" aria-label="Facebook">{ICON["fb"]}</a><a class="u-call" href="tel:{PHONE_TEL}">{ICON["phone"]}Call or text Matt {PHONE_DISPLAY}</a></p></div></div>
<header class="site-header" id="top-bar">
  <div class="wrap bar">
    {brand()}
    <a class="m-call" href="tel:{PHONE_TEL}" aria-label="Call {PHONE_DISPLAY}">{ICON["phone"]}</a>
    <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="site-nav"><span class="burger" aria-hidden="true"></span><span class="mb-label">Menu</span></button>
    {nav_html(path)}
  </div>
</header>
<main id="main">
{bc}
{body}
{"" if path == "/contact/" else quote_band()}
</main>
<footer class="site-footer">
  <div class="wrap foot">
    <div class="foot-brand">{brand(64)}<p>Stone slinger service: gravel, sand, topsoil and stone supplied, delivered and placed across Northern Ontario. Owner-operated by {OWNER}.</p>
      <p class="foot-call"><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p><p class="foot-sub">Call or text</p></div>
    <div><h2>Services</h2><ul class="plain">{svcs}</ul></div>
    <div><h2>Service areas</h2><ul class="plain">{towns}</ul><h2 class="mt">Tools</h2><ul class="plain"><li><a href="/gravel-calculator/">Gravel calculator</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/gallery/">Projects</a></li></ul></div>
    <div><h2>Contact</h2><address>{BUSINESS}<br>{STREET}<br>{CITY}, {REGION} {POSTAL}<br><a href="mailto:{EMAIL}">{EMAIL}</a></address><p>{HOURS}</p><p><a href="{FACEBOOK}" rel="noopener">Facebook</a> &middot; <a href="/about/">About</a> &middot; <a href="/contact/">Contact</a></p></div>
  </div>
  <p class="copy wrap">&copy; {date.today().year} {BUSINESS}, {CITY}, {REGION}. All rights reserved.</p>
</footer>
<div class="mbar"><a href="tel:{PHONE_TEL}">{ICON["phone"]}Call</a><a href="{SMS}">{ICON["chat"]}Text</a><a href="#quote" class="mbar-q">{ICON["quote"]}Quote</a></div>
<dialog class="lightbox" id="lightbox"><button class="lb-close" type="button" aria-label="Close photo">&times;</button><img id="lb-img" src="data:," alt=""><p id="lb-cap"></p></dialog>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""

def svc_options():
    return "".join(f"<option>{v['name']}</option>" for v in SERVICES.values()) + "<option>Not sure</option>"

def town_options():
    return "".join(f"<option>{t['name']}</option>" for t in TOWNS.values()) + "<option>Other area</option>"

def quote_band():
    bg = pic("large-site-sling", sizes="100vw", cls="cta-bg")
    return f"""<section class="qband" id="quote">{bg}<div class="wrap qband-grid"><div class="qb-copy"><p class="eyebrow">Free quote</p><h2>Tell us about <em>the job.</em></h2>
<p>Matt quotes every job himself and usually replies the same day. Prefer to talk? Call or text <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>, or text a photo of the spot.</p>
<ul class="ticks light"><li>Supplied, delivered and placed</li><li>Half loads available</li><li>No lawn ruts, no wheelbarrows</li></ul></div>
<form class="quote-form" action="{esc(FORM_ACTION)}" method="post" enctype="text/plain">
<div class="fg"><div class="f"><label for="qf-name">Name</label><input id="qf-name" name="name" autocomplete="name" required></div>
<div class="f"><label for="qf-phone">Phone</label><input id="qf-phone" name="phone" type="tel" autocomplete="tel" required></div></div>
<div class="fg"><div class="f"><label for="qf-svc">Service</label><select id="qf-svc" name="service">{svc_options()}</select></div>
<div class="f"><label for="qf-town">Town</label><select id="qf-town" name="town">{town_options()}</select></div></div>
<div class="fg"><div class="f"><label for="qf-qty">Amount (if known)</label><input id="qf-qty" name="amount" placeholder="e.g. half load, 10 tonnes"></div>
<div class="f"><label for="qf-when">When</label><select id="qf-when" name="timing"><option>As soon as possible</option><option>Within 2 weeks</option><option>This month</option><option>Just pricing</option></select></div></div>
<div class="f"><label for="qf-details">Job details (distance from the road, access, anything else)</label><textarea id="qf-details" name="details" rows="3"></textarea></div>
<button class="btn btn-gold btn-block" type="submit">Request my free quote</button>
<p class="fine">Or text a photo to <a href="{SMS}">{PHONE_DISPLAY}</a>.</p></form></div></section>"""

def cta(text="Ready to get your project done?"):
    return ""

def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs) + "</div>"

def quick_form(idp="q"):
    return f"""<form class="quick" action="{esc(FORM_ACTION)}" method="post" enctype="text/plain"><h2>Start a free quote</h2><p class="sub">Matt usually replies the same day.</p>
<div class="f"><label for="{idp}-svc">What do you need?</label><select id="{idp}-svc" name="service">{svc_options()}</select></div>
<div class="f"><label for="{idp}-town">Where is the job?</label><select id="{idp}-town" name="town">{town_options()}</select></div>
<div class="f"><label for="{idp}-name">Name</label><input id="{idp}-name" name="name" autocomplete="name" required></div>
<div class="f"><label for="{idp}-phone">Phone</label><input id="{idp}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<button class="btn btn-gold btn-block" type="submit">Get my quote</button><p class="fine">Or call or text <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p></form>"""

def page_head(title, lead, photo=None, eyebrow=None):
    img = pic(photo, sizes="100vw", eager=True, cls="head-bg") if photo else ""
    cls = "page-head has-photo" if img else "page-head"
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f'<section class="{cls}">{img}<div class="wrap head-inner">{eb}<h1>{title}</h1><p class="lead">{lead}</p></div></section>'

def reviews_html():
    if not REVIEWS: return ""
    cards = "".join(f'<blockquote class="review"><p>{esc(t)}</p><footer>{esc(n)}</footer></blockquote>' for n, t in REVIEWS)
    return f'<section class="sec"><div class="wrap"><h2 class="h-sec">What customers say</h2><div class="cards">{cards}</div></div></section>'

def svc_card(s, v, h="h3"):
    img = pic(v["photo"], sizes="(min-width:900px) 25vw, (min-width:600px) 50vw, 100vw")
    media = f'<div class="card-media">{img}</div>' if img else ""
    return f'<article class="card">{media}<div class="card-body"><{h}><a href="/services/{s}/">{v["name"]}</a></{h}><p>{v["blurb"]}</p><p class="more">Learn more</p></div></article>'

PROJECTS = ["Driveways & laneways", "Foundation backfill", "Septic beds", "French drains & weeping tile", "Pool backfill", "Shop & building pads",
            "Patios & walkways", "Lawns & gardens", "Retaining walls", "Parking areas", "Cottages & waterfront", "Farm yards"]

def projects_html():
    items = "".join(f"<li>{p}</li>" for p in PROJECTS)
    return f'<section class="sec"><div class="wrap"><p class="eyebrow eb-dark">Jobs we handle</p><h2 class="h-sec">Built for the jobs <em>you have</em></h2><ul class="proj">{items}</ul></div></section>'

HERO_ARC = """<svg class="hero-arc" viewBox="0 0 560 420" aria-hidden="true" focusable="false"><path d="M20 380 C 140 40, 380 0, 540 300" fill="none" stroke="#FDC600" stroke-width="5" stroke-linecap="round"/><g fill="#FDC600"><circle cx="540" cy="300" r="7"/><circle cx="520" cy="330" r="5"/><circle cx="552" cy="336" r="4"/></g></svg>"""

def ticker_html():
    items = ["Stone slinger placement", "Gravel & driveways", "Topsoil & sand", "Drainage stone", "Beach sand", "Half loads", "Kirkland Lake", "Temiskaming Shores", "Timmins", "Larder Lake", "Matheson", "Cobalt"]
    row = "".join(f"<span>{i}</span>" for i in items)
    return f'<div class="ticker" aria-hidden="true"><div class="ticker-track">{row}{row}</div></div>'

def versus_html():
    return """<section class="sec vs-sec"><div class="wrap"><p class="eyebrow">The difference</p><h2 class="h-sec">Don't dump it. <em>Sling it.</em></h2>
<div class="vs"><div class="vs-col vs-bad"><p class="vs-k">Dump and spread</p><h3>The old way</h3><ul><li>Drops the whole load in one spot</li><li>You rent a loader or grab a wheelbarrow</li><li>Tire ruts across the lawn</li><li>A weekend of shovelling and raking</li></ul></div>
<div class="vs-mid" aria-hidden="true">VS</div>
<div class="vs-col vs-good"><p class="vs-k">Slung and placed</p><h3>The Brownlee way</h3><ul><li>Places material up to 100 ft away</li><li>Behind the house, over fences, into garages</li><li>Truck stays on the road or driveway</li><li>Most jobs done in about an hour</li></ul></div></div></div></section>"""

def trust_html():
    return """<section class="trust"><div class="wrap"><ul><li>Owner-operated</li><li>Based in Kirkland Lake</li><li>Free quotes</li><li>Residential, farm &amp; commercial</li><li>Call or text anytime</li></ul></div></section>"""

# ---------- pages ----------
def page_home():
    hero_img = pic("hero", sizes="100vw", eager=True, cls="hero-bg")
    hero_cls = "hero has-photo" if hero_img else "hero"
    art = "" if hero_img else f'<div class="hero-art">{TRUCK}</div>'
    hero = f"""<section class="{hero_cls}">{hero_img}<div class="wrap hero-grid"><div class="hero-copy">
<p class="eyebrow load-in">Stone slinger service &middot; Kirkland Lake, ON</p>
<h1 class="load-in d1">The right material. <em>Exactly</em> where you need it.</h1>
<p class="lead load-in d2">One call. One truck. Gravel, sand, topsoil and stone supplied, delivered and slung up to 100 ft, right where you need it. Serving Kirkland Lake, Timmins, Temiskaming Shores and the surrounding area.</p>
<p class="actions load-in d3"><a class="btn btn-gold" href="#quote">Get a free quote</a><a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></p><ul class="chips-hero load-in d4"><li>Owner-operated</li><li>Up to 100 ft reach</li><li>6 towns served</li><li>Half loads</li></ul>{art}</div>
<div class="load-in d5">{quick_form()}</div></div>{HERO_ARC}</section>{ticker_html()}"""
    stats = """<section class="stats"><div class="wrap"><dl>
<div><dt>Slinger reach</dt><dd>Up to 100 ft</dd></div><div><dt>Most jobs done in</dt><dd>About 1 hr</dd></div><div><dt>Half loads</dt><dd>Available</dd></div><div><dt>Owner-operated</dt><dd>Matt Brownlee</dd></div></dl></div></section>"""
    cards = "".join(svc_card(s, v) for s, v in SERVICES.items())
    action_img = pic("large-site-sling", sizes="(min-width:900px) 50vw, 100vw") or pic("slinging-lawn", sizes="(min-width:900px) 50vw, 100vw")
    action_media = f'<div class="split-media">{action_img}</div>' if action_img else f'<div class="split-media">{TRUCK}</div>'
    steps = """<ol class="steps"><li><h3>Call or text</h3><p>Tell Matt your town, the material and the size of the job.</p></li>
<li><h3>Get a clear quote</h3><p>One price for material and placement before anything is booked.</p></li>
<li><h3>Truck arrives</h3><p>The slinger parks on the road or driveway. The conveyor does the reaching.</p></li>
<li><h3>Material placed</h3><p>Stone, sand or topsoil lands where you need it, ready to level.</p></li></ol>"""
    g = gallery_stems()[1:7]
    work = ""
    if g:
        tiles = "".join(f'<figure class="tile">{pic(s, sizes="(min-width:900px) 33vw, 50vw")}</figure>' for s in g)
        work = f'<section class="sec"><div class="wrap"><div class="sec-head"><h2 class="h-sec">Recent <em>jobs</em></h2><a class="link-arrow" href="/gallery/">View all photos</a></div><div class="mosaic">{tiles}</div></div></section>'
    towns = "".join(f'<li><a href="/service-areas/{s}/">{t["name"]}</a></li>' for s, t in TOWNS.items())
    return layout("/", "Stone Slinger Service Kirkland Lake | Brownlee Sand & Gravel",
        "Stone slinger service in Kirkland Lake: gravel, topsoil, sand and stone supplied and placed up to 100 ft away. Half loads available. Call (705) 622-3373.",
        f"""{hero}{stats}{versus_html()}
<section class="sec"><div class="wrap"><div class="sec-head"><h2 class="h-sec">Everything we <em>supply and place</em></h2><a class="link-arrow" href="/services/">All services</a></div><div class="cards cards-4">{cards}</div></div></section>
<section class="sec dark"><div class="wrap split">{action_media}<div class="split-copy"><p class="eyebrow">Why a stone slinger</p><h2>No wheelbarrows. No ruts. <em>No wasted weekend.</em></h2>
<ul class="ticks"><li>Reaches up to 100 ft, behind the house and over fences</li><li>Material lands level and where you want it</li><li>One operator, fast turnaround, lower labour cost</li><li>Truck stays on the road or driveway</li></ul>
<p><a class="btn btn-gold" href="/services/stone-slinger/">How the slinger works</a></p></div></div></section>
{projects_html()}<section class="sec tint"><div class="wrap"><h2 class="h-sec">From first call to <em>placed</em></h2>{steps}</div></section>
{work}{reviews_html()}
<section class="sec tint"><div class="wrap two"><div><h2 class="h-sec">Where we <em>work</em></h2><ul class="chips">{towns}</ul><p>Based in Kirkland Lake. Not on the list? Call, we cover nearby communities too.</p></div>
<div class="calc-teaser"><h2 class="h-sec">How much do you need?</h2><p>Enter length, width and depth and get cubic yards and tonnes in seconds.</p><p><a class="btn btn-dark" href="/gravel-calculator/">Open the gravel calculator</a></p></div></div></section>
<section class="sec"><div class="wrap narrow"><h2 class="h-sec">Common <em>questions</em></h2>{faq_html(FAQS[:4])}<p><a class="link-arrow" href="/faq/">More questions</a></p></div></section>
{cta()}""", schemas=[faq_schema(FAQS[:4])])

def page_services():
    cards = "".join(svc_card(s, v, "h2") for s, v in SERVICES.items())
    return layout("/services/", "Stone Slinger Services | Brownlee Sand & Gravel",
        "Stone slinger placement, gravel and crushed stone, topsoil and sand, and bulk delivery in Kirkland Lake, Timmins, Temiskaming Shores and area.",
        page_head("Our services", "Precise placement and bulk delivery for homeowners, contractors, cottages and farms.", "driveway-gravel", "Services") +
        f'<section class="sec"><div class="wrap"><div class="cards cards-4">{cards}</div></div></section>{cta()}',
        crumbs=[("/", "Home"), ("/services/", "Services")])

def page_service(slug):
    v = SERVICES[slug]
    others = "".join(f'<li><a href="/services/{s}/">{o["name"]}</a></li>' for s, o in SERVICES.items() if s != slug)
    towns = "".join(f'<li><a href="/service-areas/{s}/">{t["name"]}</a></li>' for s, t in TOWNS.items())
    body = "".join(f"<p>{p}</p>" for p in v["body"])
    pts = "".join(f"<li>{p}</li>" for p in v["points"])
    strip = [s for s in gallery_stems() if s not in ("hero", v["photo"])][:3]
    sx = "".join(f'<figure class="tile">{pic(s, sizes="(min-width:900px) 33vw, 100vw")}</figure>' for s in strip)
    strip_html = f'<section class="sec"><div class="wrap"><h2 class="h-sec">On the job</h2><div class="mosaic m3">{sx}</div></div></section>' if strip else ""
    svc = {"@context": "https://schema.org", "@type": "Service", "name": v["name"], "description": v["desc"], "provider": {"@id": BID},
           "areaServed": [{"@type": "City", "name": t["name"]} for t in TOWNS.values()], "serviceType": v["name"]}
    return layout(f"/services/{slug}/", f'{v["name"]} | Brownlee Sand & Gravel', v["desc"],
        page_head(v["h1"], v["blurb"], v.get("head", v["photo"]), "Services") +
        f"""<section class="sec"><div class="wrap two"><div class="prose">{body}<p class="actions"><a class="btn btn-gold" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="btn btn-line" href="/contact/">Request a quote</a></p></div>
<aside class="panel"><h2>At a glance</h2><ul class="ticks">{pts}</ul><h3>Other services</h3><ul class="plain">{others}</ul></aside></div></section>
{strip_html}{projects_html() if slug=="stone-slinger" else ""}
<section class="sec tint"><div class="wrap"><h2 class="h-sec">Where we provide this</h2><ul class="chips">{towns}</ul></div></section>
<section class="sec"><div class="wrap narrow"><h2 class="h-sec">Questions</h2>{faq_html(FAQS[:5])}</div></section>{cta()}""",
        crumbs=[("/", "Home"), ("/services/", "Services"), (f"/services/{slug}/", v["name"])], schemas=[svc, faq_schema(FAQS[:5])])

def page_areas():
    cards = ""
    for s, t in TOWNS.items():
        img = pic(t["photo"], sizes="(min-width:900px) 33vw, 100vw")
        media = f'<div class="card-media">{img}</div>' if img else ""
        cards += f'<article class="card">{media}<div class="card-body"><h2><a href="/service-areas/{s}/">{t["name"]}</a></h2><p>{t["lead"]}</p><p class="more">Services in {t["name"]}</p></div></article>'
    return layout("/service-areas/", "Service Areas | Brownlee Sand & Gravel",
        "Stone slinger and aggregate delivery in Kirkland Lake, Temiskaming Shores, Timmins, Larder Lake, Matheson, Cobalt and surrounding Northern Ontario.",
        page_head("Service areas", "Based in Kirkland Lake and serving the surrounding region. Not on the list? Call, we cover nearby communities.", "slinger-truck-job", "Northern Ontario") +
        f'<section class="sec"><div class="wrap"><div class="cards cards-3">{cards}</div></div></section>{cta()}',
        crumbs=[("/", "Home"), ("/service-areas/", "Service Areas")])

def page_town(slug):
    t = TOWNS[slug]; name = t["name"]
    others = "".join(f'<li><a href="/service-areas/{s}/">{o["name"]}</a></li>' for s, o in TOWNS.items() if s != slug)
    svcs = "".join(f'<li><a href="/services/{s}/">{v["name"]}</a></li>' for s, v in SERVICES.items())
    uses = "".join(f"<li>{u}</li>" for u in t["uses"])
    faqs = [(f"Do you serve {name}?", f"Yes. We serve {name}, including {t['near']}. Call {PHONE_DISPLAY} for a quote."),
            (f"What can you place in {name}?", "Gravel, crushed limestone, sand and topsoil, delivered in bulk or placed with the stone slinger."),
            ("How do I get a quote?", f"Call or text {PHONE_DISPLAY}, or use the contact form with your town, material and job size.")]
    return layout(f"/service-areas/{slug}/", f"Stone Slinger {name}, ON | Brownlee Sand & Gravel",
        f"Stone slinger, gravel, sand and topsoil in {name}, ON and {t['near']}. Free quote: {PHONE_DISPLAY}.",
        page_head(f"Stone slinger &amp; gravel delivery in {name}, ON", t["lead"], t["photo"], "Service area") +
        f"""<section class="sec"><div class="wrap two"><div class="prose"><h2>What we do in {name}</h2><ul class="ticks">{uses}</ul>
<p>We cover {name} and nearby {t["near"]}. The slinger places material up to 100 ft from the road or driveway, so tight lots and long laneways are no problem.</p>
<p class="actions"><a class="btn btn-gold" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></p></div>
<aside class="panel"><h2>Services</h2><ul class="plain">{svcs}</ul><h3>Estimate your load</h3><p><a href="/gravel-calculator/">Gravel calculator</a></p></aside></div></section>
<section class="sec tint"><div class="wrap"><h2 class="h-sec">Other areas we serve</h2><ul class="chips">{others}</ul></div></section>
<section class="sec"><div class="wrap narrow"><h2 class="h-sec">{name} FAQ</h2>{faq_html(faqs)}</div></section>{cta(f"Need material in {name}?")}""",
        crumbs=[("/", "Home"), ("/service-areas/", "Service Areas"), (f"/service-areas/{slug}/", name)],
        schemas=[faq_schema(faqs), {"@context": "https://schema.org", "@type": "Service", "name": f"Stone slinger and gravel delivery in {name}", "provider": {"@id": BID}, "areaServed": {"@type": "City", "name": name}}])

def page_calc():
    return layout("/gravel-calculator/", "Gravel Calculator | Brownlee Sand & Gravel",
        "Free gravel, sand and topsoil calculator. Enter length, width and depth to estimate cubic yards and tonnes for your driveway, pad or garden.",
        page_head("Gravel calculator", "Estimate how much gravel, crushed stone, sand or topsoil your project needs.", None, "Free tool") +
        f"""<section class="sec"><div class="wrap two"><form id="calc" class="panel form" novalidate>
<div class="f"><label for="len">Length (ft)</label><input id="len" type="number" inputmode="decimal" min="0" step="any" value="40"></div>
<div class="f"><label for="wid">Width (ft)</label><input id="wid" type="number" inputmode="decimal" min="0" step="any" value="12"></div>
<div class="f"><label for="dep">Depth (inches)</label><input id="dep" type="number" inputmode="decimal" min="0" step="any" value="4"></div>
<div class="f"><label for="mat">Material</label><select id="mat"><option value="1.4">Gravel</option><option value="1.4">Crushed limestone</option><option value="1.35">Sand</option><option value="1.1">Topsoil</option></select></div>
<div class="f"><label for="extra">Extra for settling and waste</label><select id="extra"><option value="1.1" selected>10% (recommended)</option><option value="1">None</option><option value="1.15">15%</option></select></div></form>
<div class="panel dark result" aria-live="polite"><h2>Your estimate</h2><p class="big"><span id="o-yd">0</span> <small>cubic yards</small></p><p class="big"><span id="o-t">0</span> <small>tonnes (approx.)</small></p><p><span id="o-m">0</span> cubic metres</p>
<p class="fine">Estimate only. Weight varies with moisture and stone size. Call for an exact quote.</p>
<p><a class="btn btn-gold" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></p></div></div></section>
<section class="sec"><div class="wrap narrow prose"><h2>How the estimate works</h2><p>Cubic yards equal length times width times depth in feet, divided by 27. We add an allowance for settling and waste, then convert to tonnes using typical bulk weights for each material.</p></div></section>{cta()}""",
        crumbs=[("/", "Home"), ("/gravel-calculator/", "Gravel Calculator")],
        schemas=[{"@context": "https://schema.org", "@type": "WebApplication", "name": "Gravel Calculator", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "url": SITE_URL + "/gravel-calculator/", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"}}])

def page_faq():
    return layout("/faq/", "Stone Slinger FAQ | Brownlee Sand & Gravel",
        "Answers about stone slinger service: reach, materials, timing, service areas and quotes from Brownlee Sand & Gravel in Kirkland Lake, ON.",
        page_head("Frequently asked questions", "Quick answers about stone slinger service.", None, "FAQ") +
        f'<section class="sec"><div class="wrap narrow">{faq_html(FAQS)}</div></section>{cta()}',
        crumbs=[("/", "Home"), ("/faq/", "FAQ")], schemas=[faq_schema(FAQS)])

def page_about():
    img = pic("hero", sizes="(min-width:900px) 50vw, 100vw")
    media = f'<div class="split-media">{img}</div>' if img else ""
    return layout("/about/", "About Matt Brownlee | Brownlee Sand & Gravel",
        "Brownlee Sand & Gravel is an owner-operated stone slinger business in Kirkland Lake, Ontario, run by Matt Brownlee.",
        page_head("About Brownlee Sand &amp; Gravel", "Owner-operated in Kirkland Lake, Ontario.", None, "About") +
        f"""<section class="sec"><div class="wrap split">{media}<div class="split-copy prose"><p>Brownlee Sand &amp; Gravel is run by {OWNER} out of {CITY}. Matt operates the stone slinger truck himself, so the person who quotes your job is the person who places your material.</p>
<p>We provide precise stone, topsoil and aggregate placement across Kirkland Lake, Temiskaming Shores, Timmins, Larder Lake, Matheson, Cobalt and surrounding Northern Ontario.</p>
<p class="actions"><a class="btn btn-gold" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></p></div></div></section>{cta()}""",
        crumbs=[("/", "Home"), ("/about/", "About")])

def page_gallery():
    stems = gallery_stems()
    if stems:
        g = '<div class="gallery">' + "".join(
            f'<figure class="g-item"><a href="/images/{s}-{PH[s]["widths"][-1]}.jpg" data-lightbox>{pic(s, sizes="(min-width:1100px) 33vw, (min-width:600px) 50vw, 100vw")}</a><figcaption>{esc(PH[s]["alt"])}</figcaption></figure>'
            for s in stems) + "</div>"
    else:
        g = f'<p class="notice">Job photos are being added. Follow our <a href="{FACEBOOK}" rel="noopener">Facebook page</a> for the latest work.</p>'
    return layout("/gallery/", "Our Work: Stone Slinger Job Photos | Brownlee Sand & Gravel",
        "Photos of stone slinger, gravel, sand and topsoil jobs across Kirkland Lake, Timmins and Temiskaming Shores by Brownlee Sand & Gravel.",
        page_head("Our work", "Real jobs from across Northern Ontario. Tap any photo to see it full size.", None, "Gallery") +
        f'<section class="sec"><div class="wrap">{g}</div></section>{cta()}',
        crumbs=[("/", "Home"), ("/gallery/", "Our Work")])

def page_contact():
    return layout("/contact/", "Contact & Free Quote | Brownlee Sand & Gravel",
        f"Call or text {PHONE_DISPLAY} or send a message for a free quote on stone slinger, gravel, sand and topsoil in Kirkland Lake and Northern Ontario.",
        page_head("Get a free quote", "Call or text, or tell us about the job and Matt will get back to you.", None, "Contact") +
        f"""<section class="sec"><div class="wrap two">
<form id="quote" action="{esc(FORM_ACTION)}" method="post" enctype="text/plain" class="panel form">
<div class="f"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
<div class="f"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="f"><label for="town">Job location (town)</label><input id="town" name="town" required></div>
<div class="f"><label for="service">Service</label><select id="service" name="service">{svc_options()}</select></div>
<div class="f"><label for="details">Job details (size, access, date)</label><textarea id="details" name="details" rows="5"></textarea></div>
<button class="btn btn-gold" type="submit">Send request</button></form>
<div class="panel dark contact-card"><h2>Reach Matt directly</h2><p class="big-phone"><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p><p>Call or text</p>
<address>{BUSINESS}<br>{STREET}<br>{CITY}, {REGION} {POSTAL}<br><a href="mailto:{EMAIL}">{EMAIL}</a></address><p>{HOURS}</p>
<p><a href="{FACEBOOK}" rel="noopener">Message us on Facebook</a></p></div></div></section>""",
        crumbs=[("/", "Home"), ("/contact/", "Contact")],
        schemas=[{"@context": "https://schema.org", "@type": "ContactPage", "url": SITE_URL + "/contact/"}])

def page_404():
    return layout("/404.html", "Page not found | Brownlee Sand & Gravel", "Page not found.",
        page_head("Page not found", 'That page has moved. <a href="/">Go to the home page</a> or <a href="/services/">see our services</a>.')).replace(
        'content="index,follow,max-image-preview:large"', 'content="noindex"')

CSS = r"""/* Brownlee design system v4: royal navy + safety yellow (Keller-style), Archivo display + Figtree body */
:root{
--ink:#0B1B2E;--ink-2:#1E2F45;--muted:#4A5D73;--line:#DCE3EA;--surface:#EEF2F6;--white:#FFFFFF;
--navy:#011D3F;--navy-2:#003B73;--navy-3:#1D5A9A;
--gold:#FDC600;--gold-hi:#FFD633;--gold-deep:#003B73;--gold-tint:#FFF4C2;
--r-sm:8px;--r-md:14px;--r-lg:20px;--r-pill:999px;
--sh-sm:0 1px 2px rgba(1,29,63,.06),0 1px 1px rgba(1,29,63,.04);--sh-md:0 10px 30px -12px rgba(1,29,63,.25);--sh-lg:0 30px 60px -20px rgba(1,29,63,.45);
--fd:"Archivo","Arial Black","Helvetica Neue",Arial,sans-serif;--fb:"Figtree",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
--ease:cubic-bezier(.2,.7,.2,1);--hdr:84px}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;scroll-padding-top:100px}
body{margin:0;font:400 1.0625rem/1.65 var(--fb);color:var(--ink);background:var(--white);-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}a{color:var(--gold-deep)}address{font-style:normal}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:4px}
.ico{width:18px;height:18px;flex:none}.chev{width:14px;height:14px;flex:none;transition:transform .25s var(--ease)}
.wrap{width:min(1240px,100% - 40px);margin-left:auto;margin-right:auto}.narrow{max-width:860px}
.skip{position:absolute;left:-999px;top:0;background:#000;color:#fff;padding:8px 12px;z-index:200}.skip:focus{left:8px;top:8px}
h1,h2,h3{font-family:var(--fd);font-stretch:semi-expanded;line-height:1.02;margin:0 0 .4em;letter-spacing:-.025em;color:inherit}
h1{font-size:clamp(2.6rem,6.2vw,5rem);font-weight:800}h2{font-size:clamp(2rem,4.4vw,3.4rem);font-weight:800}h3{font-size:1.4rem;font-weight:700;letter-spacing:-.015em}
h1 em,h2 em{font-style:normal;color:var(--gold)}.sec:not(.dark):not(.vs-sec) h2 em,.panel:not(.dark) h2 em{color:var(--ink);background:linear-gradient(transparent 58%,#FDC600 58%,#FDC600 90%,transparent 90%);padding:0 .06em}
.h-sec{max-width:20ch}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font:700 .8rem var(--fd);font-stretch:semi-expanded;color:var(--gold);letter-spacing:.16em;text-transform:uppercase;margin:0 0 14px}
.eyebrow:before{content:"";width:22px;height:3px;background:var(--gold);border-radius:2px}.eb-dark{color:var(--gold-deep)}
.lead{font-size:1.22rem;line-height:1.6}

/* utility bar */
.utility{background:var(--navy);color:#C9D3E0;font-size:.875rem}
.util-row{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:38px}
.utility p{margin:0;display:flex;align-items:center;gap:8px}.utility .ico{width:15px;height:15px;color:var(--gold)}
.u-mid{font-weight:600;color:#fff}.u-right{gap:16px}.utility a{color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:6px}
.u-call{font-weight:700;font-variant-numeric:tabular-nums}.u-call:hover{color:var(--gold-hi)}

/* header */
.site-header{background:#fff;color:var(--ink);position:sticky;top:0;z-index:100;border-bottom:1px solid var(--line);transition:box-shadow .25s var(--ease)}
.site-header.scrolled{box-shadow:0 8px 24px -12px rgba(1,29,63,.25)}
.bar{display:flex;align-items:center;gap:24px;min-height:var(--hdr);transition:min-height .25s var(--ease)}.scrolled .bar{min-height:68px}
.brand{display:flex;align-items:center;gap:12px;color:var(--ink);text-decoration:none;flex:none}
.brand-logo{width:58px;height:58px;border-radius:50%;background:#000;box-shadow:0 0 0 2px var(--gold);transition:width .25s var(--ease),height .25s var(--ease)}.scrolled .brand-logo{width:48px;height:48px}
.brand-mark{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;background:var(--gold);color:var(--ink);font:800 1.6rem var(--fd)}
.brand-text{font:800 1.45rem/.95 var(--fd);font-stretch:semi-expanded;letter-spacing:-.02em}.brand-text small{display:block;font:700 .66rem var(--fd);font-stretch:semi-expanded;letter-spacing:.2em;text-transform:uppercase;color:var(--navy-2);margin-top:5px}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;flex:1}
.nav-list{list-style:none;margin:0;padding:0;display:flex;align-items:center;gap:2px}
.nav-item{position:relative}
.nav-link{display:inline-flex;align-items:center;gap:6px;white-space:nowrap;color:var(--ink);background:none;border:0;cursor:pointer;text-decoration:none;padding:10px 13px;font:600 1rem var(--fb);border-radius:var(--r-sm);transition:background .2s,color .2s}
.nav-link:hover,.drop-btn[aria-expanded="true"]{background:var(--surface)}
.nav-link[aria-current],.nav-item[data-on]>.nav-link{color:var(--gold-deep)}
.nav-link[aria-current]{box-shadow:inset 0 -3px 0 var(--gold)}
.drop-btn[aria-expanded="true"] .chev{transform:rotate(180deg)}
.drop{position:absolute;top:calc(100% + 12px);left:-8px;min-width:300px;background:var(--white);color:var(--ink);border-radius:var(--r-lg);box-shadow:var(--sh-lg);border:1px solid var(--line);padding:16px;visibility:hidden;opacity:0;transform:translateY(8px);transition:opacity .2s var(--ease),transform .2s var(--ease),visibility 0s .2s}
.drop.open{visibility:visible;opacity:1;transform:none;transition:opacity .2s var(--ease),transform .2s var(--ease)}
.drop.mega{width:min(780px,92vw)}.drop.small{min-width:270px}
.drop:before{content:"";position:absolute;top:-16px;left:0;right:0;height:16px}
.mega-grid{display:grid;grid-template-columns:1fr 240px;gap:16px}
.drop-list{list-style:none;margin:0;padding:0;display:grid;gap:2px}.drop-list.two{grid-template-columns:1fr 1fr}
.drop-list a{display:block;padding:10px 12px;border-radius:var(--r-sm);text-decoration:none;color:var(--ink);transition:background .15s}
.drop-list a strong{display:block;font:600 1rem var(--fb)}.drop-list a span{display:block;font-size:.86rem;color:var(--muted)}
.drop-list a:hover,.drop-list a[aria-current]{background:var(--surface)}.drop-list a:hover strong{color:var(--gold-deep)}
.mega-card{background:var(--navy);color:#D5DEEA;border-radius:var(--r-md);padding:20px;position:relative;overflow:hidden}
.mega-card:after{content:"";position:absolute;right:-30px;bottom:-30px;width:120px;height:120px;border-radius:50%;border:18px solid rgba(253,198,0,.18)}
.mega-card p{margin:0 0 12px;font-size:.95rem;position:relative}.mc-k{font:800 1.3rem/1.05 var(--fd);font-stretch:semi-expanded;letter-spacing:-.02em;color:#fff}.mc-ph a{color:var(--gold-hi);font:800 1.15rem var(--fd);text-decoration:none}
.drop-foot{margin:12px 0 0;padding:12px 12px 2px;border-top:1px solid var(--line);font-size:.9rem;color:var(--muted)}.drop-foot a{font-weight:700}
.nav-cta{display:flex;align-items:center;gap:10px;flex:none}

/* buttons */
.btn{position:relative;overflow:hidden;display:inline-flex;align-items:center;justify-content:center;gap:10px;white-space:nowrap;padding:15px 26px;border-radius:var(--r-sm);font:700 1.02rem var(--fb);letter-spacing:.005em;text-decoration:none;min-height:52px;border:2px solid transparent;cursor:pointer;transition:background .2s,transform .2s var(--ease),box-shadow .2s,border-color .2s}
.btn:hover{transform:translateY(-2px)}.btn:active{transform:translateY(0)}
.btn-gold{background:var(--gold);color:var(--ink);box-shadow:0 8px 20px -8px rgba(253,198,0,.7)}.btn-gold:hover{background:var(--gold-hi);box-shadow:0 12px 26px -8px rgba(253,198,0,.8)}
.btn-gold:after{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-20deg);transition:left .6s var(--ease)}.btn-gold:hover:after{left:130%}
.btn-dark{background:var(--navy);color:#fff}.btn-dark:hover{background:var(--navy-2)}
.btn-ghost{border-color:rgba(255,255,255,.6);color:#fff;background:rgba(255,255,255,.06)}.btn-ghost:hover{background:rgba(255,255,255,.14);border-color:#fff}
.btn-line{border-color:var(--ink);color:var(--ink)}.btn-line:hover{background:var(--ink);color:#fff}
.btn-phone{border-color:var(--line);color:var(--ink);font-variant-numeric:tabular-nums;padding:12px 16px;min-height:48px}.btn-phone:hover{border-color:var(--gold)}.btn-phone .ico{color:var(--navy-2)}
.btn-sm{padding:10px 16px;min-height:44px;font-size:.95rem}.btn-block{width:100%}
.menu-btn,.m-call{display:none}
.actions{display:flex;flex-wrap:wrap;gap:12px}

.crumbs{width:min(1240px,100% - 40px);margin:0 auto;padding:16px 0 0;font-size:.88rem}
.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:center;gap:4px}
.crumbs li{display:inline-flex;align-items:center;gap:4px}
.crumbs li+li:before{content:"";width:6px;height:6px;margin:0 8px 0 4px;border-top:1.5px solid currentColor;border-right:1.5px solid currentColor;transform:rotate(45deg);opacity:.55}
.crumbs a{display:inline-flex;align-items:center;gap:6px;color:var(--muted);text-decoration:none;padding:4px 6px;border-radius:6px;transition:background .2s,color .2s}.crumbs a:hover{color:var(--ink);background:var(--surface)}
.crumbs .ico{width:15px;height:15px}.crumbs [aria-current]{font-weight:600;color:var(--ink);padding:4px 6px}
.head-inner .crumbs+.eyebrow{display:none}.head-inner .crumbs{width:fit-content;max-width:100%;margin:0 0 26px;padding:0;display:flex;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:4px 12px 4px 6px;color:#C9D6E6}
.head-inner .crumbs a{color:#C9D6E6}.head-inner .crumbs a:hover{color:#fff;background:rgba(255,255,255,.1)}.head-inner .crumbs [aria-current]{color:var(--gold)}

/* hero */
.hero{position:relative;background:var(--navy);color:#fff;overflow:hidden;padding:96px 0 104px;isolation:isolate}
.hero-bg,.head-bg,.cta-bg{position:absolute;top:0;right:0;bottom:0;left:0;width:100%;height:100%;object-fit:cover;z-index:-2}
.hero-bg{object-position:65% 50%;animation:kenburns 18s var(--ease) both}
@keyframes kenburns{from{transform:scale(1.08)}to{transform:scale(1)}}
.hero.has-photo:after{content:"";position:absolute;top:0;right:0;bottom:0;left:0;z-index:-1;background:linear-gradient(105deg,rgba(1,29,63,.96) 0%,rgba(1,29,63,.84) 46%,rgba(1,29,63,.35) 100%)}
.hero-arc{position:absolute;right:4%;top:6%;width:min(560px,48vw);height:auto;z-index:-1;opacity:.9;pointer-events:none}
.hero-arc path{stroke-dasharray:6 14;animation:dash 2.4s linear infinite}
@keyframes dash{to{stroke-dashoffset:-40}}
.hero-grid{position:relative;display:grid;grid-template-columns:1.3fr 1fr;gap:56px;align-items:center}
.hero-copy{min-width:0}.hero .lead{max-width:36rem;color:#DDE5EE}.hero-art{margin-top:26px;border-radius:var(--r-md);overflow:hidden}
.hero .eyebrow{color:var(--gold)}
.chips-hero{list-style:none;padding:0;margin:26px 0 0;display:flex;flex-wrap:wrap;gap:8px}
.chips-hero li{display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);padding:7px 14px;border-radius:var(--r-pill);font:600 .9rem var(--fb)}
.chips-hero li:before{content:"";width:8px;height:8px;border-radius:50%;background:var(--gold);box-shadow:0 0 0 4px rgba(253,198,0,.2)}
.load-in{animation:rise .8s var(--ease) both}.load-in.d1{animation-delay:.08s}.load-in.d2{animation-delay:.16s}.load-in.d3{animation-delay:.24s}.load-in.d4{animation-delay:.32s}.load-in.d5{animation-delay:.42s}
@keyframes rise{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
.quick{background:var(--white);color:var(--ink);border-radius:var(--r-lg);padding:30px;box-shadow:var(--sh-lg);min-width:0;position:relative}
.quick:before{content:"";position:absolute;left:30px;right:30px;top:0;height:4px;border-radius:0 0 4px 4px;background:var(--gold)}
.quick h2{font-size:1.9rem;margin:0}.quick .sub{margin:4px 0 18px;color:var(--muted)}.quick .fine{color:var(--muted);margin:12px 0 0;text-align:center}
.f{margin:0 0 14px;min-width:0}.f label{display:block;font-weight:600;font-size:.92rem;margin-bottom:6px;color:var(--ink-2)}
.f input,.f select,.f textarea{width:100%;padding:13px 14px;font:inherit;font-size:1rem;border:1.5px solid #C5D0DC;border-radius:var(--r-sm);min-height:50px;background:#FAFCFE;color:var(--ink);transition:border-color .15s,box-shadow .15s,background .15s}
.f input:hover,.f select:hover,.f textarea:hover{border-color:#9FB0C3}
.f input:focus,.f select:focus,.f textarea:focus{border-color:var(--navy-3);background:#fff;box-shadow:0 0 0 4px rgba(31,61,107,.12);outline:0}
.fg{display:grid;grid-template-columns:1fr 1fr;gap:14px}

/* ticker */
.ticker{background:var(--gold);color:var(--navy);overflow:hidden;white-space:nowrap;border-top:1px solid rgba(0,0,0,.06)}
.ticker-track{display:inline-flex;gap:0;animation:marquee 40s linear infinite;padding:14px 0}
.ticker span{display:inline-flex;align-items:center;gap:22px;padding-right:22px;font:800 1.05rem var(--fd);font-stretch:semi-expanded;letter-spacing:-.01em}
.ticker span:after{content:"";width:8px;height:8px;background:var(--navy);transform:rotate(45deg)}
@keyframes marquee{to{transform:translateX(-50%)}}

/* stats */
.stats{background:var(--navy);border-bottom:0}.stats dl{display:grid;grid-template-columns:repeat(4,1fr);margin:0}
.stats div{padding:34px 18px;text-align:left;border-left:1px solid rgba(255,255,255,.12)}.stats div:first-child{border-left:0;padding-left:0}
.stats dt{font:600 .85rem var(--fb);color:#AFC0D4;order:2}.stats dd{margin:0 0 4px;font:800 clamp(1.9rem,3.6vw,2.8rem)/1 var(--fd);font-stretch:semi-expanded;letter-spacing:-.03em;color:var(--gold)}
.stats div{display:flex;flex-direction:column-reverse}

/* sections */
.sec{padding:112px 0}.sec.tint{background:var(--surface)}.sec.dark{background:var(--navy);color:#D5DEEA}.sec.dark h2{color:#fff}
.sec-head{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;margin-bottom:36px}.sec-head .h-sec{margin:0}
.link-arrow{display:inline-flex;align-items:center;gap:8px;font:700 1rem var(--fb);text-decoration:none;color:var(--gold-deep)}.link-arrow:after{content:"\2192";transition:transform .2s var(--ease)}.link-arrow:hover:after{transform:translateX(4px)}

/* versus */
.vs-sec{background:var(--navy);color:#C9D3E0}.vs-sec h2{color:#fff}.vs-sec h2 em{color:var(--gold);background:none}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:40px}
.vs-col{border-radius:var(--r-lg);padding:34px;position:relative}.vs-col ul{list-style:none;margin:0;padding:0}.vs-col li{padding:11px 0 11px 34px;position:relative;border-top:1px solid rgba(255,255,255,.1)}
.vs-k{font:700 .78rem var(--fd);font-stretch:semi-expanded;letter-spacing:.16em;text-transform:uppercase;margin:0 0 8px}
.vs-bad{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.12)}.vs-bad h3{color:#fff}.vs-bad .vs-k{color:#8C99AB}
.vs-bad li:before{content:"\2715";position:absolute;left:4px;top:11px;color:#F28B82;font-weight:800}
.vs-good{background:var(--gold);color:var(--ink);box-shadow:0 30px 60px -25px rgba(253,198,0,.55)}.vs-good h3{color:var(--ink)}.vs-good .vs-k{color:var(--navy-2)}.vs-good li{border-top-color:rgba(0,0,0,.12)}
.vs-good li:before{content:"\2713";position:absolute;left:4px;top:11px;color:var(--ink);font-weight:900}
.vs-mid{display:none}

/* cards */
.cards{display:grid;gap:22px}.cards-4{grid-template-columns:repeat(4,1fr)}.cards-3{grid-template-columns:repeat(3,1fr)}.cards-2{grid-template-columns:repeat(2,1fr)}
.card{position:relative;background:var(--white);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .3s var(--ease),transform .3s var(--ease),border-color .3s}
.card:hover{box-shadow:var(--sh-md);transform:translateY(-6px);border-color:transparent}
.card-media{height:210px;overflow:hidden;background:var(--surface);position:relative}.card-media img{width:100%;height:100%;object-fit:cover;transition:transform .7s var(--ease)}.card:hover .card-media img{transform:scale(1.07)}
.card-body{padding:22px 22px 24px;flex:1;display:flex;flex-direction:column}.card-body p{margin:0 0 14px;color:var(--muted);font-size:.98rem}.card-body .more{margin-top:auto}
.card h2,.card h3{font-size:1.32rem;margin-bottom:.45em}.card h2 a,.card h3 a{color:var(--ink);text-decoration:none}.card h2 a:after,.card h3 a:after{content:"";position:absolute;top:0;right:0;bottom:0;left:0}
.more{display:inline-flex;align-items:center;gap:8px;font:700 .95rem var(--fb);color:var(--gold-deep);margin:0}.more:after{content:"\2192";transition:transform .2s var(--ease)}.card:hover .more:after{transform:translateX(5px)}

.split{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}.split>*{min-width:0}
.split-media{border-radius:var(--r-lg);overflow:hidden;box-shadow:var(--sh-lg);position:relative}.split-media img,.split-media svg{width:100%;height:auto}
.split-media:after{content:"";position:absolute;left:18px;bottom:18px;width:64px;height:64px;border-radius:50%;background:var(--gold);box-shadow:0 0 0 10px rgba(253,198,0,.25)}
.ticks{list-style:none;padding:0;margin:0 0 1.4em}.ticks li{padding-left:36px;position:relative;margin:.7em 0;font-weight:500}
.ticks li:before{content:"";position:absolute;left:0;top:.15em;width:24px;height:24px;border-radius:50%;background:var(--gold);border:0}
.ticks li:after{content:"";position:absolute;left:8px;top:.48em;width:8px;height:5px;border-left:2.5px solid var(--navy);border-bottom:2.5px solid var(--navy);transform:rotate(-45deg)}
.sec.dark .ticks li:before,.ticks.light li:before{background:var(--gold)}.sec.dark .ticks li:after,.ticks.light li:after{border-color:var(--navy)}
.steps{list-style:none;counter-reset:s;display:grid;gap:20px;grid-template-columns:repeat(4,1fr);padding:0;margin:0;position:relative}
.steps li{counter-increment:s;background:var(--white);border:1px solid var(--line);border-radius:var(--r-lg);padding:28px;position:relative}
.steps li:before{content:counter(s);display:grid;place-items:center;width:48px;height:48px;border-radius:50%;background:var(--gold);color:var(--navy);font:800 1.3rem var(--fd);margin-bottom:18px}
.steps h3{font-size:1.2rem}.steps p{margin:0;color:var(--muted)}
.mosaic{display:grid;gap:12px;grid-template-columns:repeat(4,1fr);grid-auto-rows:220px}
.mosaic .tile{margin:0;overflow:hidden;border-radius:var(--r-md);background:var(--surface)}.mosaic .tile:first-child{grid-column:span 2;grid-row:span 2}
.mosaic.m3{grid-template-columns:repeat(3,1fr);grid-auto-rows:250px}.mosaic.m3 .tile:first-child{grid-column:auto;grid-row:auto}
.tile img,.tile picture{width:100%;height:100%;object-fit:cover;transition:transform .7s var(--ease)}.tile:hover img{transform:scale(1.05)}
.two{display:grid;grid-template-columns:1.2fr 1fr;gap:56px}.two>*{min-width:0}
.chips{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:10px}
.chips a{display:inline-flex;align-items:center;gap:8px;background:var(--white);color:var(--ink);border:1px solid var(--line);text-decoration:none;padding:11px 18px;border-radius:var(--r-pill);font:600 .98rem var(--fb);transition:all .2s var(--ease)}
.chips a:before{content:"";width:8px;height:8px;border-radius:50%;background:var(--gold);box-shadow:0 0 0 3px rgba(253,198,0,.25)}.chips a:hover{background:var(--navy);color:#fff;border-color:var(--navy);transform:translateY(-2px)}
.proj{list-style:none;padding:0;margin:20px 0 0;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.proj li{background:var(--white);border:1px solid var(--line);border-radius:var(--r-md);padding:18px 18px 18px 50px;font:600 1rem var(--fb);position:relative;transition:border-color .2s,transform .2s var(--ease)}
.proj li:before{content:"";position:absolute;left:18px;top:50%;width:18px;height:18px;margin-top:-9px;border-radius:5px;background:var(--gold);transform:rotate(45deg) scale(.7)}
.proj li:hover{border-color:var(--gold);transform:translateY(-2px)}
.calc-teaser{background:var(--navy);color:#D5DEEA;border-radius:var(--r-lg);padding:32px}.calc-teaser h2{color:#fff}.calc-teaser .btn-dark{background:var(--gold);color:var(--ink)}
.page-head{position:relative;background:var(--navy);color:#fff;padding:80px 0;overflow:hidden;isolation:isolate}
.page-head.has-photo{padding:120px 0 104px}.page-head.has-photo:after{content:"";position:absolute;top:0;right:0;bottom:0;left:0;z-index:-1;background:linear-gradient(100deg,rgba(1,29,63,.94),rgba(1,29,63,.55))}
.head-inner{position:relative}.page-head h1{font-size:clamp(2.3rem,5.4vw,4.2rem);max-width:20ch}.page-head .lead{margin:0;max-width:42rem;color:#DDE5EE}.page-head .lead a{color:var(--gold-hi)}
.panel{background:var(--surface);padding:30px;border-radius:var(--r-lg);border:1px solid var(--line)}.panel.dark{background:var(--navy);color:#D5DEEA;border-color:var(--navy)}.panel.dark h2{color:#fff}.panel.dark a{color:var(--gold-hi)}.panel h2{font-size:1.7rem}
.prose{max-width:46rem}.prose p{margin:0 0 1.1em}.prose h2{font-size:clamp(1.7rem,3vw,2.2rem)}
.gallery{columns:3 300px;column-gap:14px}.g-item{margin:0 0 14px;break-inside:avoid;border-radius:var(--r-md);overflow:hidden;background:var(--white);border:1px solid var(--line);transition:box-shadow .3s var(--ease)}
.g-item:hover{box-shadow:var(--sh-md)}.g-item a{display:block;overflow:hidden}.g-item img{transition:transform .6s var(--ease)}.g-item:hover img{transform:scale(1.04)}.g-item figcaption{padding:12px 14px;font-size:.9rem;color:var(--muted)}
.notice{background:var(--surface);padding:22px;border-radius:var(--r-md)}
.faq details{border:1px solid var(--line);border-radius:var(--r-md);margin:10px 0;background:var(--white);transition:box-shadow .2s,border-color .2s}
.faq details[open]{border-color:var(--gold);box-shadow:var(--sh-sm)}
.faq summary{cursor:pointer;padding:20px 60px 20px 22px;font:600 1.08rem var(--fb);list-style:none;position:relative}
.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";position:absolute;right:18px;top:50%;transform:translateY(-50%);width:30px;height:30px;display:grid;place-items:center;border-radius:50%;background:var(--surface);color:var(--ink);font:600 1.3rem/1 var(--fb);transition:background .2s,transform .2s}
.faq details[open] summary:after{content:"\2212";background:var(--gold)}.faq details p{margin:0;padding:0 22px 20px;color:var(--muted)}
.review{margin:0;background:var(--surface);border-radius:var(--r-md);padding:24px}.review footer{font-weight:700;color:var(--muted)}

/* quote band */
.qband{position:relative;background:var(--navy);color:#D5DEEA;padding:112px 0;overflow:hidden;isolation:isolate}
.qband:after{content:"";position:absolute;top:0;right:0;bottom:0;left:0;z-index:-1;background:linear-gradient(90deg,rgba(1,29,63,.97),rgba(1,29,63,.86))}
.qband:before{content:"";position:absolute;top:0;left:0;right:0;height:8px;background:repeating-linear-gradient(-45deg,#FDC600 0,#FDC600 16px,#011D3F 16px,#011D3F 32px)}
.qband-grid{position:relative;display:grid;grid-template-columns:1fr 1.1fr;gap:64px;align-items:center}.qband-grid>*{min-width:0}
.qband h2{color:#fff;font-size:clamp(2.3rem,5vw,3.8rem)}.qband a{color:var(--gold-hi)}
.quote-form{background:var(--white);color:var(--ink);border-radius:var(--r-lg);padding:32px;box-shadow:var(--sh-lg)}.quote-form .fine{text-align:center;color:var(--muted);margin:12px 0 0}.quote-form .fine a{color:var(--gold-deep)}
.result .big{font:800 clamp(2.4rem,6vw,3.6rem)/1 var(--fd);font-stretch:semi-expanded;letter-spacing:-.03em;margin:.2em 0;color:var(--gold)}.result .big small{font:600 1rem var(--fb);color:#C9D3E0;letter-spacing:0}
.fine{font-size:.9rem;color:#9FB0BD}.big-phone{font:800 2.4rem/1 var(--fd);font-stretch:semi-expanded;letter-spacing:-.02em;margin:.2em 0}.big-phone a{text-decoration:none}

/* footer */
.site-footer{background:#00142D;color:#AEB9C7}.site-footer a{color:#E8EDF3;text-decoration:none}.site-footer a:hover{color:var(--gold-hi)}
.site-footer h2{font:700 .8rem var(--fd);font-stretch:semi-expanded;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin-bottom:14px}.site-footer h2.mt{margin-top:1.6em}
.site-footer .brand,.site-footer .brand-text{color:#fff}.site-footer .brand-text small{color:var(--gold)}
.foot{display:grid;grid-template-columns:1.5fr 1fr 1fr 1.2fr;gap:40px;padding:72px 0 32px}.foot>*{min-width:0}
.foot-call{margin:0}.foot-call a{font:800 2rem var(--fd);font-stretch:semi-expanded;letter-spacing:-.02em;color:var(--gold)}.foot-sub{margin:0;font-size:.9rem}
.plain{list-style:none;padding:0;margin:0}.plain li{margin:.45em 0}.copy{padding:20px 0 32px;font-size:.88rem;border-top:1px solid #0D2A4F}

/* reveal on scroll (content visible without JS) */
.js .reveal{opacity:0;transform:translateY(28px);transition:opacity .8s var(--ease),transform .8s var(--ease)}
.js .reveal.in{opacity:1;transform:none}

.mbar{display:none}
.lightbox{border:0;padding:0;background:transparent;max-width:min(1200px,94vw);max-height:92vh}.lightbox::backdrop{background:rgba(5,10,18,.92)}
.lightbox img{max-height:84vh;width:auto;margin:0 auto;border-radius:var(--r-md)}.lightbox p{color:#fff;text-align:center;margin:12px 0 0}
.lb-close{position:fixed;top:14px;right:18px;width:48px;height:48px;border-radius:50%;border:0;background:var(--gold);color:var(--ink);font-size:2rem;line-height:1;cursor:pointer}

@media(max-width:1320px){.btn-phone span{display:none}.btn-phone{padding:12px}.nav-link{padding:10px 10px;font-size:.96rem}.bar{gap:16px}}
@media(max-width:1000px){.cards-4{grid-template-columns:repeat(2,1fr)}.steps{grid-template-columns:repeat(2,1fr)}.foot{grid-template-columns:1fr 1fr}.u-mid{display:none}}
@media(max-width:1120px){
 :root{--hdr:68px}.utility{display:none}body{padding-bottom:64px}
 .bar{gap:10px}.brand-logo{width:48px;height:48px}.brand-text{font-size:1.25rem}
 .m-call{display:grid;place-items:center;margin-left:auto;width:48px;height:48px;border-radius:var(--r-sm);background:var(--gold);color:var(--ink)}.m-call .ico{width:22px;height:22px}
 .menu-btn{display:inline-flex;align-items:center;gap:10px;background:var(--white);color:var(--ink);border:1.5px solid var(--line);border-radius:var(--r-sm);padding:0 14px;height:48px;font:700 .95rem var(--fb)}
 .burger,.burger:before,.burger:after{display:block;width:20px;height:2px;background:currentColor;position:relative;border-radius:2px;transition:transform .25s var(--ease),background .2s}.burger:before,.burger:after{content:"";position:absolute;left:0}.burger:before{top:-6px}.burger:after{top:6px}
 .menu-btn[aria-expanded="true"] .burger{background:transparent}.menu-btn[aria-expanded="true"] .burger:before{transform:translateY(6px) rotate(45deg)}.menu-btn[aria-expanded="true"] .burger:after{transform:translateY(-6px) rotate(-45deg)}
 .nav{display:none;position:fixed;top:var(--navtop,69px);left:0;right:0;bottom:0;background:var(--white);flex-direction:column;align-items:stretch;justify-content:flex-start;overflow-y:auto;padding:8px 20px 28px;gap:0;animation:rise .3s var(--ease)}
 .nav.open{display:flex}
 .nav-list{flex-direction:column;align-items:stretch;gap:0}.nav-item{border-bottom:1px solid var(--line)}
 .nav-link{width:100%;justify-content:space-between;padding:0 4px;min-height:58px;font-size:1.12rem;border-radius:0}.nav-link:hover,.drop-btn[aria-expanded="true"]{background:none}.nav-link[aria-current]{box-shadow:none}
 .drop,.drop.mega,.drop.small{position:static;width:auto;min-width:0;box-shadow:none;border:0;border-radius:var(--r-md);margin:0 0 14px;padding:6px;background:var(--surface);display:none;visibility:visible;opacity:1;transform:none;transition:none}
 .drop.open{display:block}.drop:before{display:none}.mega-grid{grid-template-columns:1fr}.mega-card{display:none}.drop-list.two{grid-template-columns:1fr}
 .drop-list a{min-height:48px}.drop-list a:hover,.drop-list a[aria-current]{background:var(--white)}
 .nav-cta{flex-direction:column;align-items:stretch;margin-top:20px}.btn-phone span{display:inline}.nav-cta .btn{width:100%}
 .mbar{display:grid;grid-template-columns:1fr 1fr 1.25fr;position:fixed;left:0;right:0;bottom:0;z-index:90;background:var(--white);box-shadow:0 -6px 20px -8px rgba(1,29,63,.25);border-top:1px solid var(--line)}
 .mbar a{display:flex;align-items:center;justify-content:center;gap:8px;min-height:62px;font:700 1rem var(--fb);text-decoration:none;color:var(--ink);border-right:1px solid var(--line)}
 .mbar a .ico{color:var(--navy-2)}.mbar .mbar-q{background:var(--gold);border:0}.mbar .mbar-q .ico{color:var(--ink)}
 .hero-grid,.split,.two,.qband-grid{grid-template-columns:1fr;gap:32px}.cards-3{grid-template-columns:1fr 1fr}
 .stats dl{grid-template-columns:1fr 1fr}.stats div{padding:24px 16px}.stats div:nth-child(odd){border-left:0;padding-left:0}.stats div:nth-child(n+3){border-top:1px solid rgba(255,255,255,.12)}
 .vs{grid-template-columns:1fr}.hero-arc{opacity:.35}
 .mosaic{grid-template-columns:1fr 1fr;grid-auto-rows:170px}.mosaic.m3{grid-template-columns:1fr 1fr;grid-auto-rows:170px}.proj{grid-template-columns:1fr 1fr}
 .sec,.qband{padding:72px 0}.hero{padding:56px 0 64px}.page-head{padding:56px 0}.page-head.has-photo{padding:80px 0 64px}
 body.nav-open{overflow:hidden}}
@media(max-width:600px){.cards-2,.cards-3,.cards-4,.steps,.proj{grid-template-columns:1fr}.foot{grid-template-columns:1fr}.fg{grid-template-columns:1fr;gap:0}.mb-label{display:none}.menu-btn{padding:0 13px}.brand-text{font-size:1.1rem}.brand-text small{font-size:.58rem}.wrap,.crumbs{width:calc(100% - 32px)}.quick,.quote-form{padding:22px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*:before,*:after{animation:none!important;transition:none!important}.js .reveal{opacity:1;transform:none}}
"""

JS = r"""document.documentElement.classList.add('js');(function(){
var hdr=document.getElementById('top-bar'),nav=document.getElementById('site-nav'),mb=document.querySelector('.menu-btn');
var mq=window.matchMedia('(max-width:1120px)');
function closeDrops(except){document.querySelectorAll('.drop-btn[aria-expanded="true"]').forEach(function(b){if(b!==except){b.setAttribute('aria-expanded','false');var d=document.getElementById(b.getAttribute('aria-controls'));if(d)d.classList.remove('open');}});}
document.querySelectorAll('.drop-btn').forEach(function(b){
  var d=document.getElementById(b.getAttribute('aria-controls')),li=b.parentNode,t;
  function open(){closeDrops(b);b.setAttribute('aria-expanded','true');d.classList.add('open');}
  function close(){b.setAttribute('aria-expanded','false');d.classList.remove('open');}
  b.addEventListener('click',function(e){e.stopPropagation();b.getAttribute('aria-expanded')==='true'?close():open();});
  li.addEventListener('mouseenter',function(){if(!mq.matches){clearTimeout(t);open();}});
  li.addEventListener('mouseleave',function(){if(!mq.matches){t=setTimeout(close,180);}});
  li.addEventListener('focusout',function(e){if(!mq.matches&&!li.contains(e.relatedTarget))close();});
});
document.addEventListener('click',function(e){if(!e.target.closest('.has-drop'))closeDrops();});
function setNav(o){if(!nav||!mb)return;nav.classList.toggle('open',o);mb.setAttribute('aria-expanded',o?'true':'false');document.body.classList.toggle('nav-open',o);
  if(o&&hdr){document.documentElement.style.setProperty('--navtop',hdr.getBoundingClientRect().bottom+'px');var f=nav.querySelector('a,button');if(f)f.focus();}}
if(mb)mb.addEventListener('click',function(){setNav(!nav.classList.contains('open'));});
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){if(nav&&nav.classList.contains('open')){setNav(false);mb.focus();}closeDrops();}
  if(e.key==='Tab'&&nav&&nav.classList.contains('open')){var f=[mb].concat([].slice.call(nav.querySelectorAll('a,button'))).filter(function(x){return x.offsetParent!==null;});var i=f.indexOf(document.activeElement);
    if(e.shiftKey&&i<=0){e.preventDefault();f[f.length-1].focus();}else if(!e.shiftKey&&i===f.length-1){e.preventDefault();f[0].focus();}}
});
if(nav)nav.addEventListener('click',function(e){var a=e.target.closest('a');if(a&&mq.matches)setNav(false);});
mq.addEventListener&&mq.addEventListener('change',function(){setNav(false);closeDrops();});
var cand=document.querySelectorAll('.sec .h-sec,.sec .eyebrow,.card,.steps li,.vs-col,.proj li,.tile,.g-item,.split-media,.split-copy,.panel,.faq details,.quote-form,.qb-copy,.calc-teaser,.stats div');
if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
var k=0;cand.forEach(function(el){if(el.getBoundingClientRect().top>window.innerHeight){el.classList.add('reveal');el.style.transitionDelay=((k++%4)*70)+'ms';io.observe(el);}});
setTimeout(function(){document.querySelectorAll('.reveal:not(.in)').forEach(function(el){if(el.getBoundingClientRect().top<window.innerHeight)el.classList.add('in');});},2500);}
document.querySelectorAll('.stats dd').forEach(function(dd){var m=dd.textContent.match(/^(\D*)(\d+)(.*)$/);if(!m||matchMedia('(prefers-reduced-motion: reduce)').matches)return;var end=+m[2],st=null;function f(t){if(!st)st=t;var p=Math.min((t-st)/1200,1);dd.textContent=m[1]+Math.round(end*(1-Math.pow(1-p,3)))+m[3];if(p<1)requestAnimationFrame(f);}
var o=new IntersectionObserver(function(es){if(es[0].isIntersecting){requestAnimationFrame(f);o.disconnect();}});o.observe(dd);});
var onS=function(){if(hdr)hdr.classList.toggle('scrolled',window.scrollY>40);};window.addEventListener('scroll',onS,{passive:true});onS();
var d=document.getElementById('lightbox');
if(d&&d.showModal){var li=document.getElementById('lb-img'),lc=document.getElementById('lb-cap');
document.querySelectorAll('[data-lightbox]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var im=a.querySelector('img');li.src=a.getAttribute('href');li.alt=im?im.alt:'';lc.textContent=im?im.alt:'';d.showModal();});});
d.querySelector('.lb-close').addEventListener('click',function(){d.close();});d.addEventListener('click',function(e){if(e.target===d)d.close();});}
var f=document.getElementById('calc');
if(f){var g=function(i){return document.getElementById(i)};
function calc(){var l=parseFloat(g('len').value)||0,w=parseFloat(g('wid').value)||0,dp=parseFloat(g('dep').value)||0;
var yd=(l*w*(dp/12)/27)*parseFloat(g('extra').value);var t=yd*parseFloat(g('mat').value)*0.9072;var m=yd*0.7646;
g('o-yd').textContent=yd.toFixed(1);g('o-t').textContent=t.toFixed(1);g('o-m').textContent=m.toFixed(1);}
f.addEventListener('input',calc);f.addEventListener('submit',function(e){e.preventDefault();});calc();}
})();
"""

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="#0b1620"/><text x="32" y="45" font-size="38" font-weight="900" text-anchor="middle" fill="#f5b800" font-family="Arial,sans-serif">B</text></svg>'

def write(rel, content):
    p = DIST / rel.lstrip("/"); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding="utf-8")

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    process_photos()
    make_og_card()
    pages = {"/": page_home(), "/services/": page_services(), "/service-areas/": page_areas(),
             "/gravel-calculator/": page_calc(), "/gallery/": page_gallery(), "/faq/": page_faq(), "/about/": page_about(), "/contact/": page_contact()}
    for s in SERVICES: pages[f"/services/{s}/"] = page_service(s)
    for s in TOWNS: pages[f"/service-areas/{s}/"] = page_town(s)
    for path, content in pages.items(): write(path + "index.html", content)
    write("/404.html", page_404())
    write("/assets/style.css", CSS); write("/assets/site.js", JS); write("/assets/favicon.svg", FAVICON)
    write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    urls = ""
    for p in pages:
        imgs = ""
        if p == "/gallery/":
            imgs = "".join(f"<image:image><image:loc>{SITE_URL}/images/{s}-{PH[s]['widths'][-1]}.jpg</image:loc></image:image>" for s in gallery_stems())
        urls += f"<url><loc>{SITE_URL}{p}</loc><lastmod>{TODAY}</lastmod>{imgs}</url>"
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">{urls}</urlset>')
    write("/.htaccess", "ErrorDocument 404 /404.html\nOptions -Indexes\n<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType image/avif \"access plus 1 year\"\nExpiresByType image/webp \"access plus 1 year\"\nExpiresByType image/jpeg \"access plus 1 year\"\nExpiresByType image/png \"access plus 1 year\"\nExpiresByType text/css \"access plus 1 month\"\nExpiresByType application/javascript \"access plus 1 month\"\n</IfModule>\n<IfModule mod_deflate.c>\nAddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml\n</IfModule>\n")
    print(f"Built {len(pages)+1} pages, {len(PH)} photos, logo={'yes' if LOGO else 'no'} into {DIST}")

if __name__ == "__main__":
    main()
