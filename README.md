# NBRinfo.com — Nordschleife Public Driving Days

A static GitHub Pages website for Nürburgring Nordschleife enthusiasts.

## Features

- **Interactive Track Map** — SVG Nordschleife with 125 labeled corners, 7 segments, slider-driven car animation
- **Timetable** — 2026 Touristenfahrten public driving dates
- **Live Cams** — Embedded Nordschleife entrance webcam
- **Track Status** — Auto-fetched status with color-coded page frame (green/yellow/red)

## Tech Stack

- Pure HTML5 + Tailwind CSS (CDN) + vanilla JavaScript
- Zero build step, zero dependencies
- Mobile-first, dark racing theme

## Deploy to GitHub Pages

```bash
# 1. Create GitHub repo
gh repo create nbrinfo.com --public --source=. --push

# 2. Enable Pages: Settings → Pages → Source: main branch, / (root)

# 3. Custom domain: Settings → Pages → Custom domain: NBRinfo.com
#    Then add DNS records:
#    A     @    185.199.108.153
#    A     @    185.199.109.153
#    A     @    185.199.110.153
#    A     @    185.199.111.153
#    CNAME www  <username>.github.io
```

The `CNAME` file is already included for the custom domain.

## File Structure

```
nbrinfo.com/
├── index.html          # Complete single-page app
├── CNAME               # GitHub Pages custom domain
├── README.md
└── assets/
    └── favicon.svg     # Site favicon
```

## Disclaimer

For enthusiasts only. Not affiliated with Nürburgring GmbH. Always verify dates on [nuerburgring.de](https://nuerburgring.de/open-hours) before travelling.
