#!/usr/bin/env python3
"""
Builds the static pages for the Ogbontor Engineering Enterprise site.

Every page is plain, dependency-free HTML once generated — this script only
exists so the shared shell (head, header, footer) stays identical across pages.
Edit the data/partials here and re-run `python3 tools/build.py`, or just edit
the generated .html files directly if you prefer.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORG        = "Ogbontor Engineering Enterprise"
ORG_SHORT  = "Ogbontor"
RC         = "9862078"
REGISTER_ENDPOINT = "https://script.google.com/macros/s/AKfycbyH2rW40zmKwwqDDqF91gTuwTG6fb1hSAtO6N1WHHh8ukCKSzHLNXvC14F_ccUOmxnA/exec"
PORTFOLIO  = [
  ("Joint-Agent IDE", "jointagentide.com", "https://jointagentide.com",
   "An autonomous agent for embedded development — writes firmware, compiles, debugs and flashes real hardware from the browser."),
  ("CNG Protect", "cngprotect.com", "https://cngprotect.com",
   "Smart IoT-blockchain monitoring for compressed-natural-gas cylinders — pressure, integrity and custody, verifiable on chain."),
]
EMAIL      = "victorogbonna313@gmail.com"   # switch to info@ogbontor.com once that mailbox is live
PHONE      = "+234 903 6494 405"
PHONE_TEL  = "+2349036494405"
WHATSAPP   = "https://chat.whatsapp.com/CBLct4fEPPa8FAFz10cGH8"
MAPS_URL   = "https://www.google.com/maps/search/?api=1&query=Lion+Science+Park+Road%2C+University+of+Nigeria%2C+Nsukka%2C+Enugu+State%2C+Nigeria"
ADDRESS    = "1 Lion Science Park Road, University of Nigeria, Nsukka 410002, Enugu State, Nigeria"
SITE_URL   = "https://ogbontor.com"
TAGLINE    = "Empowering Africa's Hardware Tech Revolution"

# ---------------------------------------------------------------- icons ----
ICONS = {
 "spark":  '<path d="M12 3v3m0 12v3M5.6 5.6l2.1 2.1m8.6 8.6 2.1 2.1M3 12h3m12 0h3M5.6 18.4l2.1-2.1m8.6-8.6 2.1-2.1"/>',
 "arrow":  '<path d="M5 12h14m-6-6 6 6-6 6"/>',
 "chip":   '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 3v4m4-4v4m-4 10v4m4-4v4M3 10h4m-4 4h4m10-4h4m-4 4h4"/>',
 "cpu":    '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v3m6-3v3M9 19v3m6-3v3M2 9h3m-3 6h3m14-6h3m-3 6h3"/>',
 "bot":    '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 4v4M9 14h.01M15 14h.01M2 13h2m16 0h2"/><circle cx="12" cy="3" r="1.5"/>',
 "wifi":   '<path d="M5 12.5a11 11 0 0 1 14 0M8.5 16a6.5 6.5 0 0 1 7 0M12 20h.01"/>',
 "users":  '<path d="M16 20v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 20v-2a4 4 0 0 0-3-3.87M16 3.13A4 4 0 0 1 16 11"/>',
 "book":   '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
 "check":  '<path d="m5 13 4 4L19 7"/>',
 "wrench": '<path d="M14.7 6.3a4 4 0 0 0 5 5l-9.4 9.4a2.1 2.1 0 0 1-3-3z"/>',
 "zap":    '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
 "globe":  '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18z"/>',
 "mail":   '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
 "phone":  '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "pin":    '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "clock":  '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 "layers": '<path d="m12 2 9 5-9 5-9-5 9-5z"/><path d="m3 12 9 5 9-5M3 17l9 5 9-5"/>',
 "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2a2.1 2.1 0 0 0-3-3z"/><path d="M12 15 9 12a11 11 0 0 1 8-9 11 11 0 0 1-3 11z"/><path d="M9 12H5s.5-3 2-4 4 0 4 0"/><path d="M12 15v4s3-.5 4-2 0-4 0-4"/>',
 "graph":  '<path d="M3 3v18h18"/><path d="m7 15 4-5 3 3 5-7"/>',
 "flask":  '<path d="M9 2h6M10 2v6.5L4.6 18a2 2 0 0 0 1.7 3h11.4a2 2 0 0 0 1.7-3L14 8.5V2"/><path d="M7 16h10"/>',
 "hand":   '<path d="M11 11V5.5a1.5 1.5 0 0 1 3 0V11m0-1.5a1.5 1.5 0 0 1 3 0V13m0-2a1.5 1.5 0 0 1 3 0v5a6 6 0 0 1-6 6h-2a6 6 0 0 1-5.2-3L4 15.5a1.6 1.6 0 0 1 2.7-1.7L8 15.5V7a1.5 1.5 0 0 1 3 0z"/>',
 "info":   '<circle cx="12" cy="12" r="9"/><path d="M12 11v5m0-9h.01"/>',
 "menu":   '<path d="M3 6h18M3 12h18M3 18h18"/>',
 "x":      '<path d="M18 6 6 18M6 6l12 12"/>',
 "sun":    '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "moon":   '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
 "wa":     '<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.1-1.3A10 10 0 1 0 12 2z"/><path d="M8.5 7.8c.2-.4.4-.4.7-.4h.6c.2 0 .4 0 .6.5l.8 2c.1.3 0 .5-.1.7l-.4.5c-.2.2-.3.4-.1.7a7 7 0 0 0 3.2 2.8c.3.1.5.1.7-.1l.6-.7c.2-.2.4-.2.6-.1l1.9.9c.3.1.4.3.4.5a2 2 0 0 1-1.4 1.6c-.5.2-1.2.2-3.5-.8a9.5 9.5 0 0 1-4.6-4.6c-.8-1.7-.6-2.6-.4-3.1z"/>',
 "link":   '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7L11.8 5"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7L12.2 19"/>',
 "pcb":    '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v4a2 2 0 0 0 2 2h2a2 2 0 0 1 2 2v3M3 15h4a2 2 0 0 1 2 2v4"/><circle cx="15" cy="15" r="1.6"/><circle cx="9" cy="9" r="1.2"/>',
 "cad":    '<path d="m12 2 9 5v10l-9 5-9-5V7l9-5z"/><path d="m12 12 9-5m-9 5v10m0-10L3 7"/>',
 "palette":'<circle cx="12" cy="12" r="9"/><circle cx="8.5" cy="9.5" r="1.1" fill="currentColor"/><circle cx="14" cy="8" r="1.1" fill="currentColor"/><circle cx="16.5" cy="13" r="1.1" fill="currentColor"/><path d="M12 21a3 3 0 0 1 0-6 2 2 0 0 0 0-4"/>',
 "code":   '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-2-15-4 18"/>',
 "brain":  '<path d="M9.5 3A2.5 2.5 0 0 0 7 5.5 2.5 2.5 0 0 0 4.5 8a2.5 2.5 0 0 0 .6 1.6A2.5 2.5 0 0 0 4 12a2.5 2.5 0 0 0 1.4 2.2A2.5 2.5 0 0 0 5 16a2.5 2.5 0 0 0 2.5 2.5A2.5 2.5 0 0 0 10 21h2V3z"/><path d="M14.5 3A2.5 2.5 0 0 1 17 5.5 2.5 2.5 0 0 1 19.5 8a2.5 2.5 0 0 1-.6 1.6A2.5 2.5 0 0 1 20 12a2.5 2.5 0 0 1-1.4 2.2A2.5 2.5 0 0 1 19 16a2.5 2.5 0 0 1-2.5 2.5A2.5 2.5 0 0 1 14 21h-2"/>',
 "printer":'<path d="M7 8V3h10v5"/><rect x="3" y="8" width="18" height="8" rx="2"/><path d="M7 16h10v5H7z"/><circle cx="17.5" cy="11.5" r=".8" fill="currentColor"/>',
 "factory":'<path d="M3 21V10l5 3V10l5 3V10l5 3V7l3 2v12z"/><path d="M8 21v-4m5 4v-4m5 4v-4"/>',
 "plane":  '<path d="M2 12h3l2-3h3l-1.5 3H14l3-5h2.5L17 12l2.5 5H17l-3-5H8.5l1.5 3H7l-2-3H2z"/>',
 "motor":  '<circle cx="12" cy="12" r="4"/><path d="M12 2v3m0 14v3M2 12h3m14 0h3M5 5l2 2m10 10 2 2M19 5l-2 2M7 17l-2 2"/>',
 "chip2":  '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="10" y="10" width="4" height="4"/><path d="M10 2v4m4-4v4m-4 12v4m4-4v4M2 10h4m-4 4h4m12-4h4m-4 4h4"/>',
 "calendar":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4m8-4v4M3 10h18"/>',
 "clipboard":'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1"/><path d="M9 11h6M9 15h4"/>',
 "briefcase":'<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M2 13h20"/>',
 "award":  '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 8 5-3 5 3-1.5-8"/>',
 "atom":   '<circle cx="12" cy="12" r="1.6"/><ellipse cx="12" cy="12" rx="9.5" ry="4" /><ellipse cx="12" cy="12" rx="9.5" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="9.5" ry="4" transform="rotate(120 12 12)"/>',
 "external":'<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5"/>',
 "megaphone":'<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 6a9 9 0 0 1 0 12"/>',
 "handshake":'<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2l-3-3"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2L13 9H9.5L7 11.5"/><path d="M3 9.5 6.5 6H11l2 2"/><path d="M2 12.5 5 15m16-6-3-3"/>',
 "tools":  '<path d="M14.7 6.3a4 4 0 0 0 5 5l-9.4 9.4a2.1 2.1 0 0 1-3-3z"/><path d="m8 8-5-5 2-2 5 5"/>',
}
def ico(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


EVENTS = [
 ("award", "The conference",
  "A mega hardware technology conference opens the programme — talks, demos and speakers from across Nigeria and around the world.",
  "Opens the programme"),
 ("book",  "Three weeks of bootcamp",
  "Intensive, hands-on sessions across all eleven tracks at UNN Nsukka. Free, hardware supplied, no prior experience needed.",
  "Three weeks &middot; free"),
 ("zap",   "The hackathon",
  "Teams build against a brief to close the programme, with prizes to be revealed.",
  "Closes the programme"),
]


# The people, beyond the founder. Bios stay short on purpose.
TEAM = [
 ("Theophilus Edafe", "CAD Engineer", "theophilus-edafe.jpg",
  "Turns ideas into working prototypes. Helps startups and innovators develop, refine and 3D-print "
  "physical products — CAD, mechanical design, embedded systems and hands-on fabrication."),
 ("Bright Okonkwo", "Full-Stack Embedded Systems Engineer", "bright-okonkwo.jpg",
  "Works the whole stack of a connected device — firmware on the microcontroller, the protocols "
  "carrying its data, and the services that receive it. Comfortable from register level to cloud."),
 ("Elsie Iloene", "Full-Stack Software Developer", "elsie-iloene.jpg",
  "Builds the software our hardware needs to be useful — dashboards, APIs and interfaces that turn "
  "raw sensor output into something a person can act on."),
]

BOOTCAMP_MONTH = "November 2026"
BOOTCAMP_TRACKS = [
 ("bot",     "Robotics"),
 ("cpu",     "Embedded Systems"),
 ("wifi",    "Internet of Things"),
 ("pcb",     "PCB Design"),
 ("cad",     "CAD"),
 ("layers",  "IoT-Blockchain"),
 ("palette", "IoT UI/UX"),
 ("code",    "IoT Web Development"),
 ("brain",   "Edge AI"),
 ("printer", "3D Printing"),
 ("tools",   "Fabrication"),
]

NAV = [("index.html","Home"),("about.html","About"),("programs.html","Programs"),
       ("projects.html","Projects"),("community.html","Community"),
       ("register.html","Register"),("contact.html","Contact")]


def asset_v(path):
    """Short content hash for cache-busting, so a redeploy never serves stale CSS/JS."""
    import hashlib
    full = os.path.join(ROOT, path)
    try:
        with open(full, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()[:8]
    except OSError:
        return "0"

CSS_V = asset_v("assets/css/styles.css")
JS_V  = asset_v("assets/js/main.js")


def head(title, desc, page):
    nav = "\n".join(f'          <a href="{h}">{l}</a>' for h, l in NAV)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B57D0">
<link rel="canonical" href="{SITE_URL}/{page}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{ORG}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE_URL}/{page}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.png">
<meta property="og:image:secure_url" content="{SITE_URL}/assets/img/og-image.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ORG} — South-East Nigeria's largest student hardware tech community">
<meta property="og:locale" content="en_NG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_URL}/assets/img/og-image.png">
<meta name="twitter:image:alt" content="{ORG}">
<meta name="author" content="{ORG}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="geo.region" content="NG-EN">
<meta name="geo.placename" content="Nsukka, Enugu State, Nigeria">
<meta name="geo.position" content="6.8567;7.3958">
<meta name="ICBM" content="6.8567, 7.3958">
<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600&display=swap">
<meta name="register-endpoint" content="{REGISTER_ENDPOINT}">
<link rel="stylesheet" href="assets/css/styles.css?v={CSS_V}">
<noscript><style>.reveal{{opacity:1!important;transform:none!important}}</style></noscript>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": ["Organization", "EducationalOrganization"],
  "name": "{ORG}",
  "alternateName": "Ogbontor",
  "url": "{SITE_URL}/",
  "logo": "{SITE_URL}/assets/img/logo.png",
  "image": "{SITE_URL}/assets/img/og-image.png",
  "description": "The largest student hardware tech community in South-East Nigeria — training students in embedded systems, robotics, IoT and blockchain hardware.",
  "email": "{EMAIL}",
  "telephone": "{PHONE_TEL}",
  "slogan": "{TAGLINE}",
  "identifier": "RC {RC}",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "1 Lion Science Park Road, University of Nigeria",
    "addressLocality": "Nsukka",
    "postalCode": "410002",
    "addressRegion": "Enugu State",
    "addressCountry": "NG"
  }},
  "areaServed": "South-East Nigeria",
  "foundingLocation": "Nsukka, Enugu State, Nigeria",
  "knowsAbout": ["Embedded Systems", "Robotics", "Internet of Things", "PCB Design",
                 "Edge AI", "Blockchain Hardware", "3D Printing", "CAD", "Fabrication"],
  "sameAs": ["{WHATSAPP}"]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{ORG}",
  "url": "{SITE_URL}/",
  "inLanguage": "en-NG",
  "publisher": {{ "@type": "Organization", "name": "{ORG}" }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "EducationEvent",
  "name": "Africa's Hardware Revolution: From Spark to Ignition",
  "description": "A mega hardware technology conference at the University of Nigeria, Nsukka, followed by three weeks of intensive free bootcamp covering robotics, embedded systems, IoT, PCB design, CAD, IoT-blockchain, edge AI, 3D printing and fabrication, closing with a hackathon.",
  "startDate": "2026-11",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "isAccessibleForFree": true,
  "inLanguage": "en-NG",
  "url": "{SITE_URL}/register.html",
  "image": "{SITE_URL}/assets/img/og-image.png",
  "location": {{
    "@type": "Place",
    "name": "University of Nigeria, Nsukka",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "1 Lion Science Park Road, University of Nigeria",
      "addressLocality": "Nsukka",
      "postalCode": "410002",
      "addressRegion": "Enugu State",
      "addressCountry": "NG"
    }}
  }},
  "organizer": {{ "@type": "Organization", "name": "{ORG}", "url": "{SITE_URL}/" }},
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "NGN",
    "availability": "https://schema.org/InStock",
    "url": "{SITE_URL}/register.html",
    "validFrom": "2026-09-01"
  }},
  "audience": {{ "@type": "EducationalAudience", "educationalRole": "student" }}
}}
</script>

<script>
  // Set the theme before first paint so there is no flash of the wrong colours.
  // Blue-on-white is the brand default; only an explicit choice switches to dark.
  (function(){{try{{if(localStorage.getItem("ogbontor-theme")==="dark")
     document.documentElement.setAttribute("data-theme","dark");}}catch(e){{}}}})();
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="container nav">
    <a class="brand" href="index.html" aria-label="{ORG} — home">
      <img src="assets/img/logo.png" alt="" width="34" height="34">
      <span>
        <span class="brand-name">OGBONTOR</span><br>
        <span class="brand-sub">Engineering</span>
      </span>
    </a>

    <nav id="primary-nav" class="nav-links" aria-label="Primary">
{nav}
    </nav>

    <div class="nav-actions">
      <button class="icon-btn" data-theme-toggle type="button" aria-label="Switch colour theme">
        <span class="theme-icon-sun">{ico("sun")}</span>
        <span class="theme-icon-moon">{ico("moon")}</span>
      </button>
      <a class="btn btn--primary nav-cta" href="register.html">{ico("clipboard")} Register free</a>
      <button class="icon-btn nav-toggle" data-nav-toggle type="button"
              aria-label="Toggle navigation" aria-expanded="false" aria-controls="primary-nav">
        {ico("menu")}
      </button>
    </div>
  </div>
</header>

<main id="main">

<div class="alert-bar">
  <div class="container">
    <p>
      {ico("megaphone")}
      <span class="pill">November 2026</span>
      <strong>Free conference, 3-week bootcamp &amp; hackathon</strong>
      <span class="alert-tagline">&mdash; Africa's Hardware Revolution: From Spark to Ignition</span>
    </p>
    <a class="alert-cta" href="register.html">Register free {ico("arrow")}</a>
  </div>
</div>
'''

FOOTER = f'''</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="index.html">
          <img src="assets/img/logo.png" alt="" width="34" height="34">
          <span>
            <span class="brand-name">OGBONTOR</span><br>
            <span class="brand-sub">Engineering</span>
          </span>
        </a>
        <p>{TAGLINE}. We train students across South-East Nigeria to design, build and ship
           real hardware — then help them turn it into products.</p>
        <div class="socials">
          <a href="{WHATSAPP}" target="_blank" rel="noopener" aria-label="WhatsApp community">{ico("wa")}</a>
          <a href="mailto:{EMAIL}" aria-label="Email us">{ico("mail")}</a>
          <a href="tel:{PHONE_TEL}" aria-label="Call us">{ico("phone")}</a>
        </div>
      </div>

      <div class="footer-col">
        <h2>Explore</h2>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="programs.html">Programs</a></li>
          <li><a href="projects.html">Projects</a></li>
          <li><a href="community.html">Community</a></li>
          <li><a href="index.html#portfolio">Portfolio companies</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h2>Programs</h2>
        <ul>
          <li><a href="register.html">Register (free bootcamp)</a></li>
          <li><a href="programs.html#curriculum">Curriculum</a></li>
          <li><a href="programs.html#siwes">SIWES &amp; IT placements</a></li>
          <li><a href="programs.html#membership">Membership</a></li>
          <li><a href="community.html#events">Build nights</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h2>Reach us</h2>
        <ul class="footer-contact">
          <li>{ico("pin")}<a href="{MAPS_URL}" target="_blank" rel="noopener">{ADDRESS}</a></li>
          <li>{ico("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ico("phone")}<a href="tel:{PHONE_TEL}">{PHONE}</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> {ORG}. All rights reserved. &middot; RC {RC}</span>
      <span class="mono">Our tomorrow is indeed here.</span>
    </div>
  </div>
</footer>

<div class="lightbox" data-lightbox role="dialog" aria-modal="true" aria-label="Image viewer">
  <button class="lightbox-close" type="button" aria-label="Close image viewer">{ico("x")}</button>
  <div>
    <img alt="">
    <p class="lightbox-cap"></p>
  </div>
</div>

<script src="assets/js/main.js?v={JS_V}"></script>
</body>
</html>
'''

def write(page, title, desc, body):
    html = head(title, desc, page) + body + FOOTER
    path = os.path.join(ROOT, page)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  wrote {page}  ({len(html)//1024} KB)")


# ------------------------------------------------------------------ data ----
# Verified against the Behance project modules (numbering and status are theirs):
# items 1-10 are the "Real-Life Projects" list, 11-13 the "in development" list,
# and #6 is flagged "(in progress)" in the source. Images were matched to projects
# from the module order, then confirmed by eye at full size.
# A 5th element may carry extras: {"video", "link", "logo"}.
PROJECTS_BUILT = [
 ("CNG Protect", "A smart IoT-blockchain device that monitors compressed-natural-gas cylinders — pressure, integrity and custody — signed on the device and verifiable on chain. Now a company of its own.",
  "gallery/cng-protect-module.jpg", ["IoT", "Blockchain", "Safety"],
  {"link": "https://cngprotect.com", "logo": "companies/cng-protect.jpg", "logo_alt": "CNG Protect logo"}),
 ("Joint-Agent IDE", "An autonomous agent for embedded development — it writes firmware, compiles, debugs and flashes real hardware from one browser tab. Spun out of this lab into its own product.",
  "gallery/joint-agent-dashboard.jpg", ["Software", "Embedded", "AI Agent"],
  {"link": "https://jointagentide.com", "logo": "companies/joint-agent.png", "logo_alt": "Joint-Agent logo"}),
 ("Line Following Robot", "The classic controls exercise done properly — sensor array, tuned PID loop, and a chassis the team built in-house. Press play to watch it track the line.",
  "line-following-poster.jpg", ["Robotics", "Control", "PID"],
  {"video": "video/line-following-robot.mp4"}),
 ("Smart Solar Power Measurement System", "Measures and logs output across up to six solar panels at once, comparing passive fins, forced air and water cooling on a live rooftop deployment.",
  "gallery/solar-deployment-site.jpg", ["Energy", "Telemetry", "Sensors"]),
 ("Bluetooth Six-Wheel Terrain Climber", "A six-wheel rover driven over Bluetooth, built to keep traction and stay level on the broken ground around campus.",
  "gallery/terrain-climber-complete.jpg", ["Robotics", "Mechanical", "Control"]),
 ("Smart Walking Stick for the Blind", "Ultrasonic ranging with haptic and audible feedback, so a user feels an obstacle before they reach it. Field-tested on open ground.",
  "gallery/walking-stick-bench.jpg", ["Assistive Tech", "Sensors"]),
 ("Ultraviolet Radiation Detection System", "A handheld UV index meter reading out to an LCD in a sealed enclosure — built for people who work long hours in open sun.",
  "gallery/uv-detector-enclosure.jpg", ["Instrumentation", "Health"]),
 ("Gas Leak & Temperature Monitor", "Continuous temperature and combustible-gas monitoring with a keypad front end, raising a local alarm the moment a threshold is crossed.",
  "gallery/gas-monitor-enclosure.jpg", ["Safety", "IoT", "Alarms"]),
 ("Pulse & Heart Rate Monitor", "Optical pulse and SpO2 measurement with Telegram integration, so a reading can reach a relative or clinician without extra hardware.",
  "gallery/pulse-monitor-reading.jpg", ["Medical", "Connectivity"]),
 ("Obstacle Avoidance Robot", "Autonomous navigation around unmapped obstacles using ultrasonic sweeps and a reactive control strategy.",
  "gallery/obstacle-robot-complete.jpg", ["Robotics", "Autonomy"]),
]

PROJECTS_WIP = [
 ("Joint-Agent Board & IoT Kit", "The hardware side of Joint-Agent — Nigeria's first IoT-blockchain board and development kit, signing sensor readings on the board itself. In build.",
  "gallery/joint-agent-kit.jpg", ["IoT", "Blockchain", "Hardware"],
  {"logo": "companies/joint-agent.png", "logo_alt": "Joint-Agent logo"}),
 ("Robotic Arm — 6 Degrees of Freedom", "A six-axis arm with inverse kinematics and a teach-pendant workflow, intended as the teaching rig for our robotics tier.",
  "gallery/robotic-arm.jpg", ["Robotics", "Kinematics"]),
 ("Autonomous Self-Driving Vehicle", "A self-driving platform with an advanced computer-vision pipeline for lane keeping, obstacle classification and route planning.",
  "placeholders/autonomous-vehicle.svg", ["Computer Vision", "Autonomy", "Edge AI"]),
 ("Smart Electrocardiogram System", "A low-cost ECG front end with digital filtering, aimed at clinics that cannot justify imported equipment.",
  "placeholders/ecg-system.svg", ["Medical", "Signal Processing"]),
]

CURRICULUM = [
 ("I", "Foundational Knowledge", "Core principles — the vocabulary and habits everything else is built on.", [
   "Introduction to Embedded Systems",
   "Fundamentals of Electronics and Circuit Design",
   "Programming Essentials for Embedded Systems",
   "Introduction to Robotics"]),
 ("II", "Intermediate Skills", "Practical application — where members start shipping working hardware.", [
   "Microcontroller Programming and Applications",
   "Sensors and Actuators",
   "Communication Protocols",
   "Real-Time Operating Systems (RTOS)",
   "Internet of Things (IoT) Systems and Applications"]),
 ("III", "Advanced Topics", "Specialised knowledge — the work that separates a hobbyist from an engineer.", [
   "Advanced Robotics and AI Integration",
   "Edge Computing and AI for Embedded Systems",
   "FPGA Programming and Applications",
   "Power Management in Embedded Systems",
   "CPU Design and Architecture",
   "GPU Design and Parallel Processing",
   "Autonomous Systems and Control",
   "Advanced Sensor Fusion Techniques"]),
 ("IV", "CAD and Design Integration", "Turning a breadboard into something you can hold, mount and manufacture.", [
   "CAD for Embedded Systems and Robotics",
   "Design for Embedded Systems and Robotics Projects"]),
 ("V", "Capstone Projects", "Real builds, real deadlines, real users.", [
   "Real-world embedded systems and robotics projects with CAD design",
   "Industry internships and collaborations",
   "Entrepreneurship and startup development",
   "Ethical considerations in embedded systems and robotics"]),
]

def project_card(p, status):
    name, desc, img, tags = p[0], p[1], p[2], p[3]
    extra = p[4] if len(p) > 4 and isinstance(p[4], dict) else {}
    video, link, logo = extra.get("video"), extra.get("link"), extra.get("logo")

    tag_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    if video:
        tag_html = '<span class="tag tag--live">Video</span>' + tag_html
    badge = ('<span class="tag tag--live badge-float">Completed</span>' if status == "built"
             else '<span class="tag tag--wip badge-float">Pending</span>')

    logo_html = ""
    if logo:
        logo_html = (f'<img class="project-logo" src="assets/img/{logo}" '
                     f'alt="{extra.get("logo_alt", name + " logo")}" loading="lazy">')

    if video:
        # preload="none" -> nothing is fetched until the visitor presses play.
        media = f'''          <div class="project-media project-media--video">
            {badge}
            <img class="media-blur" src="assets/img/{img}" alt="" aria-hidden="true" loading="lazy">
            <video preload="none" playsinline controls
                   poster="assets/img/{img}"
                   aria-label="{name} in action">
              <source src="assets/{video}" type="video/mp4">
            </video>
          </div>'''
    else:
        media = f'''          <div class="project-media">
            {badge}
            {logo_html}
            <img src="assets/img/{img}" alt="{name}" loading="lazy" width="800" height="500">
          </div>'''

    if link:
        # the whole card is a link out to the product's own site
        title = (f'<h3><a class="project-out" href="{link}" target="_blank" rel="noopener">'
                 f'{name} {ico("external")}</a></h3>')
        cls = "project project--linked reveal"
    else:
        title = f"<h3>{name}</h3>"
        cls = "project reveal"

    return f'''        <article class="{cls}">
{media}
          <div class="project-body">
            {title}
            <p>{desc}</p>
            <div class="tag-row">{tag_html}</div>
          </div>
        </article>'''


def stat(num, label, suffix="", prefix=""):
    return f'''        <div class="stat">
          <div class="stat-num grad-text" data-count="{num}" data-suffix="{suffix}" data-prefix="{prefix}">0</div>
          <div class="stat-label">{label}</div>
        </div>'''


# ------------------------------------------------------------------ home ----
def build_home():
    _ext = ico("external")
    banner_tracks = "\n".join(f'          <span>{ico(k)} {label}</span>' for k, label in BOOTCAMP_TRACKS)
    marquee_group = ('      <div class="marquee-group">\n'
                     + "\n".join(f'        <span class="marquee-item">{ico(k)} {label}</span>'
                                 for k, label in BOOTCAMP_TRACKS)
                     + '\n      </div>')
    companies = "\n".join(f'''        <article class="company reveal" data-delay="{i*0.08:.2f}">
          <img class="company-logo" src="assets/img/companies/{slug}" alt="{name} logo" loading="lazy">
          <h3>{name}</h3>
          <p>{blurb}</p>
          <a class="company-link" href="{url}" target="_blank" rel="noopener">{_ext} {domain}</a>
        </article>''' for i, ((name, domain, url, blurb), slug) in enumerate(
            zip(PORTFOLIO, ["joint-agent.png", "cng-protect.jpg"])))
    featured = "\n".join(project_card(p, "built") for p in PROJECTS_BUILT[:6])
    stats = "\n".join([
        stat(14, "Projects in the portfolio"),
        stat(19, "Curriculum modules"),
        stat(5,  "Skill tiers, foundation to capstone"),
        stat(1,  "Hardware lab at UNN Nsukka"),
    ])
    pillars = [
      ("book",  "We train",     "Nineteen modules, Ohm's law to FPGA design. Taught with a board in front of you, not slides."),
      ("wrench","We build",     "Real prototypes from week one. Fourteen systems on the bench so far."),
      ("rocket","We incubate",  "Capstones that prove themselves become products. We help with IP, pitches and pilot users."),
      ("globe", "We manufacture","The long game: hardware designed and assembled in Enugu, not imported and repaired."),
    ]
    pillar_html = "\n".join(f'''        <article class="card reveal" data-delay="{i*0.07:.2f}">
          <div class="card-ico">{ico(k)}</div>
          <h3>{t}</h3>
          <p>{d}</p>
        </article>''' for i,(k,t,d) in enumerate(pillars))

    tiers = "\n".join(f'''          <li>
            <span class="mod-n">{rn}</span>
            <div><strong>{name}</strong><br><span class="muted">{len(mods)} {"modules" if len(mods)!=1 else "module"} &middot; {blurb}</span></div>
          </li>''' for rn, name, blurb, mods in CURRICULUM)

    partners = "\n".join(f'        <div><img src="assets/img/partners/partner-{i}.svg" alt="Partner {i} logo — placeholder" loading="lazy"></div>'
                         for i in range(1, 7))

    body = f'''  <section class="hero">
    <div class="backdrop"><div class="grid-lines"></div></div>
    <div class="container">
      <div class="hero-grid">
        <div>
          <span class="eyebrow">{ico("pin")} University of Nigeria, Nsukka &middot; Enugu State</span>
          <h1>South-East Nigeria's <span class="grad-text">largest student hardware tech</span>
            <span class="underline-accent">community</span>.</h1>
          <p class="lede">
            Students here stop reading about hardware and start building it. Embedded systems,
            robotics, IoT and blockchain devices — soldered, coded and deployed from our lab in Nsukka.
          </p>
          <div class="hero-cta">
            <a class="btn btn--primary btn--lg" href="{WHATSAPP}" target="_blank" rel="noopener">
              {ico("wa")} Join the community
            </a>
            <a class="btn btn--ghost btn--lg" href="projects.html">
              See what we've built {ico("arrow")}
            </a>
          </div>
          <p class="hero-note">
            <span>{ico("check")} Free to join &middot; open to every student</span>
          </p>
        </div>

        <div class="carousel reveal" data-carousel aria-roledescription="carousel" aria-label="Ogbontor highlights">
          <div class="carousel-window">

            <figure class="slide is-active" data-slide role="group" aria-roledescription="slide" aria-label="1 of 5">
              <img class="slide-photo" src="assets/img/gallery/cohort-group-photo.jpg"
                   alt="The Ogbontor bootcamp cohort outside the lab at UNN Nsukka"
                   width="900" height="500" fetchpriority="high">
              <figcaption>Previous bootcamp &middot; UNN Nsukka</figcaption>
            </figure>

            <div class="slide slide--cta" data-slide role="group" aria-roledescription="slide" aria-label="2 of 5">
              <span class="kicker">Registration open &middot; free</span>
              <h2>Register now</h2>
              <p>Africa's Hardware Revolution &mdash; From Spark to Ignition. Open to every student, no fee.</p>
              <div class="slide-inset">
                <img src="assets/img/gallery/bootcamp-cohort-wide.jpg" alt="Members at work during a previous bootcamp" loading="lazy">
              </div>
              <a class="btn btn--lg" href="register.html">{ico("clipboard")} Register free</a>
            </div>

            <figure class="slide" data-slide role="group" aria-roledescription="slide" aria-label="3 of 5">
              <img class="slide-photo" src="assets/img/gallery/bootcamp-lecture.jpg"
                   alt="A teaching session during a previous Ogbontor bootcamp" loading="lazy" width="900" height="500">
              <figcaption>Previous bootcamp &middot; teaching session</figcaption>
            </figure>

            <div class="slide slide--cta" data-slide role="group" aria-roledescription="slide" aria-label="4 of 5">
              <span class="kicker">Partner with us</span>
              <h2>Become a sponsor</h2>
              <p>We are building the biggest hardware campus bootcamp in South-East Nigeria &mdash; over 800
                 attendees, speakers from Nigeria and around the world.</p>
              <a class="btn btn--lg" href="index.html#sponsors">{ico("handshake")} Sponsor the bootcamp</a>
            </div>

            <figure class="slide" data-slide role="group" aria-roledescription="slide" aria-label="5 of 5">
              <img class="slide-photo" src="assets/img/gallery/bootcamp-cohort-wide.jpg"
                   alt="Members working at benches during a previous Ogbontor bootcamp" loading="lazy" width="900" height="500">
              <figcaption>Previous bootcamp &middot; open lab</figcaption>
            </figure>

          </div>

          <button class="carousel-nav carousel-nav--prev" type="button" data-carousel-prev aria-label="Previous slide">{ico("arrow")}</button>
          <button class="carousel-nav carousel-nav--next" type="button" data-carousel-next aria-label="Next slide">{ico("arrow")}</button>
          <div class="carousel-dots" data-carousel-dots role="tablist" aria-label="Choose slide"></div>
        </div>
      </div>
    </div>
  </section>

  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">
{marquee_group}
{marquee_group}
    </div>
  </div>

  <section class="section" id="equipment">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("tools")} <span class="sec-no">01</span> Modern equipment for hardware tech</span>
        <h2>Ideas do not stay on paper here</h2>
        <p class="lede">A community is only as good as the machines in the room. Design a part on Monday,
          hold it on Tuesday — instead of waiting weeks on an import.</p>
      </div>

      <div class="video-stage reveal">
        <video class="video-bg" src="assets/video/3d-printer.mp4" muted loop autoplay playsinline aria-hidden="true" tabindex="-1"></video>
        <video class="video-main" src="assets/video/3d-printer.mp4"
               poster="assets/img/3d-printer-poster.svg"
               muted loop autoplay playsinline controls preload="metadata"
               aria-label="Our 3D printer running in the lab"></video>
      </div>
      <p class="video-cap">Our 3D printer running in the lab at UNN Nsukka.</p>

      <div class="grid grid-3 mt-4">
        <article class="card reveal">
          <div class="card-ico">{ico("layers")}</div>
          <h3>3D printing &amp; fabrication</h3>
          <p>Enclosures, brackets, jigs, custom parts. Free for members, available to everyone else.</p>
        </article>
        <article class="card reveal" data-delay="0.08">
          <div class="card-ico">{ico("wrench")}</div>
          <h3>A bench that is actually equipped</h3>
          <p>Soldering stations, measurement gear, dev boards, a component library. Your project stalls on
             your thinking, not your budget.</p>
        </article>
        <article class="card reveal" data-delay="0.16">
          <div class="card-ico">{ico("rocket")}</div>
          <h3>Prototype to product</h3>
          <p>Print, test, revise, print again. Fast iteration is the difference between a school project and
             a product.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--tight" id="bootcamp">
    <div class="container">
      <div class="bootcamp bracketed reveal">
       <div class="bootcamp-grid">
        <div>
        <span class="eyebrow">{ico("zap")} <span class="sec-no">02</span> Free bootcamp &middot; open to everyone at UNN</span>
        <h2>Africa's Hardware Revolution</h2>
        <p class="theme-line">From Spark to Ignition</p>
        <p><strong>Free. Open to every UNN student.</strong> No fee, no experience, no particular course.
           Bring curiosity; we supply the bench, the boards and the people.</p>
        <p class="programme-line" style="margin-top:1rem"><strong>A Mega Hardware Conference this
           November</strong>, followed by <strong>3 weeks of intensive practical hardware bootcamp</strong>
           and a <strong>hackathon</strong>.</p>
        <p style="margin-top:.8rem;font-size:.9rem;opacity:.85">Other South-East campuses next — one per state.</p>
        <div class="bootcamp-facts">
          <span>{ico("calendar")} November 2026</span>
          <span>{ico("check")} Completely free</span>
          <span>{ico("users")} Students &amp; individuals welcome</span>
          <span>{ico("pin")} University of Nigeria, Nsukka</span>
          <span>{ico("tools")} Hardware supplied</span>
        </div>
        <div class="bootcamp-facts" style="margin-top:.7rem">
{banner_tracks}
        </div>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="register.html">{ico("clipboard")} Register free</a>
          <a class="btn btn--ghost btn--lg" href="programs.html#bootcamp">What you'll learn {ico("arrow")}</a>
        </div>
        </div>
        <div class="bootcamp-art">
          <img src="assets/img/africa-circuit.png"
               alt="Africa drawn as a circuit board, with the lab at UNN Nsukka marked" width="330" height="440" loading="lazy">
        </div>
       </div>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <div class="stats reveal">
{stats}
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("target")} <span class="sec-no">03</span> What we do</span>
        <h2>A community, a school, and a workshop — in one place</h2>
        <p class="lede">Africa imports the technology it depends on. The capacity to build it is already
          here — it has just never been trained or equipped. That is the gap we close.</p>
      </div>
      <div class="grid grid-4">
{pillar_html}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow">{ico("chip")} <span class="sec-no">04</span> Selected work</span>
        <h2>Hardware our members have actually shipped</h2>
        <p class="lede">Not renders. Boards populated, enclosures printed, firmware flashed, systems run
          outside the lab.</p>
      </div>
      <div class="grid grid-3">
{featured}
      </div>
      <div class="center mt-4">
        <a class="btn btn--ghost btn--lg" href="projects.html">View all 14 projects {ico("arrow")}</a>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="split">
        <div>
          <span class="eyebrow">{ico("book")} <span class="sec-no">05</span> The curriculum</span>
          <h2 class="mt-2">Nineteen modules, five tiers, one straight line</h2>
          <p class="lede mt-2">Most people stall because nobody laid the path out in order. Ours runs from
            your first resistor to CPU architecture — ending in a capstone that has to work in front of real
            users.</p>
          <ul class="modules mt-3" style="grid-template-columns:1fr; padding:0; background:none;">
{tiers}
          </ul>
          <a class="btn btn--primary mt-3" href="programs.html#curriculum">Explore the full curriculum {ico("arrow")}</a>
        </div>
        <figure class="reveal">
          <img src="assets/img/gallery/bootcamp-lecture.jpg" alt="A session in progress during an Ogbontor bootcamp, with members following along on laptops" loading="lazy" width="800" height="600">
        </figure>
      </div>
    </div>
  </section>

  <section class="section" id="siwes-teaser">
    <div class="container">
      <div class="siwes-panel bracketed reveal">
        <div class="siwes-grid">
          <div>
            <span class="eyebrow">{ico("briefcase")} <span class="sec-no">06</span> SIWES &amp; IT placements</span>
            <h2 class="mt-2">Do your industrial training somewhere you actually build</h2>
            <p class="lede mt-2">A bench, a project team and a supervisor who can actually assess the
              engineering you did — not a logbook you fill in at the end of the month.</p>
            <ul class="siwes-points">
              <li>{ico("check")}<span>Logbooks signed and ITF documentation handled properly.</span></li>
              <li>{ico("check")}<span>You join a real project team with a deliverable and a deadline.</span></li>
              <li>{ico("check")}<span>The same curriculum our members take.</span></li>
            </ul>
            <a class="btn btn--primary mt-3" href="programs.html#siwes">
              {ico("briefcase")} More about SIWES &amp; IT placements {ico("arrow")}
            </a>
          </div>

          <div>
            <p class="eyebrow" style="margin-bottom:.9rem">{ico("atom")} R&amp;D you can join</p>
            <div class="rnd-chips">
              <span>{ico("motor")} Electric motor manufacturing</span>
              <span>{ico("plane")} Manned aircraft prototyping</span>
              <span>{ico("chip2")} Microchip technology</span>
              <span class="chip-note">{ico("award")} First student-led hardware lab in South-East Nigeria to prototype in these areas</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="split split--flip">
        <div>
          <span class="eyebrow">{ico("users")} <span class="sec-no">07</span> The community</span>
          <h2 class="mt-2">You will not be building alone</h2>
          <p class="lede mt-2">The hardest part of hardware is the hour where nothing works and you have no
            idea why. A community is what gets you through it.</p>
          <ul class="check-list">
            <li>{ico("check")}<span><strong>Weekly build nights</strong> — open lab, real benches, people to ask.</span></li>
            <li>{ico("check")}<span><strong>Cohort bootcamps</strong> — structured, intensive, and free to members.</span></li>
            <li>{ico("check")}<span><strong>Mentorship</strong> — paired with someone two steps ahead of you, not twenty.</span></li>
            <li>{ico("check")}<span><strong>A component library</strong> — borrow the sensor instead of buying it.</span></li>
            <li>{ico("check")}<span><strong>Demo days</strong> — show the thing you built to people who understand it.</span></li>
          </ul>
          <a class="btn btn--ghost mt-3" href="community.html">How the community works {ico("arrow")}</a>
        </div>
        <figure class="reveal">
          <img src="assets/img/gallery/bootcamp-lab.jpg" alt="Members working at benches during an open lab session" loading="lazy" width="800" height="600">
        </figure>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("rocket")} <span class="sec-no">08</span> Where this is going</span>
        <h2>Made in Enugu</h2>
        <p class="lede">Not a better robotics club. Indigenous capability — electronics, vehicles and smart
          systems <em>designed</em> here, for African roads, climate and culture.</p>
      </div>
      <div class="grid grid-3">
        <figure class="project reveal" data-zoom>
          <div class="project-media"><img src="assets/img/gallery/made-in-enugu-factory.jpg" alt="Concept: an electronics assembly line operating in Enugu" loading="lazy" width="800" height="500"></div>
          <div class="project-body"><h3>Consumer electronics</h3><p>Assembly lines staffed by engineers we trained.</p></div>
        </figure>
        <figure class="project reveal" data-delay="0.08" data-zoom>
          <div class="project-media"><img src="assets/img/gallery/made-in-enugu-automotive.jpg" alt="Concept: vehicle drivetrain assembly in Enugu" loading="lazy" width="800" height="500"></div>
          <div class="project-body"><h3>Vehicles &amp; mobility</h3><p>Drivetrains and controls for the roads we actually drive on.</p></div>
        </figure>
        <figure class="project reveal" data-delay="0.16" data-zoom>
          <div class="project-media"><img src="assets/img/gallery/made-in-enugu-aircraft.jpg" alt="Concept: aircraft maintenance and assembly in Enugu" loading="lazy" width="800" height="500"></div>
          <div class="project-body"><h3>Aerospace &amp; heavy systems</h3><p>The far end of the roadmap — and why the curriculum goes so deep.</p></div>
        </figure>
      </div>
      <p class="center muted mt-3" style="font-size:.82rem">Illustrative concepts — these show the direction of the roadmap, not facilities currently in operation.</p>
    </div>
  </section>

  <section class="section" id="portfolio">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("rocket")} <span class="sec-no">09</span> Portfolio companies</span>
        <h2>What comes out the other end</h2>
        <p class="lede">Capstones become products. Products become companies. These two came out of this lab.</p>
      </div>
      <div class="grid grid-2">
{companies}
      </div>
    </div>
  </section>

  <section class="section section--alt" id="sponsors">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("link")} <span class="sec-no">10</span> Partners &amp; sponsors</span>
        <h2>Become a sponsor</h2>
        <p class="lede">It opens with <strong>the biggest hardware technology conference in South-East
          Nigeria</strong> — 800+ attendees, speakers from across Nigeria and around the world — then three
          weeks of bootcamp and a hackathon. Help us build it.</p>
      </div>

      <div class="grid grid-4">
        <article class="card reveal">
          <div class="card-ico">{ico("users")}</div>
          <h3>800+ attendees</h3>
          <p>Students, makers and early-career engineers from across the South-East, in one room.</p>
        </article>
        <article class="card reveal" data-delay="0.07">
          <div class="card-ico">{ico("globe")}</div>
          <h3>Speakers worldwide</h3>
          <p>Practitioners from Nigeria and worldwide, on hardware they actually shipped.</p>
        </article>
        <article class="card reveal" data-delay="0.14">
          <div class="card-ico">{ico("layers")}</div>
          <h3>Where your support goes</h3>
          <p>Venue, components, printing, speaker travel — and free seats for students who could not otherwise come.</p>
        </article>
        <article class="card reveal" data-delay="0.21">
          <div class="card-ico">{ico("target")}</div>
          <h3>What you get</h3>
          <p>Branding across the event and this site, a stand on the floor, first access to the people you want to hire.</p>
        </article>
      </div>

      <div class="partners mt-4 reveal">
{partners}
      </div>

      <div class="sponsor-cta mt-3 reveal">
        <h3>This space is for your logo</h3>
        <p>Equipment, component budgets, speaker travel, internships or funding. Tell us what you have in
          mind and we will send the deck.</p>
        <div class="hero-cta" style="justify-content:center">
          <a class="btn btn--primary" href="mailto:{EMAIL}?subject=Sponsorship%20%E2%80%94%20Ogbontor%20hardware%20bootcamp">{ico("mail")} Become a sponsor</a>
          <a class="btn btn--ghost" href="contact.html">Talk to us first {ico("arrow")}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="cta-band bracketed reveal">
        <span class="eyebrow">{ico("zap")} Open intake</span>
        <h2 class="mt-2">Our tomorrow is indeed here.</h2>
        <p>Bring curiosity. We supply the bench, the boards and the people.</p>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("wa")} Join on WhatsApp</a>
          <a class="btn btn--ghost btn--lg" href="contact.html">Talk to us first {ico("arrow")}</a>
        </div>
      </div>
    </div>
  </section>

'''
    write("index.html",
          f"{ORG} — South-East Nigeria's Largest Student Hardware Tech Community",
          "Ogbontor Engineering Enterprise is the largest student hardware tech community in South-East Nigeria — training students in embedded systems, robotics, IoT and blockchain hardware at UNN Nsukka.",
          body)


def page_hero(eyebrow_icon, eyebrow, title, lede, crumb):
    return f'''  <section class="page-hero">
    <div class="backdrop"><div class="grid-lines"></div></div>
    <div class="container">
      <p class="crumbs"><a href="index.html">Home</a> / {crumb}</p>
      <span class="eyebrow mt-2">{ico(eyebrow_icon)} {eyebrow}</span>
      <h1>{title}</h1>
      <p class="lede">{lede}</p>
    </div>
  </section>

'''

# ----------------------------------------------------------------- about ----
def build_about():
    team_html = '''        <article class="founder reveal">
          <img src="assets/img/team/founder.jpg" alt="Victor Ogbonna, founder of Ogbontor Engineering Enterprise"
               width="360" height="360" loading="lazy">
          <div>
            <p class="founder-role">Founder</p>
            <h3>Victor Ogbonna</h3>
            <p class="founder-bio">I started Ogbontor because the capacity to build hardware in Nigeria is
              already here. What was missing was a bench, a curriculum deep enough to matter, and a room full
              of people working the same problem at the same time.</p>
            <p class="founder-bio" style="margin-top:.8rem">Behind me is a team of hardware professionals —
              and more of them join as the lab grows.</p>
            <div class="founder-links">
              <a class="btn btn--ghost" href="mailto:{EMAIL}">{ico_mail} Email me</a>
              <a class="btn btn--ghost" href="{WHATSAPP}" target="_blank" rel="noopener">{ico_wa} Community</a>
            </div>
          </div>
        </article>'''

    crew_html = "\n".join(f'''        <article class="person reveal" data-delay="{i*0.07:.2f}">
          <img src="assets/img/team/{photo}" alt="{name}, {role} at {ORG}" loading="lazy" width="400" height="400">
          <h3>{name}</h3>
          <p>{role}</p>
          <p class="person-bio">{bio}</p>
        </article>''' for i, (name, role, photo, bio) in enumerate(TEAM))

    team_html = (team_html
                 .replace("{ico_mail}", ico("mail"))
                 .replace("{ico_wa}", ico("wa"))
                 .replace("{EMAIL}", EMAIL)
                 .replace("{WHATSAPP}", WHATSAPP))
    values = [
      ("hand",  "Hands on the hardware", "Nobody learns embedded systems from a slide deck. Every module ends with something on a bench that either works or doesn't."),
      ("users", "Nobody builds alone",   "Seniors teach juniors. The person who solved your bug last month is in the room. That loop is the whole community."),
      ("globe", "Built for here",        "Designed for Nigerian power, Nigerian roads, Nigerian budgets and Nigerian users — not adapted from a product made for somewhere else."),
      ("shield","Rigour, not theatre",   "Datasheets get read. Designs get reviewed. Claims get measured. An impressive demo that cannot be reproduced is not an achievement."),
    ]
    values_html = "\n".join(f'''        <article class="card reveal" data-delay="{i*0.07:.2f}">
          <div class="card-ico">{ico(k)}</div>
          <h3>{t}</h3><p>{d}</p>
        </article>''' for i,(k,t,d) in enumerate(values))

    body = page_hero("users", "About us", f"We are building the engineers who will build Nigeria's hardware.",
        f"{ORG} is a hardware technology enterprise and student community based at the University of Nigeria, Nsukka. We train, we prototype, and we turn what works into products.", "About")

    body += f'''  <section class="section">
    <div class="container">
      <div class="split">
        <div>
          <span class="eyebrow">{ico("info")} The problem</span>
          <h2 class="mt-2">Africa consumes technology it cannot repair</h2>
          <div class="prose mt-2">
            <p>Nigeria, and indeed much of the African continent, faces a significant setback in
               technological development. Almost everything electronic in daily use here was designed
               somewhere else, for someone else, and arrives as a sealed box.</p>
            <p>When it fails, it is replaced rather than fixed. When it doesn't suit local conditions —
               unstable mains, dust, heat, intermittent connectivity — it is tolerated rather than redesigned.
               And the engineering capacity that would let us do otherwise never gets built, because there is
               nowhere to learn it properly and nothing to practise on.</p>
            <p><strong>That is a training problem before it is an industrial one.</strong> It is the one we
               decided to work on.</p>
          </div>
        </div>
        <figure class="reveal">
          <img src="assets/img/gallery/solar-build-process.jpg" alt="The solar measurement system under construction on a breadboard" loading="lazy" width="800" height="600">
        </figure>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="split split--flip">
        <div>
          <span class="eyebrow">{ico("target")} Our position</span>
          <h2 class="mt-2">The capacity is already here</h2>
          <div class="prose mt-2">
            <p>{ORG_SHORT} is dedicated to fostering a new era of Nigerian technological innovation. We
               believe Nigeria possesses the inherent capacity to address its own technological challenges,
               rather than depending on solutions designed for other contexts.</p>
            <p>What has been missing is not talent. It is a bench, a curriculum that goes deep enough to
               matter, and a room full of people working on the same problem at the same time. We assembled
               those three things in Nsukka, and the result is now the largest student hardware tech community
               in South-East Nigeria.</p>
          </div>
          <ul class="check-list">
            <li>{ico("check")}<span>Founded and operating from the University of Nigeria, Nsukka</span></li>
            <li>{ico("check")}<span>Registered in Nigeria &mdash; RC {RC}</span></li>
            <li>{ico("check")}<span>Fourteen hardware systems designed, built or under active development</span></li>
            <li>{ico("check")}<span>Membership open to students across South-East Nigeria, free of charge</span></li>
          </ul>
        </div>
        <figure class="reveal">
          <img src="assets/img/gallery/bootcamp-cohort-wide.jpg" alt="A bootcamp session with members working at computers" loading="lazy" width="800" height="600">
        </figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("flask")} How we work</span>
        <h2>Four things we refuse to compromise on</h2>
      </div>
      <div class="grid grid-4">
{values_html}
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow">{ico("rocket")} Long-term objectives</span>
        <h2>What we are actually aiming at</h2>
        <p class="lede">These are deliberately larger than a student club should attempt. Stating them
          plainly is how we keep the curriculum honest about how deep it has to go.</p>
      </div>
      <div class="grid grid-3">
        <article class="project reveal">
          <div class="project-media">
            <img src="assets/img/gallery/vision-electronics.jpg" alt="Concept: Nigerian engineers working with circuit boards and consumer devices" loading="lazy" width="800" height="500">
          </div>
          <div class="project-body">
            <h3>Indigenous consumer electronics</h3>
            <p>Smartphones, televisions and household electronics designed and assembled in Nigeria — which is
               why the curriculum runs all the way to CPU and GPU architecture.</p>
          </div>
        </article>
        <article class="project reveal" data-delay="0.08">
          <div class="project-media">
            <img src="assets/img/gallery/made-in-enugu-aircraft.jpg" alt="Concept: aircraft assembly and maintenance in Enugu" loading="lazy" width="800" height="500">
          </div>
          <div class="project-body">
            <h3>Vehicles, aircraft and submersibles</h3>
            <p>Transport engineered for African terrain, climate and infrastructure rather than imported and
               then apologised for.</p>
          </div>
        </article>
        <article class="project reveal" data-delay="0.16">
          <div class="project-media">
            <img src="assets/img/gallery/vision-smart-systems.jpg" alt="Concept: a team developing smart systems and robotics" loading="lazy" width="800" height="500">
          </div>
          <div class="project-body">
            <h3>Smart systems that fit the culture</h3>
            <p>Connected systems built around how Nigerian homes, markets, clinics and farms actually operate.</p>
          </div>
        </article>
      </div>
      <p class="center muted mt-3" style="font-size:.82rem">Illustrative concepts — these show the direction of the roadmap, not facilities currently in operation.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("users")} Who runs it</span>
        <h2>The people behind it</h2>
      </div>
{team_html}

      <div class="grid grid-3 mt-4">
{crew_html}
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="cta-band bracketed reveal">
        <span class="eyebrow">{ico("wa")} Come and see</span>
        <h2 class="mt-2">The fastest way to understand us is to show up</h2>
        <p>Join the community channel, come to a build night, and watch what happens on the bench.</p>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("wa")} Join on WhatsApp</a>
          <a class="btn btn--ghost btn--lg" href="projects.html">See the work {ico("arrow")}</a>
        </div>
      </div>
    </div>
  </section>

'''
    write("about.html", f"About — {ORG}",
          f"Who we are: a hardware technology enterprise and the largest student hardware tech community in South-East Nigeria, based at the University of Nigeria, Nsukka.",
          body)


# -------------------------------------------------------------- programs ----
def build_programs():
    n = 0
    tiers_html = []
    for rn, name, blurb, mods in CURRICULUM:
        items = []
        for m in mods:
            if rn == "V":
                items.append(f'          <li><span class="mod-n">{ico("check")}</span><span>{m}</span></li>')
            else:
                n += 1
                items.append(f'          <li><span class="mod-n">{n:02d}</span><span>{m}</span></li>')
        tiers_html.append(f'''      <section class="tier reveal">
        <header class="tier-head">
          <span class="tier-rn">{rn}</span>
          <div><h3>{name}</h3><p>{blurb}</p></div>
        </header>
        <ul class="modules">
{chr(10).join(items)}
        </ul>
      </section>''')
    tiers_html = "\n".join(tiers_html)

    tracks = [
      ("bot",   "Robotics &amp; Control",   "Kinematics, PID, motor drivers, chassis design and the arm rig."),
      ("wifi",  "IoT &amp; Connectivity",   "MQTT, LoRa, GSM, power budgeting and devices that survive a field deployment."),
      ("chip",  "PCB &amp; Hardware Design","Schematic capture, layout, DFM, bring-up and debugging a board that arrived dead."),
      ("cpu",   "Embedded AI &amp; Vision", "Running inference on constrained silicon: quantisation, accelerators, camera pipelines."),
      ("layers","Blockchain Hardware",      "Signing at the edge, key custody on device, and getting sensor data on-chain credibly."),
      ("tools", "CAD &amp; Fabrication",    "Enclosures, tolerances, 3D printing and designing something you can actually manufacture."),
    ]
    tracks_html = "\n".join(f'''        <article class="card reveal" data-delay="{i*0.06:.2f}">
          <div class="card-ico">{ico(k)}</div><h3>{t}</h3><p>{d}</p>
        </article>''' for i,(k,t,d) in enumerate(tracks))

    tiers_member = [
      ("Associate", "Free", "Anyone enrolled at any institution in South-East Nigeria.", [
        "Community channel and study groups", "Open build nights", "Foundational tier (Modules 01–04)",
        "Demo day attendance"], False),
      ("Builder", "Free · by cohort", "Members who have cleared the foundational tier.", [
        "Everything in Associate", "Full bootcamp seat", "Component library borrowing privileges",
        "Assigned mentor", "Intermediate &amp; advanced tiers", "Project team placement"], True),
      ("Resident", "By application", "Members carrying a capstone toward a real product.", [
        "Everything in Builder", "Dedicated bench space", "Budget for parts &amp; fabrication",
        "Incubation support: IP, pitch, pilot users", "Industry placement &amp; introductions"], False),
    ]
    mem_html = ""
    for name, price, who, feats, featured in tiers_member:
        lis = "".join(f'<li>{ico("check")}<span>{f}</span></li>' for f in feats)
        style = ' style="border-color:var(--accent-line); box-shadow:var(--glow)"' if featured else ''
        badge = '<span class="tag tag--wip" style="position:absolute;top:1.25rem;right:1.35rem">Most common</span>' if featured else ''
        mem_html += f'''        <article class="card reveal"{style}>
          {badge}
          <h3>{name}</h3>
          <p class="mono" style="color:var(--accent);font-size:.86rem;margin:.35rem 0 .1rem">{price}</p>
          <p>{who}</p>
          <ul class="check-list">{lis}</ul>
        </article>
'''

    body = page_hero("book", "Programs", "From your first resistor to a capstone that ships.",
        "A 19-module curriculum across five tiers, run as hands-on cohorts. Every tier ends with hardware you built yourself — not an exam.", "Programs")

    body += f'''  <section class="section section--tight">
    <div class="container">
      <div class="bootcamp bracketed reveal">
       <div class="bootcamp-grid">
        <div>
        <span class="eyebrow">{ico("zap")} Free bootcamp &middot; open to everyone at UNN</span>
        <h2>Africa's Hardware Revolution</h2>
        <p class="theme-line">From Spark to Ignition</p>
        <p>Our next bootcamp is <strong>free and open to every student at the University of Nigeria,
           Nsukka</strong> — whatever you study, and whether or not you have ever touched a circuit. Come to
           learn, come to build something real, and come to be inspired.</p>
        <p class="programme-line" style="margin-top:1rem"><strong>A Mega Hardware Conference this
           November</strong>, followed by <strong>3 weeks of intensive practical hardware bootcamp</strong>
           and a <strong>hackathon</strong>.</p>
        <div class="bootcamp-facts">
          <span>{ico("calendar")} November 2026</span>
          <span>{ico("check")} Completely free</span>
          <span>{ico("users")} Open to all UNN students</span>
          <span>{ico("award")} Hackathon prizes</span>
        </div>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="register.html">{ico("clipboard")} Register free</a>
        </div>
        </div>
        <div class="bootcamp-art">
          <img src="assets/img/africa-circuit.png"
               alt="Africa drawn as a circuit board, with the lab at UNN Nsukka marked" width="330" height="440" loading="lazy">
        </div>
       </div>
      </div>
    </div>
  </section>

  <section class="section" id="bootcamp">
    <div class="container">
      <div class="split">
        <div>
          <span class="eyebrow">{ico("zap")} Cohort bootcamps</span>
          <h2 class="mt-2">Intensive, in person, and free</h2>
          <div class="prose mt-2">
            <p>Bootcamps are how most members enter. A cohort moves through the foundational tier together
               over a fixed number of weeks, in the lab, with boards on the bench from day one.</p>
            <p>You are not watching someone else build. You get a kit, a partner, a bug, and somebody
               experienced within arm's reach when you are stuck.</p>
          </div>
          <ul class="check-list">
            <li>{ico("check")}<span><strong>Cohort-based</strong> — you start and finish with the same people.</span></li>
            <li>{ico("check")}<span><strong>Hardware supplied</strong> — boards, sensors and tools from the community library.</span></li>
            <li>{ico("check")}<span><strong>Project-assessed</strong> — you pass by building, not by writing.</span></li>
            <li>{ico("check")}<span><strong>Free for members</strong> — the cost barrier is the thing we are removing.</span></li>
          </ul>
          <a class="btn btn--primary mt-3" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("wa")} Ask about the next cohort</a>
        </div>
        <figure class="reveal">
          <img src="assets/img/gallery/walking-stick-training.jpg" alt="A member being trained on building a smart walking stick" loading="lazy" width="800" height="600">
        </figure>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="curriculum">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow">{ico("layers")} The curriculum</span>
        <h2>Nineteen modules, in the order they actually make sense</h2>
        <p class="lede">Tiers I through IV are taught modules. Tier V is the capstone — a real build, on a
          deadline, in front of real users.</p>
      </div>
{tiers_html}
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("target")} Specialist tracks</span>
        <h2>Where members go after the core</h2>
        <p class="lede">Once the foundational and intermediate tiers are behind you, you pick a direction and
          go deep with a project team working on it.</p>
      </div>
      <div class="grid grid-3">
{tracks_html}
      </div>
    </div>
  </section>

  <section class="section section--highlight" id="siwes">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow">{ico("briefcase")} SIWES &amp; IT placements</span>
        <h2>Do your industrial training somewhere you actually build</h2>
        <p class="lede">We host <strong>SIWES and IT students</strong> from universities, polytechnics and
          colleges of education. A placement here is a bench, a project team and a supervisor — not a
          logbook you fill in at the end of the month.</p>
      </div>

      <div class="grid grid-3">
        <article class="card reveal">
          <div class="card-ico">{ico("clipboard")}</div>
          <h3>Properly supervised</h3>
          <p>Logbooks signed, ITF documentation handled, and a supervisor who can actually assess the
             engineering you did.</p>
        </article>
        <article class="card reveal" data-delay="0.08">
          <div class="card-ico">{ico("wrench")}</div>
          <h3>On a real project</h3>
          <p>You join a project team with a deliverable and a deadline, and leave with something you can
             demonstrate at your defence.</p>
        </article>
        <article class="card reveal" data-delay="0.16">
          <div class="card-ico">{ico("book")}</div>
          <h3>The full curriculum</h3>
          <p>Placement students sit the same tiers our members do — embedded systems, robotics, IoT, PCB
             design, CAD, edge AI, 3D printing and fabrication.</p>
        </article>
      </div>

      <div class="sec-head mt-4">
        <span class="eyebrow">{ico("award")} First of its kind</span>
        <h2>The deep end</h2>
        <p class="lede">We are the <strong>first student-led hardware lab in South-East Nigeria to
          prototype in these areas</strong>. Alongside the technology programmes, placement students can
          work on the R&amp;D lines we are building toward — long-horizon programmes where you would be
          joining early, on foundational work.</p>
      </div>

      <div class="grid grid-3">
        <article class="rnd reveal">
          <div class="rnd-top">
            <div class="card-ico">{ico("motor")}</div>
            <h3>Electric motor manufacturing</h3>
          </div>
          <div class="rnd-body">
            <p>Winding, stator and rotor design, controller electronics and test rigs — the part of the
               electrification supply chain Nigeria currently imports wholesale.</p>
          </div>
        </article>
        <article class="rnd reveal" data-delay="0.08">
          <div class="rnd-top">
            <div class="card-ico">{ico("plane")}</div>
            <h3>Manned aircraft prototyping</h3>
          </div>
          <div class="rnd-body">
            <p>Airframe prototyping, avionics and control systems, working toward manned aircraft
               manufacturing — the longest horizon on our roadmap, and the reason the curriculum goes as
               deep as it does.</p>
          </div>
        </article>
        <article class="rnd reveal" data-delay="0.16">
          <div class="rnd-top">
            <div class="card-ico">{ico("chip2")}</div>
            <h3>Microchip technology</h3>
          </div>
          <div class="rnd-body">
            <p>From FPGA and CPU architecture through to silicon design — the foundation under every other
               programme we run.</p>
          </div>
        </article>
      </div>

      <div class="callout mt-4">{ico("info")}<span><strong>Applying for a placement?</strong> Send your
        institution, department, level and placement dates to
        <a href="mailto:{EMAIL}" style="color:var(--accent)">{EMAIL}</a>, or register through the bootcamp
        form and tell us in the last question.</span></div>
    </div>
  </section>

  <section class="section section--alt" id="membership">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("users")} Membership</span>
        <h2>Three levels, and the first one costs nothing</h2>
        <p class="lede">Membership is about access and commitment, not fees. You move up by building, and
          every level above Associate is earned rather than bought.</p>
      </div>
      <div class="grid grid-3">
{mem_html}      </div>
      <div class="callout mt-4">{ico("check")}<span><strong>Free for now.</strong> Every level above is free
        of charge — membership, bootcamp seats and lab access. If that ever changes we will say so here first,
        and in the community channel, well before it takes effect.</span></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="cta-band bracketed reveal">
        <span class="eyebrow">{ico("book")} Intake is open</span>
        <h2 class="mt-2">Start at Module 01</h2>
        <p>You do not need prior electronics experience, a laptop of your own, or a particular course of
          study. You need to turn up.</p>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("wa")} Join the community</a>
          <a class="btn btn--ghost btn--lg" href="contact.html">Ask a question {ico("arrow")}</a>
        </div>
      </div>
    </div>
  </section>

'''
    write("programs.html", f"Programs &amp; Curriculum — {ORG}",
          "A 19-module hardware engineering curriculum across five tiers — embedded systems, robotics, IoT, FPGA, edge AI and CAD — taught as hands-on cohort bootcamps in Nsukka.",
          body)


# -------------------------------------------------------------- projects ----
GALLERY = [
 ("cohort-group-photo.jpg",        "The bootcamp cohort outside the lab at UNN Nsukka"),
 ("bootcamp-lab.jpg",              "Open lab session — every bench occupied"),
 ("bootcamp-cohort-wide.jpg",      "Bootcamp week in progress at UNN Nsukka"),
 ("bootcamp-lecture.jpg",          "Teaching session in progress"),
 ("terrain-climber-build.jpg",     "Wiring the six-wheel terrain climber"),
 ("walking-stick-field-1.jpg",     "Field-testing the smart walking stick on open ground"),
 ("walking-stick-field-2.jpg",     "The walking stick's sensor head and controller in use"),
 ("walking-stick-training.jpg",    "A member being trained on building the smart walking stick"),
 ("walking-stick-internals.jpg",   "Inside the walking stick enclosure during integration"),
 ("solar-build-process.jpg",       "Building the solar measurement system — breadboard stage"),
 ("solar-finished-product.jpg",    "The finished solar measurement unit"),
 ("gas-monitor-development.jpg",   "Developing the gas and temperature monitor firmware"),
 ("joint-agent-dashboard.jpg",     "The Joint-Agent IoT-blockchain dashboard receiving live data"),
 ("uv-detector-demo.jpg",          "Demonstrating the UV radiation detector"),
 ("robotic-arm-build.jpg",         "Assembling the six-axis robotic arm"),
 ("obstacle-robot-build.jpg",      "The obstacle avoidance robot under assembly"),
]

def build_projects():
    built = "\n".join(project_card(p, "built") for p in PROJECTS_BUILT)
    wip   = "\n".join(project_card(p, "wip")   for p in PROJECTS_WIP)
    gal = "\n".join(f'''        <figure data-zoom>
          <img src="assets/img/gallery/{f}" alt="{c}" loading="lazy">
          <figcaption>{c}</figcaption>
        </figure>''' for f, c in GALLERY)

    body = page_hero("chip", "Projects", "Fourteen systems, built by students on a bench in Nsukka.",
        "Every project here was designed, assembled, programmed and debugged by members. Some are finished and deployed; the rest are still pending on the bench.", "Projects")

    body += f'''  <section class="section">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow">{ico("check")} Built &amp; working</span>
        <h2>Completed systems</h2>
        <p class="lede">These made it past the prototype stage — populated boards, printed
          enclosures, flashed firmware, and testing outside the lab.</p>
      </div>
      <div class="grid grid-3">
{built}
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow">{ico("wrench")} On the bench</span>
        <h2>Pending</h2>
        <p class="lede">Still in the workshop — designed and under active development, but not yet
          finished. If you want to join a project team, these are the ones taking members.</p>
      </div>
      <div class="grid grid-3">
{wip}
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow">{ico("users")} From the lab</span>
        <h2>The work, as it actually looks</h2>
        <p class="lede">Select any image to view it full size.</p>
      </div>
      <div class="gallery">
{gal}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="cta-band bracketed reveal">
        <span class="eyebrow">{ico("rocket")} Project teams</span>
        <h2 class="mt-2">Put your name on the next one</h2>
        <p>Members join project teams from the intermediate tier onward. The pending builds are taking
          people right now.</p>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("wa")} Join a project team</a>
          <a class="btn btn--ghost btn--lg" href="programs.html">See the curriculum {ico("arrow")}</a>
        </div>
      </div>
    </div>
  </section>

'''
    write("projects.html", f"Projects — {ORG}",
          "Fourteen hardware systems from our student members: CNG Protect, the Joint-Agent IoT-blockchain board, solar power measurement, terrain-climbing robots, assistive tech and medical instrumentation.",
          body)


# ------------------------------------------------------------- community ----
FAQS = [
 ("Do I need any electronics experience to join?",
  "No. The foundational tier assumes nothing — it starts at what current and voltage are and why a resistor matters. Most members arrive having never soldered anything."),
 ("Do I have to be a student at UNN?",
  f"No &mdash; and you do not have to be in Nigeria at all. The lab is at the University of Nigeria, Nsukka, and that is where the benches, build nights and bootcamps are, but <strong>membership is open to anyone, anywhere in the world</strong>. If you can get to Nsukka you can be a full member with lab access; if you cannot, you can still take part in the community channel, the study groups and remote project teams. "
  f"<br><br>The <strong>free bootcamp is specific to UNN Nsukka</strong> for this first run. We are coming to other selected universities across South-East Nigeria next &mdash; at least one in each state."),
 ("Does it cost anything?",
  "Associate and Builder membership are free, and bootcamp seats are free to members. The cost barrier is precisely the thing we exist to remove. Residents working on funded capstones are handled case by case."),
 ("What course do I need to be studying?",
  "Any. We have members from electrical and electronic engineering, computer science, mechanical engineering, physics, and several from outside the sciences entirely. Hardware needs people who can design enclosures, write documentation and talk to users as much as it needs firmware engineers."),
 ("Do I need my own laptop or components?",
  "It helps, but it is not a requirement. The community component library lends boards, sensors and tools to members, and lab machines are available during open hours."),
 ("How much time does it take?",
  "A build night is one evening a week. A bootcamp cohort is considerably more intense over a fixed run of weeks. Project teams set their own pace around the deadline they have committed to."),
 ("Can my company partner or sponsor?",
  f"Yes — equipment, component budgets, internship places and project sponsorship are all useful to us. Write to {EMAIL} and say what you have in mind."),
 ("What happens after the capstone?",
  "The strongest capstones go into incubation: we help with intellectual property, a pitch, pilot users and company formation. Both of our portfolio companies &mdash; <strong>Joint-Agent</strong> and <strong>CNG-Protect</strong> &mdash; started exactly this way."),
]

def build_community():
    what = [
      ("tools",  "Weekly build nights",  "An open lab evening every week. Bring what you are working on, or pick up a community build and get started. Benches, tools and people who have already made your mistake."),
      ("users",  "Study groups",         "Small groups working through the same module together. Far more effective than grinding a datasheet alone at 2am."),
      ("hand",   "Mentorship pairing",   "Every Builder is paired with someone two steps ahead of them — near enough to remember being stuck where you are."),
      ("layers", "Component library",    "Borrow the sensor, the analyser, the dev board. Not being able to afford a part should not be what stops a project."),
      ("graph",  "Demo days",            "Every cohort ends by showing what it built to an audience that understands it and asks hard questions."),
      ("zap",    "Hackathons",           "Fixed-length competitive builds against a brief. Fast, loud, and the quickest way to find out what you actually know."),
      ("target", "Project teams",        "Multi-month teams on the systems listed under Projects, with defined roles and a real deadline."),
      ("rocket", "Internships & placement","Introductions to partner companies, and support for members taking a capstone toward a product."),
    ]
    what_html = "\n".join(f'''        <article class="card reveal" data-delay="{i%4*0.06:.2f}">
          <div class="card-ico">{ico(k)}</div><h3>{t}</h3><p>{d}</p>
        </article>''' for i,(k,t,d) in enumerate(what))

    steps = [
      ("Join the channel", f"Open the WhatsApp community. Introduce yourself — what you study and what you want to build. That is the whole application."),
      ("Come to a build night", "Turn up at the lab on the next open evening. Nothing is expected of you the first time except showing up."),
      ("Take the foundational tier", "Join the next cohort, or work through Modules 01–04 with a study group if a cohort is not running."),
      ("Pick a direction", "Choose a specialist track, join a project team, and start building something with your name on it."),
    ]
    steps_html = "\n".join(f'''        <article class="card reveal" data-delay="{i*0.07:.2f}">
          <span class="card-num">0{i+1}</span>
          <div class="card-ico">{ico("arrow")}</div>
          <h3>{t}</h3><p>{d}</p>
        </article>''' for i,(t,d) in enumerate(steps))

    faq_html = "\n".join(f'''        <details{" open" if i==0 else ""}>
          <summary>{q}</summary>
          <div class="faq-body">{a}</div>
        </details>''' for i,(q,a) in enumerate(FAQS))

    body = page_hero("users", "Community", "The largest student hardware tech community in South-East Nigeria.",
        "Build nights, study groups, mentors, a component library and project teams — the infrastructure that turns an interest in hardware into the ability to build it.", "Community")

    body += f'''  <section class="section">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow">{ico("target")} What membership gets you</span>
        <h2>Eight things that only work with other people</h2>
        <p class="lede">You can learn to code alone. Hardware is harder to do that way — you need a bench,
          an oscilloscope, a spare part, and someone who has seen this failure before.</p>
      </div>
      <div class="grid grid-4">
{what_html}
      </div>
    </div>
  </section>

  <section class="section section--alt" id="events">
    <div class="container">
      <div class="split">
        <div>
          <span class="eyebrow">{ico("clock")} What the week looks like</span>
          <h2 class="mt-2">Come for one evening and see</h2>
          <div class="prose mt-2">
            <p>The rhythm is deliberately simple: one open lab evening a week that anyone can attend, study
               groups arranged around whichever modules are running, and project teams meeting on their own
               schedule.</p>
            <p>During a bootcamp the pace changes — cohorts meet far more often for the length of the run.</p>
          </div>
          <div class="callout mt-3">{ico("wa")}<span><strong>Dates and venue are announced in the
            community WhatsApp group.</strong> Build-night times, cohort start dates and any change of venue
            all go out there first &mdash; <a href="{WHATSAPP}" target="_blank" rel="noopener"
            style="color:var(--accent);font-weight:600">join the group</a> to get them.</span></div>
        </div>
        <figure class="reveal">
          <img src="assets/img/gallery/robotic-arm-build.jpg" alt="A member assembling the six-axis robotic arm at the bench" loading="lazy" width="800" height="600">
        </figure>
      </div>
    </div>
  </section>

  <section class="section" id="mentorship">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("rocket")} Getting started</span>
        <h2>Four steps, and the first one takes a minute</h2>
      </div>
      <div class="grid grid-4">
{steps_html}
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="split split--flip">
        <div>
          <span class="eyebrow">{ico("shield")} How we behave</span>
          <h2 class="mt-2">Code of conduct</h2>
          <div class="prose mt-2">
            <p>A community only works as a place to be a beginner if beginners are safe in it. The rules are
               short and we enforce them.</p>
          </div>
          <ul class="check-list">
            <li>{ico("check")}<span><strong>No condescension.</strong> Everyone was a beginner recently. Answer the question that was asked.</span></li>
            <li>{ico("check")}<span><strong>Credit honestly.</strong> Name who did the work, cite the reference, disclose what was borrowed.</span></li>
            <li>{ico("check")}<span><strong>Share what you learn.</strong> If you solved it, write it down where the next person will find it.</span></li>
            <li>{ico("check")}<span><strong>Respect the equipment.</strong> Shared tools and borrowed parts come back, on time and working.</span></li>
            <li>{ico("check")}<span><strong>Zero tolerance for harassment.</strong> On any grounds, in the lab or the channel.</span></li>
          </ul>
        </div>
        <figure class="reveal">
          <img src="assets/img/gallery/bootcamp-lab.jpg" alt="Members working together during a lab session" loading="lazy" width="800" height="600">
        </figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("info")} Questions</span>
        <h2>Things people ask before joining</h2>
      </div>
      <div class="faq reveal">
{faq_html}
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="cta-band bracketed reveal">
        <span class="eyebrow">{ico("wa")} Open intake</span>
        <h2 class="mt-2">Introduce yourself in the channel</h2>
        <p>That is the entire joining process. Scan the code or follow the link, say what you study and what
          you would like to build.</p>
        <div style="display:flex;justify-content:center;margin:1.75rem 0 .5rem">
          <img src="assets/img/whatsapp-qr.png" alt="QR code for the Ogbontor WhatsApp community" width="180" height="180"
               style="border-radius:var(--r);border:1px solid var(--line)">
        </div>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("wa")} Join on WhatsApp</a>
        </div>
      </div>
    </div>
  </section>

'''
    write("community.html", f"Community — {ORG}",
          "Build nights, study groups, mentorship, a component library and project teams at the largest student hardware tech community in South-East Nigeria. Free to join.",
          body)


# --------------------------------------------------------------- contact ----
def build_contact():
    body = page_hero("mail", "Contact", "Talk to us.",
        "Whether you want to join, partner with us, sponsor a cohort or commission a build — this is how to reach the team.", "Contact")

    body += f'''  <section class="section">
    <div class="container">
      <div class="split">
        <div>
          <span class="eyebrow">{ico("mail")} Send a message</span>
          <h2 class="mt-2">Tell us what you need</h2>
          <p class="lede mt-2">Fill this in and your email app will open with the message ready to send.
            Prefer to skip the form? Write to <a href="mailto:{EMAIL}" style="color:var(--accent)">{EMAIL}</a> directly.</p>

          <form class="mt-3" data-mailto="{EMAIL}" data-subject="Website enquiry — {ORG}" novalidate>
            <div class="field">
              <label for="c-name">Your name <span class="req">*</span></label>
              <input class="input" id="c-name" name="name" type="text" required autocomplete="name" placeholder="Chidi Okeke">
            </div>
            <div class="field">
              <label for="c-email">Email address <span class="req">*</span></label>
              <input class="input" id="c-email" name="email" type="email" required autocomplete="email" placeholder="you@example.com">
            </div>
            <div class="field">
              <label for="c-topic">What is this about? <span class="req">*</span></label>
              <select class="select input" id="c-topic" name="topic" required>
                <option value="">Choose one…</option>
                <option>Joining the community</option>
                <option>Bootcamp / next cohort</option>
                <option>Partnership or sponsorship</option>
                <option>Commissioning a build</option>
                <option>Press or speaking</option>
                <option>Something else</option>
              </select>
            </div>
            <div class="field">
              <label for="c-msg">Message <span class="req">*</span></label>
              <textarea class="textarea" id="c-msg" name="message" required
                placeholder="What are you working on, or what would you like to build?"></textarea>
            </div>
            <button class="btn btn--primary btn--block btn--lg" type="submit">{ico("mail")} Send message</button>
            <p class="form-status" role="status" aria-live="polite"></p>
            <p class="form-note">This form opens your own email client — nothing is sent to a server, and we
              store nothing. To collect submissions directly instead, connect the form to a service such as
              Formspree or Netlify Forms.</p>
          </form>
        </div>

        <div>
          <div class="card" style="height:auto">
            <div class="card-ico">{ico("pin")}</div>
            <h3>Find the lab</h3>
            <p>{ADDRESS}</p>
            <a class="btn btn--ghost mt-3" target="_blank" rel="noopener"
               href="https://www.google.com/maps/search/?api=1&amp;query=University+of+Nigeria+Nsukka+Lion+Science+Park">
               {ico("globe")} Open in Maps</a>
          </div>

          <div class="card mt-2" style="height:auto">
            <div class="card-ico">{ico("wa")}</div>
            <h3>Fastest route — WhatsApp</h3>
            <p>The community channel is where nearly everything happens. For joining, cohort dates or a quick
               question, this will get you an answer sooner than email.</p>
            <a class="btn btn--primary mt-3" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("wa")} Open the community</a>
            <p class="mt-2" style="font-size:.85rem;color:var(--text-muted)">
              Direct: <a href="https://wa.me/{PHONE_TEL.lstrip("+")}" target="_blank" rel="noopener" style="color:var(--accent)">{PHONE}</a>
            </p>
          </div>

          <div class="card mt-2" style="height:auto">
            <div class="card-ico">{ico("info")}</div>
            <h3>Company details</h3>
            <ul class="check-list" style="margin-top:.75rem">
              <li>{ico("check")}<span><strong>Registered name:</strong> {ORG}</span></li>
              <li>{ico("check")}<span><strong>RC number:</strong> {RC}</span></li>
              <li>{ico("check")}<span><strong>Email:</strong> <a href="mailto:{EMAIL}" style="color:var(--accent)">{EMAIL}</a></span></li>
              <li>{ico("check")}<span><strong>Phone:</strong> <a href="tel:{PHONE_TEL}" style="color:var(--accent)">{PHONE}</a></span></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("link")} Work with us</span>
        <h2>Three ways organisations get involved</h2>
      </div>
      <div class="grid grid-3">
        <article class="card reveal">
          <div class="card-ico">{ico("layers")}</div>
          <h3>Sponsor a cohort</h3>
          <p>Cover components, tools and bench space for an intake of students. The most direct way to put
             trained hardware engineers into the Nigerian workforce.</p>
        </article>
        <article class="card reveal" data-delay="0.08">
          <div class="card-ico">{ico("wrench")}</div>
          <h3>Commission a build</h3>
          <p>Instrumentation, monitoring systems, IoT deployments and prototypes — designed and built here,
             for conditions here.</p>
        </article>
        <article class="card reveal" data-delay="0.16">
          <div class="card-ico">{ico("users")}</div>
          <h3>Offer placements</h3>
          <p>Internships and graduate roles for members who have already shipped working hardware and can
             show you the board.</p>
        </article>
      </div>
    </div>
  </section>

'''
    write("contact.html", f"Contact — {ORG}",
          f"Reach Ogbontor Engineering Enterprise: {EMAIL}, {PHONE}, or the WhatsApp community. Lab at the University of Nigeria, Nsukka, Enugu State.",
          body)


# ------------------------------------------------------------ registration ----
SKILL_LEVELS = ["Complete beginner — never built anything",
                "Some exposure — a class or a tutorial or two",
                "Hobbyist — I have built a few things myself",
                "Intermediate — I can take a project end to end",
                "Advanced — I work on hardware seriously"]

def build_register():
    events_html = "\n".join(f'''        <article class="card reveal" data-delay="{i*0.08:.2f}">
          <div class="card-ico">{ico(k)}</div>
          <h3>{title}</h3>
          <p>{body}</p>
          <p class="mono mt-2" style="font-size:.76rem;color:var(--accent)">{when}</p>
        </article>''' for i, (k, title, body, when) in enumerate(EVENTS))
    tracks = "\n".join(f'''          <div class="track">
            <span class="t-ico">{ico(k)}</span><span>{label}</span>
          </div>''' for k, label in BOOTCAMP_TRACKS)

    checks = "\n".join(f'''            <label><input type="checkbox" name="tracks" value="{label}"><span>{label}</span></label>'''
                       for _, label in BOOTCAMP_TRACKS)
    levels = "\n".join(f'''                <option>{l}</option>''' for l in SKILL_LEVELS)

    body = f'''  <section class="page-hero">
    <div class="backdrop"><div class="grid-lines"></div></div>
    <div class="container">
      <p class="crumbs"><a href="index.html">Home</a> / Register</p>

      <div class="reg-hero mt-3">
        <div>
          <span class="free-badge">{ico("calendar")} November 2026 &middot; free of charge</span>
          <h1 class="mt-2">Africa's Hardware Revolution</h1>
          <p class="theme-line" style="font-family:var(--font-display);font-weight:600;font-size:clamp(1rem,2.2vw,1.35rem);color:var(--accent);margin-top:.5rem">From Spark to Ignition</p>
          <p class="programme-line"><strong>A Mega Hardware Conference this November</strong>, followed by
            <strong>3 weeks of intensive practical hardware bootcamp</strong> and a <strong>hackathon</strong>.</p>
          <p class="lede mt-2">At the University of Nigeria, Nsukka — open to students and to anyone else who
            wants to build. Whatever you study, and whether or not you have ever touched a circuit.</p>
          <div class="callout mt-3">{ico("pin")}<span><strong>This bootcamp runs at UNN Nsukka.</strong>
            We are coming to other selected universities across South-East Nigeria next &mdash; at least one
            in each state. Register anyway and we will tell you when we reach yours.</span></div>
          <div class="hero-cta">
            <a class="btn btn--primary btn--lg" href="#register-form">{ico("clipboard")} Register now</a>
            <a class="btn btn--ghost btn--lg" href="#covers">What it covers {ico("arrow")}</a>
          </div>
        </div>
        <figure>
          <img src="assets/img/gallery/cohort-group-photo.jpg"
               alt="Attendees of a previous Ogbontor bootcamp at UNN Nsukka" width="800" height="600" fetchpriority="high">
          <figcaption>Our previous bootcamp &middot; UNN Nsukka</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="events">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("calendar")} Three things, one programme</span>
        <h2>It is more than a bootcamp</h2>
        <p class="lede">A mega hardware conference, three weeks of intensive bootcamp, then a hackathon.
          One registration covers whichever of them you want.</p>
      </div>
      <div class="grid grid-3">
{events_html}
      </div>
    </div>
  </section>

  <section class="section" id="covers">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("layers")} What the bootcamp covers</span>
        <h2>Eleven tracks, one bootcamp, no fee</h2>
        <p class="lede">You do not need to pick one before you arrive. The programme runs across all of it,
          and you go deeper on whatever grips you.</p>
      </div>
      <div class="tracks">
{tracks}
      </div>
    </div>
  </section>

  <section class="section section--alt" id="register-form">
    <div class="container" style="max-width:860px">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("clipboard")} Registration</span>
        <h2>Tell us where you are starting from</h2>
        <p class="lede">The last three questions matter most. We read every one of them and shape the
          sessions around what people actually say — we would rather meet you at your need than teach at you.</p>
      </div>

      <form class="reg-form" id="registration" data-register
            data-endpoint="{REGISTER_ENDPOINT}" data-fallback-email="{EMAIL}" novalidate>

        <fieldset class="fieldset">
          <legend>Who you are</legend>
          <div class="field-row field-row--2">
            <div class="field">
              <label for="r-name">Full name <span class="req">*</span></label>
              <input class="input" id="r-name" name="Full name" type="text" required autocomplete="name" placeholder="Chidi Okeke">
            </div>
            <div class="field">
              <label for="r-email">Email address <span class="req">*</span></label>
              <input class="input" id="r-email" name="Email" type="email" required autocomplete="email" placeholder="you@example.com">
            </div>
          </div>
          <div class="field-row field-row--2">
            <div class="field">
              <label for="r-phone">Phone / WhatsApp <span class="req">*</span></label>
              <input class="input" id="r-phone" name="Phone" type="tel" required autocomplete="tel" placeholder="080 0000 0000">
            </div>
            <div class="field">
              <label for="r-status">You are <span class="req">*</span></label>
              <select class="select input" id="r-status" name="Status" required>
                <option value="">Choose one…</option>
                <option>Student at UNN Nsukka</option>
                <option>Student at another institution</option>
                <option>Recent graduate</option>
                <option>Not a student</option>
              </select>
            </div>
          </div>
          <div class="field-row field-row--2">
            <div class="field">
              <label for="r-inst">Institution</label>
              <input class="input" id="r-inst" name="Institution" type="text" placeholder="University of Nigeria, Nsukka">
            </div>
            <div class="field">
              <label for="r-course">Course / department</label>
              <input class="input" id="r-course" name="Course" type="text" placeholder="Electrical Engineering">
            </div>
          </div>
        </fieldset>

        <fieldset class="fieldset">
          <legend>What are you registering for?</legend>
          <div class="field">
            <label>Tick everything you want to attend <span class="req">*</span></label>
            <div class="check-grid mt-1" data-require-one="events">
              <label><input type="checkbox" name="events" value="Conference" checked><span>Conference (opens it)</span></label>
              <label><input type="checkbox" name="events" value="Bootcamp" checked><span>Bootcamp (three weeks)</span></label>
              <label><input type="checkbox" name="events" value="Hackathon" checked><span>Hackathon (closes it)</span></label>
            </div>
          </div>
        </fieldset>

        <fieldset class="fieldset">
          <legend>What interests you</legend>
          <div class="field">
            <label>Which tracks do you want most? <span class="muted" style="font-weight:400">(tick any)</span></label>
            <div class="check-grid mt-1">
{checks}
            </div>
          </div>
        </fieldset>

        <fieldset class="fieldset">
          <legend>Where you are starting from</legend>
          <div class="field">
            <label for="r-level">Your current level <span class="req">*</span></label>
            <select class="select input" id="r-level" name="Skill level" required>
              <option value="">Choose one…</option>
{levels}
            </select>
          </div>
          <div class="field">
            <label for="r-skills">What can you already do? <span class="muted" style="font-weight:400">(your present skill set, if any)</span></label>
            <textarea class="textarea" id="r-skills" name="Present skill set"
              placeholder="e.g. I can write basic Python, I have used an Arduino once, I can solder a little — or simply: nothing yet."></textarea>
          </div>
          <div class="field">
            <label for="r-challenge">What engineering or tech challenge are you facing right now? <span class="req">*</span></label>
            <textarea class="textarea" id="r-challenge" name="Current challenge" required
              placeholder="What is actually blocking you? A project that will not work, no access to equipment, not knowing where to start, a concept that will not click…"></textarea>
          </div>
          <div class="field">
            <label for="r-hope">What do you hope to learn here? <span class="req">*</span></label>
            <textarea class="textarea" id="r-hope" name="Hopes to learn" required
              placeholder="What would make this bootcamp worth your time?"></textarea>
          </div>
          <div class="field">
            <label for="r-extra">Anything else we should know?</label>
            <textarea class="textarea" id="r-extra" name="Anything else" style="min-height:80px"
              placeholder="Accessibility needs, scheduling constraints, anything at all."></textarea>
          </div>
        </fieldset>

        <button class="btn btn--primary btn--block btn--lg" type="submit">{ico("check")} Submit registration</button>
        <p class="form-status" role="status" aria-live="polite"></p>
        <p class="form-note">Free of charge. We use your answers to shape the sessions and to contact you
          about dates — nothing else, and we do not pass them on.</p>
      </form>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="cta-band bracketed reveal">
        <span class="eyebrow">{ico("users")} Questions first?</span>
        <h2 class="mt-2">Ask before you sign up</h2>
        <p>The community channel is the fastest way to reach us — ask anything about the bootcamp,
          the dates or what to bring.</p>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("wa")} Ask on WhatsApp</a>
          <a class="btn btn--ghost btn--lg" href="contact.html">Contact us {ico("arrow")}</a>
        </div>
      </div>
    </div>
  </section>

'''
    write("register.html", f"Register — Free Hardware Bootcamp — {ORG}",
          "Register free for Africa's Hardware Revolution: From Spark to Ignition — a free hardware bootcamp at UNN Nsukka covering robotics, embedded systems, IoT, PCB design, CAD, edge AI, 3D printing and more.",
          body)


def main():
    print("Building site…")
    build_home(); build_about(); build_programs(); build_projects(); build_community(); build_register(); build_contact()
    print("Done.")

if __name__ == "__main__":
    main()
