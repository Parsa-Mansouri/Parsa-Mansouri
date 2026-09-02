"""Generates the SVG assets for the ParSaMnSS profile README.
Run: python3 build.py   (writes the SVGs next to this file)
"""
from pathlib import Path

OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True)

NAVY = "#0B1730"      # card / banner background
NAVY_2 = "#06101F"    # deeper edge of gradient
LINE = "#1C2B4A"      # hairlines
ACCENT = "#3D7BFF"    # Kagu electric blue
ACCENT_2 = "#7FB0FF"
TEXT = "#F2F5FA"
MUTED = "#8A99B8"
DIM = "#5C6C8C"

SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"


def bg(w, h, r=16, gid="g"):
    return f"""
  <defs>
    <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{NAVY}"/>
      <stop offset="1" stop-color="{NAVY_2}"/>
    </linearGradient>
    <radialGradient id="{gid}-glow" cx="0.85" cy="0.1" r="0.7">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.28"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="{gid}-clip"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>
  </defs>
  <rect width="{w}" height="{h}" rx="{r}" fill="url(#{gid})"/>
  <rect width="{w}" height="{h}" rx="{r}" fill="url(#{gid}-glow)"/>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{LINE}"/>"""


def grid(w, h, gid, step=40):
    # faint dot grid, clipped to the rounded rect
    dots = []
    for x in range(step, w, step):
        for y in range(step, h, step):
            dots.append(f'<circle cx="{x}" cy="{y}" r="1" />')
    return f'<g clip-path="url(#{gid}-clip)" fill="{DIM}" fill-opacity="0.35">{"".join(dots)}</g>'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- header
def header():
    w, h = 1200, 400
    label_y = 92
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Parsa Mansouri, co-founder of Kagu Software">
  {bg(w, h, 20, "hd")}
  {grid(w, h, "hd", 48)}

  <!-- Kagu logo, traced from the brand mark -->
  <g transform="translate(870 140) scale(0.3) translate(-130 -370)">
    <!-- lower body -->
    <path d="M620 670 H800 L975 830 H830 Q790 830 765 805 L620 670 Z" fill="{ACCENT}" fill-opacity="0.75"/>
    <!-- tail band -->
    <polygon points="225,505 450,505 660,710 440,710" fill="{ACCENT_2}" fill-opacity="0.85"/>
    <!-- tail tip -->
    <polygon points="225,505 130,610 330,610" fill="{ACCENT}"/>
    <!-- wing -->
    <path d="M860 370 H1130 L765 710 H465 L800 395 Q825 370 860 370 Z" fill="{TEXT}"/>
  </g>

  <!-- mono label -->
  <text x="72" y="{label_y}" font-family="{MONO}" font-size="13" letter-spacing="3.5" fill="{MUTED}">
    <tspan>CO-FOUNDER · KAGU SOFTWARE</tspan>
    <tspan fill="{DIM}"> · </tspan>
    <tspan>ISTANBUL</tspan>
  </text>

  <!-- headline -->
  <text x="66" y="215" font-family="{SANS}" font-weight="800" font-size="118" letter-spacing="-4" fill="{TEXT}">PARSA</text>
  <text x="66" y="318" font-family="{SANS}" font-weight="800" font-size="118" letter-spacing="-4" fill="{ACCENT}">MANSOURI</text>

  <!-- accent underline that draws in -->
  <line x1="72" y1="342" x2="72" y2="342" stroke="{ACCENT}" stroke-width="4" stroke-linecap="round">
    <animate attributeName="x2" from="72" to="372" dur="0.9s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.1 1"/>
  </line>

  <!-- right-side one-liner -->
  <g font-family="{SANS}" font-size="17" fill="{MUTED}">
    <text x="905" y="320">I build operator software for</text>
    <text x="905" y="346">small businesses — and ship it.</text>
  </g>
</svg>
"""


# ---------------------------------------------------------------- stats strip
def stats():
    w, h = 1200, 120
    items = [
        ("40+", "REPOS SHIPPED", "under the Kagu org"),
        ("1.4K+", "CONTRIBUTIONS", "in 2026 so far"),
        ("30+", "LIVE DEPLOYMENTS", "clients & products on Vercel"),
        ("TS", "PRIMARY LANGUAGE", "Next.js · React Native · Supabase"),
    ]
    cell = w / len(items)
    cells = []
    for i, (big, label, sub) in enumerate(items):
        x = i * cell
        sep = f'<line x1="{x:.0f}" y1="24" x2="{x:.0f}" y2="{h-24}" stroke="{LINE}"/>' if i else ""
        cells.append(f"""
  {sep}
  <rect x="{x+28:.0f}" y="36" width="3" height="48" rx="1.5" fill="{ACCENT}"/>
  <text x="{x+46:.0f}" y="66" font-family="{SANS}" font-weight="800" font-size="34" letter-spacing="-1" fill="{TEXT}">{esc(big)}</text>
  <text x="{x+46:.0f}" y="88" font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{ACCENT_2}">{esc(label)}</text>
  <text x="{x+46+ (len(big)*20 if len(big)<5 else 100):.0f}" y="66" font-family="{SANS}" font-size="13" fill="{MUTED}"></text>
  <text x="{x+46:.0f}" y="106" font-family="{SANS}" font-size="12" fill="{DIM}">{esc(sub)}</text>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Key numbers">
  {bg(w, h, 16, "st")}
  {"".join(cells)}
</svg>
"""


# ---------------------------------------------------------------- project cards
def card(slug, index, kind, title, lines, chips, link_label, live=None):
    w, h = 590, 250
    chip_x = 30
    chip_svg = []
    for c in chips:
        cw = 14 + len(c) * 7.4
        chip_svg.append(f"""
  <rect x="{chip_x:.0f}" y="188" width="{cw:.0f}" height="26" rx="6" fill="{ACCENT}" fill-opacity="0.10" stroke="{ACCENT}" stroke-opacity="0.35"/>
  <text x="{chip_x+cw/2:.0f}" y="205" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{ACCENT_2}">{esc(c)}</text>""")
        chip_x += cw + 8
    body = "".join(
        f'<text x="30" y="{112 + i*22}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{esc(l)}</text>'
        for i, l in enumerate(lines)
    )
    live_svg = ""
    if live:
        live_svg = f"""
  <g font-family="{MONO}" font-size="11" letter-spacing="2">
    <circle cx="{w-30-len(live)*7.2-16:.0f}" cy="49" r="3.5" fill="#3DDC97">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <text x="{w-30:.0f}" y="53" text-anchor="end" fill="#3DDC97">{esc(live)}</text>
  </g>"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  {bg(w, h, 16, "c"+slug)}
  <rect x="0" y="0" width="5" height="{h}" fill="{ACCENT}" clip-path="url(#c{slug}-clip)"/>
  <text x="30" y="53" font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{ACCENT_2}">{index}  /  {esc(kind)}</text>{live_svg}
  <text x="30" y="86" font-family="{SANS}" font-weight="700" font-size="24" letter-spacing="-0.5" fill="{TEXT}">{esc(title)}</text>
  {body}
  {"".join(chip_svg)}
  <text x="{w-30}" y="206" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{MUTED}">{esc(link_label)}  →</text>
</svg>
"""
    (OUT / f"card-{slug}.svg").write_text(svg)


def build():
    (OUT / "header.svg").write_text(header())
    (OUT / "stats.svg").write_text(stats())

    card("touchpadel", "01", "VENUE SYSTEM", "Touch Padel",
         ["Full system for a padel club in Iraq: guest booking app,",
          "public site with QR café ordering, and a Windows operator",
          "app (till · desk · kitchen · stock) on one Postgres. EN/AR,",
          "full RTL, keeps working when the venue's internet drops."],
         ["Next.js", "React Native", "Supabase", "PostHog"], "VIEW REPO", live="LIVE")

    card("kaguos", "02", "INTERNAL OPS", "KaguOS",
         ["The system Kagu runs itself on — clients, projects,",
          "delivery and the day-to-day of the company in one place.",
          "Built the same way we build for clients: fast, boring",
          "stack, deployed continuously."],
         ["Next.js", "Supabase", "Vercel"], "VIEW REPO", live="LIVE")

    card("upperdeck", "03", "CLIENT · HOSPITALITY", "UpperDeck",
         ["Digital menu and website for UpperDeck, an American",
          "diner in Beşiktaş, Istanbul. Kagu also runs the diner's",
          "paid social on Meta and TikTok — so the site is built",
          "for walk-ins, not just for looks."],
         ["Next.js", "Vercel", "Meta Ads"], "upperdeckk.com", live="LIVE")

    card("turkcure", "04", "CLIENT · HEALTH TOURISM", "TurkCure Ops",
         ["Internal operations system for a health-tourism team:",
          "the patient pipeline from lead to aftercare, plus the",
          "providers behind it — doctors, hospitals, partners —",
          "in one back office instead of spreadsheets."],
         ["Next.js", "Supabase", "TypeScript"], "VIEW REPO", live="LIVE")


if __name__ == "__main__":
    build()
    for p in sorted(OUT.glob("*.svg")):
        print(p.name, p.stat().st_size)
