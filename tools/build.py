#!/usr/bin/env python3
"""
Builds the static pages for the Ogbontor Engineering Enterprise site.

Every page is plain, dependency-free HTML once generated — this script only
exists so the shared shell (head, header, footer) stays identical across pages.
Edit the data/partials here and re-run `python3 tools/build.py`, or just edit
the generated .html files directly if you prefer.
"""
import os, re, math

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


# ------------------------------------------------------- motion graphics ----
# Cyber / mechatronic set pieces. Every one of them is inert SVG whose motion
# lives entirely in CSS keyframes, so the single prefers-reduced-motion rule in
# styles.css freezes the whole set at once. Nothing here carries meaning a
# screen reader needs, so it is all aria-hidden.

def _gear_path(cx, cy, r_out, r_root, teeth):
    """One involute-ish gear outline: tip, tip, root, root, repeat."""
    pts, seg = [], 2 * math.pi / teeth
    for i in range(teeth):
        base = i * seg
        for frac, r in ((0.00, r_root), (0.13, r_out), (0.37, r_out), (0.50, r_root)):
            a = base + seg * frac
            pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return "M" + "L".join(pts) + "Z"


# Trace routing for the circuit backdrop — orthogonal runs with 45° breaks,
# the way a real board is fanned out.
CIRCUIT_TRACES = [
  "M-20 88 H170 L240 158 H430 L486 104 H722 L792 174 H1220",
  "M-20 248 H118 L188 178 H344 L402 236 H640 L702 298 H902 L962 238 H1220",
  "M-20 424 H262 L332 354 H520 L582 414 H820 L882 354 H1220",
  "M-20 546 H402 L472 476 H700 L762 536 H1220",
  "M302 -20 V118 L362 178 V342 L302 402 V660",
  "M898 -20 V138 L838 198 V380 L898 440 V660",
  "M1118 -20 V220 L1058 280 V660",
  "M126 660 V520 L186 460 V300",
]
CIRCUIT_PADS = [(240,158),(486,104),(792,174),(188,178),(402,236),(702,298),(962,238),
                (332,354),(582,414),(882,354),(472,476),(762,536),(362,178),(838,198),
                (1058,280),(186,460),(302,402),(898,440)]


def _chip(x, y, w, h, delay):
    n = max(3, int(w // 15))
    pins = "".join(
        f'<path class="mgc-pin" d="M{x + w*(i+0.5)/n:.1f} {y}V{y-9}"/>'
        f'<path class="mgc-pin" d="M{x + w*(i+0.5)/n:.1f} {y+h}V{y+h+9}"/>'
        for i in range(n))
    return (f'<g class="mgc-chip" style="animation-delay:{delay}s">{pins}'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7"/>'
            f'<rect class="mgc-die" x="{x+w*.28:.1f}" y="{y+h*.28:.1f}" '
            f'width="{w*.44:.1f}" height="{h*.44:.1f}" rx="3"/></g>')


def mg_circuit(cls=""):
    """Full-bleed board backdrop: static traces, pads that blink, data pulses
       running the routes, and three ICs breathing behind it all."""
    traces = "\n".join(f'  <path class="mgc-trace" d="{d}"/>' for d in CIRCUIT_TRACES)
    pulses = "\n".join(
        f'  <path class="mgc-pulse" d="{d}" style="animation-delay:{i*1.15:.2f}s;'
        f'animation-duration:{6.5 + (i % 4) * 1.6:.1f}s"/>'
        for i, d in enumerate(CIRCUIT_TRACES))
    pads = "\n".join(
        f'  <circle class="mgc-pad" cx="{x}" cy="{y}" r="4" '
        f'style="animation-delay:{(i * .41) % 3.4:.2f}s"/>'
        for i, (x, y) in enumerate(CIRCUIT_PADS))
    chips = "\n  ".join([_chip(430, 128, 56, 46, 0), _chip(640, 262, 62, 50, 1.4),
                         _chip(520, 380, 62, 50, 2.6)])
    return f'''<svg class="mg mg-circuit {cls}" viewBox="0 0 1200 620"
     preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
{traces}
{pads}
  {chips}
{pulses}
</svg>'''


def mg_arm(cls=""):
    """Mechatronic pick-and-place: shoulder sweeps, forearm counter-rotates,
       the gripper closes on a die and sets it on the board."""
    return f'''<svg class="mg mg-arm {cls}" viewBox="0 0 360 330" aria-hidden="true" focusable="false">
  <g class="mga-hud">
    <path d="M14 14h34M14 14v34M346 14h-34M346 14v34M14 316h34M14 316v-34M346 316h-34M346 316v-34"/>
  </g>
  <g class="mga-bench">
    <path class="mga-floor" d="M24 298H336"/>
    <path class="mga-floor mga-floor--2" d="M52 310H308"/>
    <rect class="mga-board" x="244" y="272" width="66" height="22" rx="4"/>
    <path class="mga-board-trace" d="M252 283h14m8 0h12m8 0h14"/>
  </g>
  <g class="mga-shoulder">
    <rect class="mga-limb" x="172" y="126" width="28" height="100" rx="14"/>
    <path class="mga-limb-line" d="M186 140v72"/>
    <g class="mga-fore">
      <rect class="mga-limb" x="175" y="56" width="22" height="78" rx="11"/>
      <path class="mga-limb-line" d="M186 68v54"/>
      <g class="mga-wrist">
        <circle class="mga-joint" cx="186" cy="60" r="9"/>
        <path class="mga-jaw mga-jaw--l" d="M180 56v-14h-8v-13"/>
        <path class="mga-jaw mga-jaw--r" d="M192 56v-14h8v-13"/>
        <rect class="mga-payload" x="176" y="22" width="20" height="14" rx="3"/>
        <path class="mga-beam" d="M186 46v-30"/>
      </g>
      <circle class="mga-joint" cx="186" cy="130" r="12"/>
    </g>
  </g>
  <circle class="mga-joint mga-joint--base" cx="186" cy="224" r="15"/>
  <rect class="mga-column" x="166" y="222" width="40" height="54" rx="9"/>
  <rect class="mga-base" x="136" y="272" width="100" height="24" rx="8"/>
  <g class="mga-spark"><circle cx="272" cy="268" r="2.5"/><circle cx="282" cy="262" r="2"/><circle cx="264" cy="260" r="1.6"/></g>
</svg>'''


def mg_gears(cls=""):
    """Three meshed gears — the programme at full speed."""
    a = _gear_path(112, 112, 62, 50, 16)
    b = _gear_path(206, 148, 50, 40, 13)
    c = _gear_path(98, 216, 54, 44, 14)
    return f'''<svg class="mg mg-gears {cls}" viewBox="30 36 244 244" aria-hidden="true" focusable="false">
  <g class="mgg mgg--cw">
    <path class="mgg-body" d="{a}"/>
    <circle class="mgg-hub" cx="112" cy="112" r="20"/>
    <circle class="mgg-bore" cx="112" cy="112" r="8"/>
    <g class="mgg-spokes"><circle cx="112" cy="78" r="6"/><circle cx="141" cy="129" r="6"/><circle cx="83" cy="129" r="6"/></g>
  </g>
  <g class="mgg mgg--ccw mgg--fast">
    <path class="mgg-body" d="{b}"/>
    <circle class="mgg-hub" cx="206" cy="148" r="16"/>
    <circle class="mgg-bore" cx="206" cy="148" r="6"/>
    <g class="mgg-spokes"><circle cx="206" cy="122" r="5"/><circle cx="229" cy="161" r="5"/><circle cx="183" cy="161" r="5"/></g>
  </g>
  <g class="mgg mgg--ccw mgg--slow">
    <path class="mgg-body" d="{c}"/>
    <circle class="mgg-hub" cx="98" cy="216" r="17"/>
    <circle class="mgg-bore" cx="98" cy="216" r="7"/>
    <g class="mgg-spokes"><circle cx="98" cy="188" r="5"/><circle cx="122" cy="230" r="5"/><circle cx="74" cy="230" r="5"/></g>
  </g>
  <g class="mgg-hud"><path d="M256 62h12v12M48 254H36v-12"/></g>
</svg>'''


def mg_core(cls=""):
    """A die under power: rings expanding out of it, packets running the buses."""
    bus, pkt = [], []
    routes = [(160, 96, 160, 8), (160, 224, 160, 312), (96, 160, 8, 160), (224, 160, 312, 160),
              (116, 116, 44, 44), (204, 116, 276, 44), (116, 204, 44, 276), (204, 204, 276, 276)]
    for i, (x1, y1, x2, y2) in enumerate(routes):
        bus.append(f'  <path class="mgk-bus" d="M{x1} {y1}L{x2} {y2}"/>')
        pkt.append(f'  <path class="mgk-packet" d="M{x1} {y1}L{x2} {y2}" '
                   f'style="animation-delay:{i * .34:.2f}s"/>')
    return f'''<svg class="mg mg-core {cls}" viewBox="0 0 320 320" aria-hidden="true" focusable="false">
{chr(10).join(bus)}
  <circle class="mgk-ring" cx="160" cy="160" r="72"/>
  <circle class="mgk-ring" cx="160" cy="160" r="72" style="animation-delay:1.1s"/>
  <circle class="mgk-ring" cx="160" cy="160" r="72" style="animation-delay:2.2s"/>
  <circle class="mgk-orbit-path" cx="160" cy="160" r="104"/>
  <g class="mgk-orbit"><circle cx="160" cy="56" r="5"/></g>
  <g class="mgk-orbit mgk-orbit--rev"><circle cx="160" cy="264" r="3.5"/></g>
  <rect class="mgk-die" x="112" y="112" width="96" height="96" rx="16"/>
  <rect class="mgk-die-inner" x="132" y="132" width="56" height="56" rx="8"/>
  <path class="mgk-die-grid" d="M132 150h56M132 168h56M150 132v56M168 132v56"/>
  <circle class="mgk-spark" cx="160" cy="160" r="9"/>
{chr(10).join(pkt)}
</svg>'''


def mg_wave(cls=""):
    """Oscilloscope trace with a sweeping graticule bar. The timebase stretches
       to the strip it sits in, so the stroke is pinned with non-scaling-stroke."""
    ve = 'vector-effect="non-scaling-stroke"'
    return f'''<svg class="mg mg-wave {cls}" viewBox="0 0 420 120" preserveAspectRatio="none"
     aria-hidden="true" focusable="false">
  <path class="mgw-grid" {ve} d="M0 30h420M0 60h420M0 90h420M60 0v120M120 0v120M180 0v120M240 0v120M300 0v120M360 0v120"/>
  <path class="mgw-trace" {ve} d="M0 60h34l10-30 10 60 12-46 10 16h30l12-34 10 52 12-30 10 12h44l10-40 10 64 12-40 10 4h34l12-26 10 44 12-30 10 12h58"/>
  <path class="mgw-scan" {ve} d="M0 0v120"/>
</svg>'''


def mg_radar(cls=""):
    """Sweep, rings, contacts — the lab looking for the next build."""
    return f'''<svg class="mg mg-radar {cls}" viewBox="0 0 240 240" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="mgr-sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="currentColor" stop-opacity=".38"/>
      <stop offset="100%" stop-color="currentColor" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <circle class="mgr-ring" cx="120" cy="120" r="108"/>
  <circle class="mgr-ring" cx="120" cy="120" r="76"/>
  <circle class="mgr-ring" cx="120" cy="120" r="44"/>
  <path class="mgr-cross" d="M120 12v216M12 120h216"/>
  <g class="mgr-sweep"><path d="M120 120L228 120A108 108 0 0 0 174 26Z" fill="url(#mgr-sweep)"/>
    <path class="mgr-edge" d="M120 120L228 120"/></g>
  <g class="mgr-blips">
    <circle cx="168" cy="84" r="4"/>
    <circle cx="86" cy="152" r="4" style="animation-delay:1.3s"/>
    <circle cx="148" cy="170" r="4" style="animation-delay:2.6s"/>
  </g>
</svg>'''



# The programme runs in order: the conference opens it, three weeks of
# building follow, the hackathon closes it. Rendered as a rail on the home
# page and as cards on the register page — one source, so the order of the
# three acts can never drift between them.
EVENTS = [
 ("award", "01", "The Conference", "One day &middot; opens the programme",
  "Speakers from Nigeria and abroad, live demos, 800+ people in one room.",
  ["One day", "800+ attendees", "Free seat"]),
 ("book",  "02", "The Bootcamp", "Three weeks &middot; free",
  "Eleven tracks, benches, boards and a partner. You leave having shipped.",
  ["Three weeks", "Eleven tracks", "Hardware supplied"]),
 ("zap",   "03", "The Hackathon", "Closes the bootcamp",
  "Final week. Teams build against a brief. Demo day crowns the winners.",
  ["Final week", "Team builds", "Prizes"]),
]

PROGRAMME_LINE = "Conference first. Then three weeks on the bench."

# The month is confirmed; the day and the venue are not. Say both together
# everywhere, so nobody reads "November" as a full date.
EVENT_MONTH = "November"
EVENT_WHEN_NOTE = "Exact dates &amp; venue announced soon"


def date_plate(cls=""):
    """The month, set loud, with the honest caveat sitting next to it."""
    return f'''<div class="when-plate {cls}">
          <span class="when-month">{EVENT_MONTH}</span>
          <span class="when-note">{ico("calendar")} {EVENT_WHEN_NOTE}</span>
        </div>'''


def programme_rail():
    """The three acts as one connected rail, each with its own motion graphic.
       The conference sits first because that is the order it now runs in."""
    art = {"01": mg_core("mg--act"), "02": mg_arm("mg--act"), "03": mg_gears("mg--act")}
    items = []
    for i, (k, no, title, when, blurb, chips) in enumerate(EVENTS):
        chip_html = "".join(f'<span>{c}</span>' for c in chips)
        items.append(f'''      <li class="prog-act reveal" data-delay="{i*0.12:.2f}">
        <div class="prog-art">{art[no]}<span class="prog-num">{no}</span></div>
        <div class="prog-body">
          <span class="prog-when">{ico(k)} {when}</span>
          <h3>{title}</h3>
          <p>{blurb}</p>
          <div class="prog-chips">{chip_html}</div>
        </div>
      </li>''')
    return '''    <ol class="prog-rail">
''' + "\n".join(items) + "\n    </ol>"

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
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap">
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
  "sameAs": ["{WHATSAPP}"]
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
      <span class="pill">Registration open</span>
      <strong>{EVENT_MONTH} &mdash; conference, then a 3-week bootcamp</strong>
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
        <p>{TAGLINE}. Students across South-East Nigeria designing, building and shipping
           real hardware.</p>
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
          <li><a href="register.html">Register (free)</a></li>
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
 ("CNG Protect", "Monitors CNG cylinders — pressure, integrity, custody — signed on the device and verifiable on chain. Now its own company.",
  "gallery/cng-protect-module.jpg", ["IoT", "Blockchain", "Safety"],
  {"link": "https://cngprotect.com", "logo": "companies/cng-protect.jpg", "logo_alt": "CNG Protect logo"}),
 ("Joint-Agent IDE", "Writes firmware, compiles, debugs and flashes real hardware from one browser tab. Spun out of this lab.",
  "gallery/joint-agent-dashboard.jpg", ["Software", "Embedded", "AI Agent"],
  {"link": "https://jointagentide.com", "logo": "companies/joint-agent.png", "logo_alt": "Joint-Agent logo"}),
 ("Line Following Robot", "Sensor array, tuned PID loop, chassis built in-house. Press play to watch it track.",
  "line-following-poster.jpg", ["Robotics", "Control", "PID"],
  {"video": "video/line-following-robot.mp4"}),
 ("Smart Solar Power Measurement System", "Logs output across six panels at once, comparing fin, air and water cooling on a live rooftop.",
  "gallery/solar-deployment-site.jpg", ["Energy", "Telemetry", "Sensors"]),
 ("Bluetooth Six-Wheel Terrain Climber", "A Bluetooth rover built to keep traction on the broken ground around campus.",
  "gallery/terrain-climber-complete.jpg", ["Robotics", "Mechanical", "Control"]),
 ("Smart Walking Stick for the Blind", "Ultrasonic ranging with haptic and audible feedback. Field-tested on open ground.",
  "gallery/walking-stick-bench.jpg", ["Assistive Tech", "Sensors"]),
 ("Ultraviolet Radiation Detection System", "A handheld UV index meter in a sealed enclosure, for people who work in open sun.",
  "gallery/uv-detector-enclosure.jpg", ["Instrumentation", "Health"]),
 ("Gas Leak & Temperature Monitor", "Temperature and combustible-gas monitoring that alarms the moment a threshold is crossed.",
  "gallery/gas-monitor-enclosure.jpg", ["Safety", "IoT", "Alarms"]),
 ("Pulse & Heart Rate Monitor", "Optical pulse and SpO2, pushed to a relative or clinician over Telegram.",
  "gallery/pulse-monitor-reading.jpg", ["Medical", "Connectivity"]),
 ("Obstacle Avoidance Robot", "Navigates unmapped obstacles on ultrasonic sweeps and reactive control.",
  "gallery/obstacle-robot-complete.jpg", ["Robotics", "Autonomy"]),
]

PROJECTS_WIP = [
 ("Joint-Agent Board & IoT Kit", "Nigeria's first IoT-blockchain board, signing sensor readings on the board itself.",
  "gallery/joint-agent-kit.jpg", ["IoT", "Blockchain", "Hardware"],
  {"logo": "companies/joint-agent.png", "logo_alt": "Joint-Agent logo"}),
 ("Robotic Arm — 6 Degrees of Freedom", "Six axes, inverse kinematics, teach-pendant workflow. The teaching rig for our robotics tier.",
  "gallery/robotic-arm.jpg", ["Robotics", "Kinematics"]),
 ("Autonomous Self-Driving Vehicle", "A self-driving platform: lane keeping, obstacle classification, route planning.",
  "placeholders/autonomous-vehicle.svg", ["Computer Vision", "Autonomy", "Edge AI"]),
 ("Smart Electrocardiogram System", "A low-cost ECG front end for clinics that cannot justify imported equipment.",
  "placeholders/ecg-system.svg", ["Medical", "Signal Processing"]),
]

CURRICULUM = [
 ("I", "Foundational Knowledge", "The vocabulary everything else is built on.", [
   "Introduction to Embedded Systems",
   "Fundamentals of Electronics and Circuit Design",
   "Programming Essentials for Embedded Systems",
   "Introduction to Robotics"]),
 ("II", "Intermediate Skills", "Where members start shipping working hardware.", [
   "Microcontroller Programming and Applications",
   "Sensors and Actuators",
   "Communication Protocols",
   "Real-Time Operating Systems (RTOS)",
   "Internet of Things (IoT) Systems and Applications"]),
 ("III", "Advanced Topics", "The work that separates a hobbyist from an engineer.", [
   "Advanced Robotics and AI Integration",
   "Edge Computing and AI for Embedded Systems",
   "FPGA Programming and Applications",
   "Power Management in Embedded Systems",
   "CPU Design and Architecture",
   "GPU Design and Parallel Processing",
   "Autonomous Systems and Control",
   "Advanced Sensor Fusion Techniques"]),
 ("IV", "CAD and Design Integration", "Breadboard to something you can hold and mount.", [
   "CAD for Embedded Systems and Robotics",
   "Design for Embedded Systems and Robotics Projects"]),
 ("V", "Capstone Projects", "Real builds, real deadlines, real users.", [
   "Real-world embedded systems and robotics projects with CAD design",
   "Industry internships and collaborations",
   "Entrepreneurship and startup development",
   "Ethical considerations in embedded systems and robotics"]),
]

def project_card(p, status, compact=False):
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

    blurb = "" if compact else f"\n            <p>{desc}</p>"
    return f'''        <article class="{cls}">
{media}
          <div class="project-body">
            {title}{blurb}
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
    featured = "\n".join(project_card(p, "built", compact=True) for p in PROJECTS_BUILT[:6])
    stats = "\n".join([
        stat(14, "Projects in the portfolio"),
        stat(19, "Curriculum modules"),
        stat(5,  "Skill tiers, foundation to capstone"),
        stat(1,  "Hardware lab at UNN Nsukka"),
    ])
    pillars = [
      ("book",  "We train",     "Nineteen modules, Ohm's law to FPGA. Taught with a board in front of you."),
      ("wrench","We build",     "Real prototypes from week one. Fourteen systems on the bench so far."),
      ("rocket","We incubate",  "Capstones that prove themselves become products. We help with IP and pilot users."),
      ("globe", "We manufacture","Hardware designed and assembled in Enugu, not imported."),
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
    <div class="backdrop">
      <div class="grid-lines"></div>
      <div class="hero-floor" aria-hidden="true"></div>
      {mg_circuit("backdrop-circuit")}
      <div class="scanlines" aria-hidden="true"></div>
    </div>
    <div class="container">
      <div class="hero-grid">
        <div>
          <span class="eyebrow">{ico("pin")} <span data-scramble>University of Nigeria, Nsukka &middot; Enugu State</span></span>
          <h1>South-East Nigeria's <span class="grad-text">largest student hardware tech</span>
            <span class="underline-accent">community</span>.</h1>
          <p class="lede">
            Students here stop reading about hardware and start building it. Embedded systems,
            robotics, IoT and blockchain devices, out of our lab in Nsukka.
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
              <p>Conference, then three weeks on the bench. Open to every student, no fee.</p>
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
              <p>A conference for 800+, then three weeks of building. Speakers from Nigeria and abroad.</p>
              <a class="btn btn--lg" href="index.html#sponsors">{ico("handshake")} Sponsor the programme</a>
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
        <p class="lede">Design a part on Monday, hold it on Tuesday. No six-week wait on an import.</p>
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
          <p>Enclosures, brackets, jigs, custom parts. Free for members.</p>
        </article>
        <article class="card reveal" data-delay="0.08">
          <div class="card-ico">{ico("wrench")}</div>
          <h3>A bench that is actually equipped</h3>
          <p>Soldering stations, measurement gear, dev boards, a component library.</p>
        </article>
        <article class="card reveal" data-delay="0.16">
          <div class="card-ico">{ico("rocket")}</div>
          <h3>Prototype to product</h3>
          <p>Print, test, revise, print again. That gap is school project versus product.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--tight" id="bootcamp">
    <div class="container">
      <div class="bootcamp bracketed reveal">
       <div class="bootcamp-grid">
        <div>
        <span class="eyebrow">{ico("zap")} <span class="sec-no">02</span> The programme &middot; free, open to all</span>
        <h2>Africa's Hardware Revolution</h2>
        <p class="theme-line">From Spark to Ignition</p>
        {date_plate()}
        <p class="lede">{PROGRAMME_LINE} A hackathon closes it.</p>
        <div class="bootcamp-facts">
          <span>{ico("check")} No fee</span>
          <span>{ico("users")} No experience needed</span>
          <span>{ico("pin")} UNN Nsukka</span>
          <span>{ico("tools")} Hardware supplied</span>
        </div>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="register.html">{ico("clipboard")} Register free</a>
          <a class="btn btn--ghost btn--lg" href="programs.html#bootcamp">What you'll learn {ico("arrow")}</a>
        </div>
        </div>
        <div class="bootcamp-art">
          <div class="holo-frame">
            {mg_circuit("holo-circuit")}
            <img src="assets/img/africa-circuit.png"
                 alt="Africa drawn as a circuit board, with the lab at UNN Nsukka marked" width="330" height="440" loading="lazy">
            <span class="holo-sweep" aria-hidden="true"></span>
          </div>
        </div>
       </div>
      </div>

{programme_rail()}
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <div class="mg-strip reveal" aria-hidden="true">{mg_wave()}</div>
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
          here, untrained and unequipped. That is the gap we close.</p>
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
        <p class="lede">Boards populated, enclosures printed, firmware flashed, systems run outside the
          lab. No renders.</p>
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
          <p class="lede mt-2">Your first resistor to CPU architecture, in order. It ends in a capstone
            that has to work in front of real users.</p>
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
            <p class="lede mt-2">A bench, a project team, and a supervisor who can assess the engineering
              you actually did.</p>
            <ul class="siwes-points">
              <li>{ico("check")}<span>Logbooks signed, ITF documentation handled.</span></li>
              <li>{ico("check")}<span>A real project team, a deliverable, a deadline.</span></li>
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
          <p class="lede mt-2">The hardest hour in hardware is the one where nothing works and you have
            no idea why. A community is what gets you through it.</p>
          <ul class="check-list">
            <li>{ico("check")}<span><strong>Weekly build nights</strong> — open lab, people to ask.</span></li>
            <li>{ico("check")}<span><strong>Three-week cohort bootcamps</strong> — intensive, and free.</span></li>
            <li>{ico("check")}<span><strong>Mentorship</strong> — someone two steps ahead, not twenty.</span></li>
            <li>{ico("check")}<span><strong>A component library</strong> — borrow it, don't buy it.</span></li>
            <li>{ico("check")}<span><strong>Demo days</strong> — show it to people who understand it.</span></li>
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
        <p class="lede">Electronics, vehicles and smart systems <em>designed</em> here, for African roads,
          climate and power.</p>
      </div>
      <div class="grid grid-3">
        <figure class="project reveal" data-zoom>
          <div class="project-media"><img src="assets/img/gallery/made-in-enugu-factory.jpg" alt="Concept: an electronics assembly line operating in Enugu" loading="lazy" width="800" height="500"></div>
          <div class="project-body"><h3>Consumer electronics</h3><p>Assembly lines staffed by engineers we trained.</p></div>
        </figure>
        <figure class="project reveal" data-delay="0.08" data-zoom>
          <div class="project-media"><img src="assets/img/gallery/made-in-enugu-automotive.jpg" alt="Concept: vehicle drivetrain assembly in Enugu" loading="lazy" width="800" height="500"></div>
          <div class="project-body"><h3>Vehicles &amp; mobility</h3><p>Drivetrains and controls for the roads we drive on.</p></div>
        </figure>
        <figure class="project reveal" data-delay="0.16" data-zoom>
          <div class="project-media"><img src="assets/img/gallery/made-in-enugu-aircraft.jpg" alt="Concept: aircraft maintenance and assembly in Enugu" loading="lazy" width="800" height="500"></div>
          <div class="project-body"><h3>Aerospace &amp; heavy systems</h3><p>The far end of the roadmap, and why the curriculum goes so deep.</p></div>
        </figure>
      </div>
      <p class="center muted mt-3" style="font-size:.82rem">Illustrative concepts &mdash; the roadmap, not facilities in operation today.</p>
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
        <p class="lede"><strong>South-East Nigeria's biggest hardware conference</strong> opens the programme.
          Three weeks of building follow. Help us put both on.</p>
      </div>

      <div class="grid grid-4">
        <article class="card reveal">
          <div class="card-ico">{ico("users")}</div>
          <h3>800+ attendees</h3>
          <p>Students, makers and engineers from across the South-East, in one room.</p>
        </article>
        <article class="card reveal" data-delay="0.07">
          <div class="card-ico">{ico("globe")}</div>
          <h3>Speakers worldwide</h3>
          <p>Practitioners on hardware they actually shipped.</p>
        </article>
        <article class="card reveal" data-delay="0.14">
          <div class="card-ico">{ico("layers")}</div>
          <h3>Where your support goes</h3>
          <p>Venue, components, speaker travel, and free seats for students who could not otherwise come.</p>
        </article>
        <article class="card reveal" data-delay="0.21">
          <div class="card-ico">{ico("target")}</div>
          <h3>What you get</h3>
          <p>Branding across the event and this site, a stand, first access to the people you want to hire.</p>
        </article>
      </div>

      <div class="partners mt-4 reveal">
{partners}
      </div>

      <div class="sponsor-cta mt-3 reveal">
        <div class="mg-inline mg-inline--sm" aria-hidden="true">{mg_radar()}</div>
        <h3>This space is for your logo</h3>
        <p>Equipment, component budgets, speaker travel or funding. Say what you have in mind and we
          will send the deck.</p>
        <div class="hero-cta" style="justify-content:center">
          <a class="btn btn--primary" href="mailto:{EMAIL}?subject=Sponsorship%20%E2%80%94%20Ogbontor%20hardware%20conference%20%26%20bootcamp">{ico("mail")} Become a sponsor</a>
          <a class="btn btn--ghost" href="contact.html">Talk to us first {ico("arrow")}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="cta-band bracketed reveal">
        {mg_circuit("cta-circuit")}
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
    <div class="backdrop">
      <div class="grid-lines"></div>
      {mg_circuit("backdrop-circuit backdrop-circuit--sm")}
      <div class="scanlines" aria-hidden="true"></div>
    </div>
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
            <p class="founder-bio">I started Ogbontor because the capacity is already here. The bench,
              the curriculum and the room were what was missing.</p>
            <p class="founder-bio" style="margin-top:.8rem">Behind me is a solid team of hardware
              professionals. <strong>We will introduce them shortly.</strong></p>
            <div class="founder-links">
              <a class="btn btn--ghost" href="mailto:{EMAIL}">{ico_mail} Email me</a>
              <a class="btn btn--ghost" href="{WHATSAPP}" target="_blank" rel="noopener">{ico_wa} Community</a>
            </div>
          </div>
        </article>'''

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
        f"A hardware technology enterprise and student community at the University of Nigeria, Nsukka. We train, we prototype, we turn what works into products.", "About")

    body += f'''  <section class="section">
    <div class="container">
      <div class="split">
        <div>
          <span class="eyebrow">{ico("info")} The problem</span>
          <h2 class="mt-2">Africa consumes technology it cannot repair</h2>
          <div class="prose mt-2">
            <p>Almost everything electronic here was designed somewhere else and arrives as a sealed box.
               When it fails it is replaced, not fixed. When it cannot take unstable mains, dust or heat,
               it is tolerated, not redesigned.</p>
            <p>The engineering capacity to do otherwise never gets built, because there is nowhere to learn
               it properly and nothing to practise on.</p>
            <p><strong>That is a training problem before it is an industrial one.</strong></p>
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
            <p>Nigeria can solve its own technological problems. Talent was never what was missing.</p>
            <p>What was missing: a bench, a curriculum deep enough to matter, and a room of people on the
               same problem at once. We put those three in Nsukka.</p>
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
        <p class="lede">Larger than a student club should attempt. Saying them out loud keeps the
          curriculum honest.</p>
      </div>
      <div class="grid grid-3">
        <article class="project reveal">
          <div class="project-media">
            <img src="assets/img/gallery/vision-electronics.jpg" alt="Concept: Nigerian engineers working with circuit boards and consumer devices" loading="lazy" width="800" height="500">
          </div>
          <div class="project-body">
            <h3>Indigenous consumer electronics</h3>
            <p>Smartphones, televisions and household electronics designed and assembled here. It is why the
               curriculum runs to CPU and GPU architecture.</p>
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
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="cta-band bracketed reveal">
        {mg_circuit("cta-circuit")}
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
        "Nineteen modules across five tiers, run as hands-on cohorts. Every tier ends in hardware you built, not an exam.", "Programs")

    body += f'''  <section class="section section--tight">
    <div class="container">
      <div class="bootcamp bracketed reveal">
       <div class="bootcamp-grid">
        <div>
        <span class="eyebrow">{ico("zap")} The programme &middot; free, open to all</span>
        <h2>Africa's Hardware Revolution</h2>
        <p class="theme-line">From Spark to Ignition</p>
        {date_plate()}
        <p class="lede">{PROGRAMME_LINE} A hackathon closes it.</p>
        <p>Free, and open to every student at UNN Nsukka — whatever you study, whether or not you
           have ever touched a circuit.</p>
        <div class="bootcamp-facts">
          <span>{ico("award")} Conference opens it</span>
          <span>{ico("book")} Three-week bootcamp</span>
          <span>{ico("zap")} Hackathon closes it</span>
          <span>{ico("tools")} Hardware supplied</span>
        </div>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="register.html">{ico("clipboard")} Register free</a>
        </div>
        </div>
        <div class="bootcamp-art">
          <div class="holo-frame">
            {mg_circuit("holo-circuit")}
            <img src="assets/img/africa-circuit.png"
                 alt="Africa drawn as a circuit board, with the lab at UNN Nsukka marked" width="330" height="440" loading="lazy">
            <span class="holo-sweep" aria-hidden="true"></span>
          </div>
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
          <h2 class="mt-2">Three weeks, in person, free</h2>
          <div class="prose mt-2">
            <p>How most members enter. A cohort takes the foundational tier together over
               <strong>three weeks</strong>, with boards on the bench from day one.</p>
            <p>You get a kit, a partner, a bug, and somebody experienced within arm's reach.</p>
          </div>
          <ul class="check-list">
            <li>{ico("check")}<span><strong>Cohort-based</strong> — you start and finish with the same people.</span></li>
            <li>{ico("check")}<span><strong>Hardware supplied</strong> — boards, sensors and tools, from our library.</span></li>
            <li>{ico("check")}<span><strong>Project-assessed</strong> — you pass by building.</span></li>
            <li>{ico("check")}<span><strong>Free for members</strong> — the cost barrier is what we are removing.</span></li>
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
        <p class="lede">Tiers I–IV are taught. Tier V is the capstone: a real build, on a deadline, in
          front of real users.</p>
      </div>
{tiers_html}
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("target")} Specialist tracks</span>
        <h2>Where members go after the core</h2>
        <p class="lede">With the first two tiers behind you, pick a direction and go deep with a project
          team.</p>
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
        <p class="lede">A bench, a project team and a supervisor who can assess the engineering you
          actually did. Open to universities, polytechnics and colleges of education.</p>
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
          <p>The same tiers our members sit: embedded systems, robotics, IoT, PCB design, CAD, edge AI,
             3D printing, fabrication.</p>
        </article>
      </div>

      <div class="sec-head mt-4">
        <span class="eyebrow">{ico("award")} First of its kind</span>
        <h2>The deep end</h2>
        <p class="lede">The <strong>first student-led hardware lab in South-East Nigeria to prototype
          in these areas</strong>. Placement students join the R&amp;D lines early, on foundational work.</p>
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
            <p>Airframe prototyping, avionics and control systems. The longest horizon on the
               roadmap.</p>
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
        <p class="lede">Access and commitment, not fees. Every level above Associate is earned by
          building.</p>
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
        {mg_circuit("cta-circuit")}
        <span class="eyebrow">{ico("book")} Intake is open</span>
        <h2 class="mt-2">Start at Module 01</h2>
        <p>No prior electronics, no laptop, no particular course. Turn up.</p>
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
        "Designed, assembled, programmed and debugged by members. Some deployed; the rest still on the bench.", "Projects")

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
        <p class="lede">Designed, under active development, not finished. These are the ones taking
          members.</p>
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
        {mg_circuit("cta-circuit")}
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
  f"<br><br>The <strong>conference and the free three-week bootcamp are specific to UNN Nsukka</strong> for this first run. Other South-East universities are next &mdash; at least one per state."),
 ("Does it cost anything?",
  "Associate and Builder membership are free, and so are bootcamp seats. The cost barrier is the thing we exist to remove. Funded capstones are handled case by case."),
 ("What course do I need to be studying?",
  "Any. Our members come from electrical engineering, computer science, mechanical, physics, and from outside the sciences entirely. Hardware needs people who can design enclosures and talk to users as much as it needs firmware engineers."),
 ("Do I need my own laptop or components?",
  "It helps, but no. The component library lends boards, sensors and tools, and lab machines are open during lab hours."),
 ("How much time does it take?",
  "A build night is one evening a week. The bootcamp runs three weeks and is far more intense. Project teams set their own pace."),
 ("Can my company partner or sponsor?",
  f"Yes — equipment, component budgets, internship places and project sponsorship are all useful to us. Write to {EMAIL} and say what you have in mind."),
 ("What happens after the capstone?",
  "The strongest go into incubation — IP, a pitch, pilot users, company formation. Both portfolio companies, <strong>Joint-Agent</strong> and <strong>CNG-Protect</strong>, started this way."),
]

def build_community():
    what = [
      ("tools",  "Weekly build nights",  "Bring what you are working on, or pick up a community build. Benches, tools, and people who already made your mistake."),
      ("users",  "Study groups",         "Small groups on the same module. Better than grinding a datasheet alone at 2am."),
      ("hand",   "Mentorship pairing",   "Paired with someone two steps ahead — near enough to remember being stuck where you are."),
      ("layers", "Component library",    "Borrow the sensor, the analyser, the dev board. A missing part should not stop a project."),
      ("graph",  "Demo days",            "Every cohort ends showing its work to an audience that asks hard questions."),
      ("zap",    "Hackathons",           "Competitive builds against a brief. The quickest way to find out what you know."),
      ("target", "Project teams",        "Multi-month teams on the systems under Projects, with roles and a real deadline."),
      ("rocket", "Internships & placement","Introductions to partner companies, and support taking a capstone to product."),
    ]
    what_html = "\n".join(f'''        <article class="card reveal" data-delay="{i%4*0.06:.2f}">
          <div class="card-ico">{ico(k)}</div><h3>{t}</h3><p>{d}</p>
        </article>''' for i,(k,t,d) in enumerate(what))

    steps = [
      ("Join the channel", f"Introduce yourself — what you study, what you want to build. That is the whole application."),
      ("Come to a build night", "Turn up on the next open evening. Nothing is expected the first time but showing up."),
      ("Take the foundational tier", "Join the next cohort, or take Modules 01–04 with a study group."),
      ("Pick a direction", "Pick a track, join a project team, build something with your name on it."),
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
        "Build nights, study groups, mentors, a component library and project teams. The infrastructure that turns interest into ability.", "Community")

    body += f'''  <section class="section">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow">{ico("target")} What membership gets you</span>
        <h2>Eight things that only work with other people</h2>
        <p class="lede">You can learn to code alone. Hardware needs a bench, a scope, a spare part,
          and someone who has seen this failure before.</p>
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
            <p>One open lab evening a week, study groups around whichever modules are running, and
               project teams on their own schedule.</p>
            <p>During the three-week bootcamp the pace changes — cohorts meet most days.</p>
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
            <p>Beginners have to be safe here. The rules are short and we enforce them.</p>
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
        {mg_circuit("cta-circuit")}
        <span class="eyebrow">{ico("wa")} Open intake</span>
        <h2 class="mt-2">Introduce yourself in the channel</h2>
        <p>That is the whole process. Scan the code, say what you study and what you want to build.</p>
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
        "Joining, partnering, sponsoring a cohort or commissioning a build — this is how to reach us.", "Contact")

    body += f'''  <section class="section">
    <div class="container">
      <div class="split">
        <div>
          <span class="eyebrow">{ico("mail")} Send a message</span>
          <h2 class="mt-2">Tell us what you need</h2>
          <p class="lede mt-2">Fill this in and your email app opens with the message ready. Or write to <a href="mailto:{EMAIL}" style="color:var(--accent)">{EMAIL}</a> directly.</p>

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
                <option>Conference / bootcamp / next cohort</option>
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
            <p class="form-note">This opens your own email client. Nothing reaches a server, and we
              store nothing.</p>
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
            <p>Nearly everything happens here. Faster than email for joining, dates or a quick
               question.</p>
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
          <p>Components, tools and bench space for one intake. The most direct route to trained
             hardware engineers.</p>
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
    events_html = programme_rail()
    tracks = "\n".join(f'''          <div class="track">
            <span class="t-ico">{ico(k)}</span><span>{label}</span>
          </div>''' for k, label in BOOTCAMP_TRACKS)

    checks = "\n".join(f'''            <label><input type="checkbox" name="tracks" value="{label}"><span>{label}</span></label>'''
                       for _, label in BOOTCAMP_TRACKS)
    levels = "\n".join(f'''                <option>{l}</option>''' for l in SKILL_LEVELS)

    body = f'''  <section class="page-hero">
    <div class="backdrop">
      <div class="grid-lines"></div>
      {mg_circuit("backdrop-circuit backdrop-circuit--sm")}
      <div class="scanlines" aria-hidden="true"></div>
    </div>
    <div class="container">
      <p class="crumbs"><a href="index.html">Home</a> / Register</p>

      <div class="reg-hero mt-3">
        <div>
          <span class="free-badge">{ico("check")} Free of charge</span>
          <h1 class="mt-2">Africa's Hardware Revolution</h1>
          <p class="theme-line" style="font-family:var(--font-display);font-weight:600;font-size:clamp(1rem,2.2vw,1.35rem);color:var(--accent);margin-top:.5rem">From Spark to Ignition</p>
          {date_plate("when-plate--lg")}
          <p class="lede">A one-day conference, then three weeks on the bench. Free, at UNN Nsukka, open
            to anyone who wants to build.</p>
          <div class="callout mt-3">{ico("pin")}<span><strong>This run is at UNN Nsukka in
            {EVENT_MONTH}.</strong> We will send you the exact dates and the venue as soon as they are
            fixed. Other South-East universities are next — at least one per state.</span></div>
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
        <span class="eyebrow">{ico("calendar")} Three acts, one programme &middot; {EVENT_MONTH}</span>
        <h2>{PROGRAMME_LINE}</h2>
        <p class="lede">One registration covers all three. Tick only what you want.</p>
      </div>
{events_html}
    </div>
  </section>

  <section class="section" id="covers">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow">{ico("layers")} What the bootcamp covers</span>
        <h2>Eleven tracks, three weeks, no fee</h2>
        <p class="lede">Pick nothing before you arrive. The bootcamp runs across all of it, and you go
          deeper on whatever grips you.</p>
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
        <p class="lede">The last three questions matter most. We read every one and shape the sessions
          around the answers.</p>
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
              <label><input type="checkbox" name="events" value="Conference" checked><span>Conference (one day, opens it)</span></label>
              <label><input type="checkbox" name="events" value="Bootcamp" checked><span>Bootcamp (three weeks)</span></label>
              <label><input type="checkbox" name="events" value="Hackathon" checked><span>Hackathon (closes the bootcamp)</span></label>
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
        <p class="form-note">Free. Your answers shape the sessions and let us send you dates. Nothing
          else, and we pass them on to nobody.</p>
      </form>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="cta-band bracketed reveal">
        {mg_circuit("cta-circuit")}
        <span class="eyebrow">{ico("users")} Questions first?</span>
        <h2 class="mt-2">Ask before you sign up</h2>
        <p>Fastest way to reach us — dates, what to bring, anything.</p>
        <div class="hero-cta">
          <a class="btn btn--primary btn--lg" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("wa")} Ask on WhatsApp</a>
          <a class="btn btn--ghost btn--lg" href="contact.html">Contact us {ico("arrow")}</a>
        </div>
      </div>
    </div>
  </section>

'''
    write("register.html", f"Register — Free Conference &amp; 3-Week Hardware Bootcamp — {ORG}",
          "Register free for Africa's Hardware Revolution: From Spark to Ignition — a one-day hardware conference at UNN Nsukka this November, followed by a free three-week bootcamp in robotics, embedded systems, IoT, PCB design, CAD, edge AI and 3D printing. Exact dates and venue announced soon.",
          body)


def main():
    print("Building site…")
    build_home(); build_about(); build_programs(); build_projects(); build_community(); build_register(); build_contact()
    print("Done.")

if __name__ == "__main__":
    main()
