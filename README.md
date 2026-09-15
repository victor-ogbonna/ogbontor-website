# Ogbontor Engineering Enterprise — website

A dependency-free static site. No build step is required to deploy it: the `.html` files
in this folder are the site.

Rebranded from the earlier **Embedded Systems and Robotics Nigeria (ESR-Nigeria)** identity —
all copy, metadata and structured data now read **Ogbontor Engineering Enterprise**.

---

## Run it locally

```bash
python3 -m http.server 8099
```

Then open <http://localhost:8099>.

## Publishing to GitHub

The repository is initialised, committed on `main`, and the remote is already set to
`git@github.com:victor-ogbonna/ogbontor-website.git`. SSH from this machine is authenticated as
**victor-ogbonna**.

**The repo does not exist on GitHub yet** — create it first (it cannot be created from here without
the GitHub CLI or a token):

1. Go to <https://github.com/new>
2. Repository name: **`ogbontor-website`**
3. Leave it **empty** — no README, no .gitignore, no licence (the commit already has them)
4. Create, then run:

```bash
cd "/home/victorogbonna313/ogbontor website" && git push -u origin main
```

### Free hosting from that repo

GitHub Pages will serve this site as-is, since there is no build step:
**Settings -> Pages -> Source: Deploy from a branch -> `main` / `root`.**
It appears at `https://victor-ogbonna.github.io/ogbontor-website/`, and a custom domain can be
pointed at it from the same screen.

---

## Deploy

Upload the whole folder to any static host — Netlify, Vercel, GitHub Pages, Cloudflare
Pages, or ordinary cPanel hosting. There is nothing to compile and no server code.

Before going live, set your real domain in three places:

| Where | What to change |
|---|---|
| `tools/build.py` | `SITE_URL` (used for canonical URLs, Open Graph and JSON-LD) |
| `robots.txt` | the `Sitemap:` line |
| `sitemap.xml` | every `<loc>` |

Then re-run `python3 tools/build.py`.

---

## Structure

```
index.html      Home — hero carousel, bootcamp banner, portfolio companies, sponsorship
register.html   Free-bootcamp registration form (posts to your Google Sheet)
about.html      Mission, the problem, objectives, leadership
programs.html   Bootcamps, the 19-module curriculum, SIWES/IT placements, R&D, membership
projects.html   13 projects (completed + pending), Afro-Joint feature, photo gallery
community.html  Build nights, mentorship, code of conduct, FAQ
contact.html    Contact form, company details, partnership options
404.html        Not-found page

assets/css/styles.css   Whole design system — one file, CSS custom properties
assets/js/main.js       Theme toggle, mobile nav, reveals, counters, lightbox, form
assets/img/             Logo, favicon, OG image, photos, placeholders
tools/build.py          Regenerates the six pages from shared partials
```

### Editing content

Two options, both fine:

1. **Edit the `.html` files directly.** They are plain HTML. This is the simplest route
   for a copy tweak.
2. **Edit `tools/build.py` and re-run it.** Use this when changing something that appears
   on every page — the header, the footer, contact details, the nav. Note that running the
   script **overwrites** the six generated pages, so do not mix the two approaches on the
   same content.

Contact details, the WhatsApp link, the RC number and the address all live at the top of
`tools/build.py` as constants.

---

## Images

Photographs come from the original Behance project gallery. Each one was matched to its
project using Behance's own module order, then **confirmed by viewing it at full size** — the
filenames now describe what the photo actually shows (`walking-stick-field-1.jpg`,
`solar-finished-product.jpg`, and so on).

The four bootcamp photos originally had an **"Embedded Systems and Robotics Nigeria
(ESR-Nigeria)" caption bar burned into the image**. That bar has been cropped off all four.

### Projects without a photo

Four projects have no usable still image and use a blue SVG placeholder in
`assets/img/placeholders/`. Drop a real photo in and update the `src` in `tools/build.py`:

| Placeholder | Project | Why |
|---|---|---|
| `line-following-robot.svg` | Line Following Robot | Behance had video only, no still |
| `autonomous-vehicle.svg` | Autonomous Self-Driving Vehicle | Pending — not built yet |
| `cng-protect.svg` | CNG Protect | Pending — not built yet |
| `ecg-system.svg` | Smart ECG System | Pending — not built yet |

### Real assets now in place

| File | What it is |
|---|---|
| `assets/img/logo.png`, `favicon.png` | The Ogbontor mark |
| `assets/img/africa-circuit.png` | Africa-as-circuit-board graphic (transparent PNG) on both bootcamp banners |
| `assets/img/whatsapp-qr.png` | Branded WhatsApp community QR, on the community page |
| `assets/img/team/founder.jpg` | Founder portrait on the about page |
| `assets/img/companies/joint-agent.png`, `cng-protect.jpg` | Portfolio company logos |
| `assets/img/gallery/solar-build-process.jpg` | Replaced with the higher-quality build photo |

### Still placeholders

The only ones left:

| File | What it needs |
|---|---|
| `assets/img/partners/partner-*.svg` | Partner and sponsor logos. |

`assets/img/legacy/` holds the old ESR-Nigeria logo and QR code. They are not referenced by
any page — kept only for reference. Delete the folder when you no longer want them.

The social preview image `assets/img/og-image.png` matches the blue brand. Regenerate or replace
it if the logo or headline changes.

---

## Videos

Two clips, both in `assets/video/`.

### `3d-printer.mp4` — the equipment highlight (home page)

8.9 seconds, 1.3 MB. **Filmed sideways, corrected by rotating it 90 degrees anticlockwise.**
The fix is metadata-only: the rotation matrix in the file's `tkhd` box was rewritten, so browsers
present it as **850x478 landscape**. No re-encoding, no quality loss. That is exactly 16:9, so it
fills the stage edge to edge.

This one *does* autoplay — it is the highlight of the section — but it is muted, looped and
inline, so it is cheap.

### `line-following-robot.mp4` — project #1 (projects page)

7.9 seconds, 1.9 MB, 720x1280 portrait. This one is genuinely portrait, filmed upright, and needs
no rotation. It sits in the first project card, which is otherwise identical in size to every
other card.

**It does not slow the page down.** The video carries `preload="none"`, which means the browser
downloads *nothing* until a visitor presses play. Measured on a fresh load of `projects.html`:

| | |
|---|---|
| Total transferred on load | **55 KB** |
| Requests for the 1.9 MB video | **0** |
| Cost of the video card | 23 KB (its poster image) |

The 1.9 MB is only fetched when someone actually clicks play — confirmed by watching the network
log before and after.

The poster (`assets/img/line-following-poster.jpg`) was captured from the clip itself by sampling
frames and keeping the brightest one, since the opening second is almost black. It doubles as the
blurred backdrop behind the portrait video, so it costs nothing extra.

### Replacing or rotating a clip

```bash
ffmpeg -i input.mp4 -vf "transpose=2" -c:a copy assets/video/3d-printer.mp4
```

(`transpose=2` anticlockwise, `transpose=1` clockwise.) ffmpeg is not installed on this machine,
which is why the rotation above was done via metadata instead.

The original unrotated 3D-printer file is in the session scratchpad as `3d-printer.backup.mp4`.
`assets/3d printing.mp4` is the untouched source you supplied.

---

## Logo

`assets/OGBONTOR_logo.png` is the original supplied file (navy disc, gold outline, OGBONTOR
wordmark beneath). Two derivatives are generated from it and used by the site:

| File | What it is | Used for |
|---|---|---|
| `assets/img/logo.png` | The circular mark alone, wordmark cropped off, squared | Header and footer |
| `assets/img/favicon.png` | Same mark at 180x180 | Browser tab, Apple touch icon |
| `assets/img/logo-full.png` | The complete lock-up, mark + wordmark | Spare, not currently referenced |

The white page behind the mark was knocked out to transparency, so it sits correctly on both the
white and the dark-navy theme. On the dark theme the mark also gets a hairline white ring, because
the navy disc would otherwise sit too close to the dark background to read. The header pairs the mark with live **OGBONTOR** text, which is
why the wordmark is cropped out of `logo.png` — otherwise the name would appear twice.

To change the logo, replace the source PNG and re-run the crop, or just overwrite
`assets/img/logo.png` and `assets/img/favicon.png` directly.

---

---

## Registration -> Google Sheet

**This is live and verified.** The form on `register.html` posts into your Google Sheet through the
Apps Script web app; the endpoint is already set in `REGISTER_ENDPOINT`.

Verified end to end on 15 Sep 2026: `doPost` returned `{"result":"ok"}` (HTTP 200) and a full form
submission cleared and confirmed.

> **Delete the test rows.** Verification wrote rows named `TEST ROW - please delete`,
> `E2E TEST - please delete` and `E2E FORM TEST - please delete`.

### A note on speed

Apps Script **cold starts are slow** — the first call measured **36 seconds**; warm calls settle
around **8 seconds**. The form is built for that:

- 60-second timeout, so a cold start is never aborted mid-flight
- a "still sending…" message after 6 seconds so nobody thinks it has hung
- if the response cannot be read, one fire-and-forget `no-cors` retry (the row still lands)
- only if that fails does it fall back to opening the visitor's email client

### What gets captured

Name, email, phone, status, institution, course, **which events they are attending**, tracks of
interest, skill level, and the three questions:

- **What can you already do?** (present skill set)
- **What engineering or tech challenge are you facing right now?**
- **What do you hope to learn here?**

Plus a timestamp and source hostname.

### If you edit the script

Apps Script keeps serving the old code until you redeploy: **Deploy -> Manage deployments ->
Edit (pencil) -> Version: New version -> Deploy.** The URL stays the same.

---

## The three events

The programme is a bootcamp, a hackathon inside it, and a one-day conference afterwards. All three
are described on `register.html`, and the form asks which the person is attending (at least one is
required — enforced in JS, since HTML cannot mark a checkbox group required).

Edit them in `EVENTS` in `tools/build.py`. **Hackathon prizes are described as "to be revealed"** —
set the real ones there when you have them.

---

## Portfolio companies

Linked from the home page (`#portfolio`):

| Company | Link | Logo |
|---|---|---|
| Joint-Agent IDE | jointagentide.com | `assets/img/companies/joint-agent.svg` — **placeholder** |
| CNG Protect | cngprotect.com | `assets/img/companies/cng-protect.svg` — **placeholder** |

Both logos are placeholders. Drop real files in and update the `src`, or edit `PORTFOLIO` in
`tools/build.py` to change names, domains or descriptions.

---

## Two things that need your input

### The registration number is gone

Every mention of the old RC number has been removed — footer, contact page, about page, and the
structured data. Send me the correct one and I will put it back. Until then the site says
"Registered in Nigeria" without a number.

### "First in Africa" was left out — deliberately

You asked me to add *first in Africa* to the electric motor manufacturing, manned aircraft and
microchip R&D lines **if correct**. I did not add it, because as written it is very unlikely to
stand up:

- **Electric motor manufacturing** — already happens in Africa commercially (Egypt, South Africa,
  Nigeria among others).
- **Manned aircraft manufacturing** — South Africa has built manned aircraft for decades
  (Denel, AHRLAC/Mwari).
- **Microchip technology** — there is existing semiconductor design activity across the continent.

A false superlative on a company site is the kind of thing a sponsor, journalist or university
partner checks, and it would cost you more credibility than it buys. The R&D section is written to
be genuinely ambitious without the claim.

If you have a **narrower** claim that is true, it will be both safer and more impressive — e.g.
"the first student-led hardware lab in Eastern Nigeria to prototype X". Send me the exact wording
and I will add it.

---

## Colours

Blue and white. The palette lives entirely in CSS custom properties at the top of
`assets/css/styles.css`:

| Token | Value | Role |
|---|---|---|
| `--accent` | `#0B57D0` | Primary blue — buttons, links, headings |
| `--accent-hi` | `#2E7BF6` | Lighter blue for gradients |
| `--accent-deep` | `#063A93` | Deep blue, gradient end |
| `--cyan` | `#0A8FB3` | Circuit-trace accent, used sparingly |

`#0B57D0` was chosen as a deep, saturated engineering blue — it reads technical rather than
corporate, echoes the blue of the original ESR robot mark, and clears WCAG AA contrast on white
for both text and white-on-blue buttons.

**Light (blue on white) is the default theme for every visitor.** Dark mode is a deep-navy
variant of the same blue, available via the header toggle and remembered per browser. The site
deliberately does *not* auto-switch to dark on a system preference, so the blue-and-white brand
is what people see first.

---

## Before you publish — things to set

These are placeholders or assumptions, deliberately flagged rather than invented:

- **Membership levels** (`programs.html`) — the three tiers are structural. Set real terms and
  any fees before publishing.
- **Build-night schedule** (`community.html`) — replace the callout with your real day, time
  and venue, plus current cohort dates.
- **Leadership names** (`about.html`) — all six read "Your Name Here".
- **Email address** — the site uses `victorogbonna313@gmail.com`. Change `EMAIL` in
  `tools/build.py` if you move to a dedicated Ogbontor address.
- **Bootcamp details** — the free UNN bootcamp is announced on the home and programs pages under
  the theme *Africa's Hardware Revolution — From Spark to Ignition*, but **no date or venue is
  given**. Add them before publishing.
- **The 800-attendee event** — described as planned, not as something that has happened. Keep that
  framing until it has.
- **Membership numbers** — the stat band deliberately shows only verifiable figures (projects,
  modules, tiers, lab). Add a member count once you have a firm one.
- **Project count** — 13 projects, taken from the Behance list (items 1–10 plus the three in
  development; item 6, the robotic arm, is flagged "in progress" there). Completed ones are
  badged **Completed**; the rest are badged **Pending**, with no count given for how many are
  pending. Add or promote projects in `PROJECTS_BUILT` / `PROJECTS_WIP` in `tools/build.py`.
- **Concept imagery** — the "Made in Enugu" and vision images are illustrative renders, and are
  labelled as such on the page. Keep that label, or swap in photographs of real facilities.

## Contact form

The form composes an email in the visitor's own mail client — nothing is sent to a server, so
there is no backend to run and no data stored. To collect submissions directly instead, point
the `<form>` at a service such as Formspree or Netlify Forms and remove the `data-mailto`
attribute (the handler lives in `assets/js/main.js`).

---

## Notes

- **Themes** — dark and light are both fully defined. The site follows the visitor's system
  preference and remembers an explicit choice in `localStorage`.
- **Accessibility** — skip link, labelled controls, keyboard-operable gallery, visible focus
  rings, one `<h1>` per page, no skipped heading levels, and `prefers-reduced-motion` honoured.
- **SEO** — per-page titles and descriptions, canonical URLs, Open Graph and Twitter cards,
  `Organization`/`EducationalOrganization` JSON-LD, `sitemap.xml` and `robots.txt`.
