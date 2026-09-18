"""Generates every SVG asset for the Parsa-Mansouri profile README.
Run: python3 build.py   (writes the SVGs next to this file)
All assets are hand-written SVG. No third-party stat widgets, no images.
"""
from pathlib import Path

OUT = Path(__file__).parent

# ---------------------------------------------------------------- tokens
NAVY    = "#0B1730"
NAVY_2  = "#060D1B"
INK     = "#040913"
LINE    = "#1C2B4A"
ACCENT  = "#3D7BFF"
ACCENT2 = "#7FB0FF"
ACCENT3 = "#1B3E7A"
TEXT    = "#F2F5FA"
MUTED   = "#8A99B8"
DIM     = "#5C6C8C"
GREEN   = "#3DDC97"
AMBER   = "#FFC46B"
PINK    = "#FF7AB6"

SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', 'JetBrains Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# Live contribution data. refresh.py rewrites data.json from my public calendar
# once a day and re-runs this file, so the graph below is never stale.
import json
from datetime import date, datetime, timedelta

_D = json.loads((OUT / "data.json").read_text())
LEVELS      = _D["levels"]
TOTAL_YEAR  = _D["total_year"]
FIRST_DATE  = datetime.strptime(_D["first_date"], "%Y-%m-%d").date()
THIS_MONTH  = str(_D["this_month"])
STREAK      = str(_D["streak"])
ACTIVE      = str(_D["active"])


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def panel(w, h, r=18, gid="g", glow_x=0.85, glow_y=0.1):
    """Shared dark panel: gradient fill, accent glow, hairline border, clip path."""
    return f"""<defs>
<linearGradient id="{gid}-bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY_2}"/>
</linearGradient>
<radialGradient id="{gid}-glow" cx="{glow_x}" cy="{glow_y}" r="0.75">
<stop offset="0" stop-color="{ACCENT}" stop-opacity="0.30"/>
<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
</radialGradient>
<clipPath id="{gid}-clip"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>
</defs>
<rect width="{w}" height="{h}" rx="{r}" fill="url(#{gid}-bg)"/>
<rect width="{w}" height="{h}" rx="{r}" fill="url(#{gid}-glow)"/>"""


def border(w, h, r=18):
    return f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{LINE}"/>'


def dotgrid(w, h, gid, step=44, drift=True):
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1"/>'
        for x in range(0, w + step, step)
        for y in range(0, h + step, step)
    )
    anim = ""
    if drift:
        anim = (f'<animateTransform attributeName="transform" type="translate" '
                f'values="0 0; {step} {step}" dur="14s" repeatCount="indefinite"/>')
    return (f'<g clip-path="url(#{gid}-clip)"><g fill="{DIM}" fill-opacity="0.30" '
            f'transform="translate(-{step} -{step})">{dots}{anim}</g></g>')


def sweep(w, h, gid, dur="7s", begin="0s"):
    """Diagonal light sweep that runs across the panel forever."""
    return f"""<g clip-path="url(#{gid}-clip)">
<g transform="translate(-{w} 0)">
<rect x="0" y="-{h}" width="150" height="{h*3}" fill="url(#{gid}-sweep)" transform="rotate(18)"/>
<animateTransform attributeName="transform" type="translate" from="-{w*0.6} 0" to="{w*1.4} 0"
 dur="{dur}" begin="{begin}" repeatCount="indefinite"/>
</g></g>"""


def sweep_def(gid):
    return f"""<linearGradient id="{gid}-sweep" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#ffffff" stop-opacity="0"/>
<stop offset="0.5" stop-color="#ffffff" stop-opacity="0.055"/>
<stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>"""


def rise(delay, dy=22, dur="0.7s"):
    """Fade + slide up, then hold."""
    return (f'<animate attributeName="opacity" from="0" to="1" dur="{dur}" begin="{delay}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" '
            f'dur="{dur}" begin="{delay}s" fill="freeze" calcMode="spline" '
            f'keySplines="0.16 1 0.3 1" keyTimes="0;1"/>')


KAGU_MARK = f"""<g>
<path d="M620 670 H800 L975 830 H830 Q790 830 765 805 L620 670 Z" fill="{ACCENT}" fill-opacity="0.75"/>
<polygon points="225,505 450,505 660,710 440,710" fill="{ACCENT2}" fill-opacity="0.85"/>
<polygon points="225,505 130,610 330,610" fill="{ACCENT}"/>
<path d="M860 370 H1130 L765 710 H465 L800 395 Q825 370 860 370 Z" fill="{TEXT}"/>
</g>"""


# ---------------------------------------------------------------- 1. hero
def header():
    w, h = 1200, 440
    gid = "hd"
    type_line = "building software that runs real businesses."
    type_w = len(type_line) * 9.55
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Parsa Mansouri, co-founder of Kagu Software, Istanbul">
{panel(w, h, 22, gid)}
<defs>
{sweep_def(gid)}
<linearGradient id="{gid}-name" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{ACCENT}"/><stop offset="0.55" stop-color="{ACCENT2}"/><stop offset="1" stop-color="{ACCENT}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0; 1 0; -1 0" dur="9s" repeatCount="indefinite"/>
</linearGradient>
<clipPath id="{gid}-type"><rect x="70" y="352" width="0" height="30">
<animate attributeName="width" values="0;{type_w:.0f}" dur="2.6s" begin="1.1s" fill="freeze" calcMode="linear"/>
</rect></clipPath>
</defs>
{dotgrid(w, h, gid, 46)}
{sweep(w, h, gid)}

<g clip-path="url(#{gid}-clip)" opacity="0.5">
<line x1="0" y1="{h-1}" x2="{w}" y2="{h-1}" stroke="{ACCENT}" stroke-width="2"/>
</g>

<g transform="translate(900 118) scale(0.255) translate(-130 -370)" opacity="0">
{KAGU_MARK}
<animate attributeName="opacity" from="0" to="1" dur="1.1s" begin="0.45s" fill="freeze"/>
</g>

<g opacity="0">
<text x="72" y="96" font-family="{MONO}" font-size="12.5" letter-spacing="4" fill="{MUTED}">CO-FOUNDER
<tspan fill="{DIM}"> / </tspan><tspan fill="{ACCENT2}">KAGU SOFTWARE</tspan><tspan fill="{DIM}"> / </tspan>ISTANBUL</text>
{rise(0.15, 14)}
</g>

<g opacity="0">
<text x="66" y="222" font-family="{SANS}" font-weight="800" font-size="126" letter-spacing="-5" fill="{TEXT}">PARSA</text>
{rise(0.3)}
</g>
<g opacity="0">
<text x="66" y="330" font-family="{SANS}" font-weight="800" font-size="126" letter-spacing="-5" fill="url(#{gid}-name)">MANSOURI</text>
{rise(0.45)}
</g>

<g clip-path="url(#{gid}-type)">
<text x="70" y="376" font-family="{MONO}" font-size="16" fill="{MUTED}">{esc(type_line)}</text>
</g>
<rect x="{70+type_w:.0f}" y="360" width="9" height="19" fill="{ACCENT}" opacity="0">
<animate attributeName="opacity" values="0;1" dur="0.1s" begin="3.7s" fill="freeze"/>
<animate attributeName="opacity" values="1;1;0;0;1" dur="1.1s" begin="3.8s" repeatCount="indefinite"/>
</rect>

<g opacity="0">
<g font-family="{MONO}" font-size="12" letter-spacing="1.5">
<circle cx="908" cy="288" r="4" fill="{GREEN}">
<animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite"/>
</circle>
<circle cx="908" cy="288" r="4" fill="none" stroke="{GREEN}" stroke-width="1.5">
<animate attributeName="r" values="4;13" dur="2.4s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0.7;0" dur="2.4s" repeatCount="indefinite"/>
</circle>
<text x="924" y="292" fill="{GREEN}">SHIPPING TODAY</text>
</g>
<g font-family="{SANS}" font-size="16.5" fill="{MUTED}">
<text x="906" y="334">Booking systems, back office platforms</text>
<text x="906" y="358">and the sites in front of them.</text>
</g>
{rise(0.75, 16)}
</g>
</svg>
"""


# ---------------------------------------------------------------- 2. numbers
def stats():
    w, h = 1200, 132
    gid = "st"
    items = [
        (TOTAL_YEAR, "IN THE LAST YEAR", "commits, reviews, issues, PRs"),
        ("40+", "REPOS SHIPPED", "across the Kagu org"),
        ("30+", "LIVE DEPLOYMENTS", "clients and products, in production"),
        (THIS_MONTH, "CONTRIBUTIONS", date.today().strftime("so far in %B %Y")),
    ]
    cell = w / len(items)
    out = []
    for i, (big, label, sub) in enumerate(items):
        x = i * cell
        sep = (f'<line x1="{x:.0f}" y1="26" x2="{x:.0f}" y2="{h-26}" stroke="{LINE}"/>') if i else ""
        out.append(f"""{sep}
<g opacity="0">
<rect x="{x+30:.0f}" y="40" width="3" height="0" rx="1.5" fill="{ACCENT}">
<animate attributeName="height" from="0" to="52" dur="0.6s" begin="{0.2+i*0.12}s" fill="freeze"/>
</rect>
<text x="{x+48:.0f}" y="72" font-family="{SANS}" font-weight="800" font-size="36" letter-spacing="-1.4" fill="{TEXT}">{esc(big)}</text>
<text x="{x+48:.0f}" y="94" font-family="{MONO}" font-size="10.5" letter-spacing="2.6" fill="{ACCENT2}">{esc(label)}</text>
<text x="{x+48:.0f}" y="112" font-family="{SANS}" font-size="12" fill="{DIM}">{esc(sub)}</text>
{rise(0.2+i*0.12, 12, "0.6s")}
</g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Key numbers">
{panel(w, h, 16, gid, 0.5, 0.0)}
<defs>{sweep_def(gid)}</defs>
{sweep(w, h, gid, "9s", "1s")}
{"".join(out)}
{border(w, h, 16)}
</svg>
"""


# ---------------------------------------------------------------- 3. heatmap
def heat():
    cellsz, gap = 15, 4
    step = cellsz + gap
    cols = (len(LEVELS) + 6) // 7
    grid_w = cols * step - gap
    w = 1200
    pad_x = 60
    grid_x = (w - grid_w) // 2
    top = 126
    h = top + 7 * step - gap + 58
    gid = "hm"
    fills = {0: "#101B31", 1: ACCENT3, 2: "#2A62C9", 3: ACCENT, 4: "#9CC6FF"}

    best = cur = 0
    for ch in LEVELS:
        cur = cur + 1 if ch != "0" else 0
        best = max(best, cur)
    active = sum(1 for ch in LEVELS if ch != "0")

    cells = []
    for i, ch in enumerate(LEVELS):
        lvl = int(ch)
        col, row = i // 7, i % 7
        x = grid_x + col * step
        y = top + row * step
        d = 0.25 + col * 0.016
        glow = f' filter="url(#{gid}-lit)"' if lvl >= 4 else ""
        cells.append(
            f'<rect x="{x}" y="{y}" width="{cellsz}" height="{cellsz}" rx="4" fill="{fills[lvl]}" opacity="0"{glow}>'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{d:.2f}s" fill="freeze"/></rect>'
        )

    mlabels, seen = [], set()
    for col in range(cols):
        d = FIRST_DATE + timedelta(days=col * 7)
        key = (d.year, d.month)
        if key in seen or (col and d.day > 7):
            continue
        seen.add(key)
        mlabels.append(
            f'<text x="{grid_x + col*step:.0f}" y="{top-14}" font-family="{MONO}" font-size="10" '
            f'letter-spacing="1.6" fill="{DIM}">{d.strftime("%b").upper()}</text>'
        )
    mlabels = "".join(mlabels)

    facts = [(STREAK, "DAY STREAK"), (ACTIVE, "ACTIVE DAYS"), (THIS_MONTH, "THIS MONTH")]
    fx = w - pad_x
    fact_svg = []
    for big, lab in reversed(facts):
        lw = max(len(big) * 19, len(lab) * 6.6)
        fx -= lw
        fact_svg.append(
            f'<text x="{fx+lw:.0f}" y="62" text-anchor="end" font-family="{SANS}" font-weight="800" '
            f'font-size="26" letter-spacing="-1" fill="{TEXT}">{big}</text>'
            f'<text x="{fx+lw:.0f}" y="82" text-anchor="end" font-family="{MONO}" font-size="9.5" '
            f'letter-spacing="2" fill="{ACCENT2}">{lab}</text>'
        )
        fx -= 42

    legend_x = w - pad_x - 152
    legend = "".join(
        f'<rect x="{legend_x + 36 + i*19}" y="{h-36}" width="13" height="13" rx="3.5" fill="{fills[i]}"/>'
        for i in range(5)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{TOTAL_YEAR} contributions in the last year">
{panel(w, h, 18, gid, 0.9, 0.05)}
<defs>
{sweep_def(gid)}
<filter id="{gid}-lit" x="-60%" y="-60%" width="220%" height="220%">
<feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
</defs>
{sweep(w, h, gid, "11s", "2s")}
<g opacity="0">
<text x="{pad_x}" y="48" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{ACCENT2}">THE RECEIPTS</text>
<text x="{pad_x}" y="80" font-family="{SANS}" font-weight="700" font-size="22" letter-spacing="-0.4" fill="{TEXT}">{TOTAL_YEAR} contributions in the last year</text>
{"".join(fact_svg)}
{rise(0.1, 10, "0.6s")}
</g>
<line x1="{pad_x}" y1="100" x2="{w-pad_x}" y2="100" stroke="{LINE}"/>
{mlabels}
{"".join(cells)}
<text x="{legend_x}" y="{h-26}" font-family="{MONO}" font-size="10.5" letter-spacing="1.8" fill="{DIM}">LESS</text>
{legend}
<text x="{legend_x + 143}" y="{h-26}" font-family="{MONO}" font-size="10.5" letter-spacing="1.8" fill="{DIM}">MORE</text>
<text x="{pad_x}" y="{h-26}" font-family="{MONO}" font-size="10.5" letter-spacing="1.8" fill="{DIM}">{FIRST_DATE.strftime("%b %Y").upper()} / {(FIRST_DATE + timedelta(days=len(LEVELS)-1)).strftime("%b %Y").upper()}</text>
{border(w, h, 18)}
</svg>
"""


# ---------------------------------------------------------------- 4. marquee
def stack():
    w, h = 1200, 128
    gid = "mq"
    row_a = ["TypeScript", "Next.js", "React", "React Native", "Expo", "Tailwind",
             "Supabase", "PostgreSQL", "Row Level Security", "Prisma", "tRPC", "Zod"]
    row_b = ["Vercel", "Turborepo", "pnpm", "Node.js", "Python", "Electron",
             "PostHog", "Stripe", "Meta Ads API", "Figma", "Git", "CI/CD"]

    def build_row(items, y, dur, reverse, accent):
        chips, x = [], 0
        for it in items:
            cw = 26 + len(it) * 7.9
            chips.append(f"""<g transform="translate({x:.0f} 0)">
<rect x="0" y="0" width="{cw:.0f}" height="38" rx="10" fill="{accent}" fill-opacity="0.09" stroke="{accent}" stroke-opacity="0.32"/>
<circle cx="14" cy="19" r="3" fill="{accent}"/>
<text x="{cw/2+7:.0f}" y="24" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{TEXT}" fill-opacity="0.92">{esc(it)}</text>
</g>""")
            x += cw + 14
        total = x
        inner = "".join(chips)
        frm, to = (f"-{total:.0f} 0", "0 0") if reverse else ("0 0", f"-{total:.0f} 0")
        return f"""<g transform="translate(0 {y})">
<g>
<animateTransform attributeName="transform" type="translate" from="{frm}" to="{to}" dur="{dur}" repeatCount="indefinite"/>
<g>{inner}</g><g transform="translate({total:.0f} 0)">{inner}</g><g transform="translate({total*2:.0f} 0)">{inner}</g>
</g></g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Tools and technologies">
{panel(w, h, 16, gid, 0.5, 0.5)}
<defs>
<linearGradient id="{gid}-fade" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{NAVY}" stop-opacity="1"/><stop offset="0.08" stop-color="{NAVY}" stop-opacity="0"/>
<stop offset="0.92" stop-color="{NAVY}" stop-opacity="0"/><stop offset="1" stop-color="{NAVY}" stop-opacity="1"/>
</linearGradient>
</defs>
<g clip-path="url(#{gid}-clip)">
{build_row(row_a, 16, "34s", False, ACCENT)}
{build_row(row_b, 72, "42s", True, ACCENT2)}
</g>
<rect width="{w}" height="{h}" rx="16" fill="url(#{gid}-fade)"/>
{border(w, h, 16)}
</svg>
"""


# ---------------------------------------------------------------- 5. cards
def card(slug, index, kind, title, lines, chips, link_label, live="LIVE"):
    w, h = 590, 268
    gid = "c" + slug
    chip_svg, cx = [], 30
    for c in chips:
        cw = 16 + len(c) * 7.5
        chip_svg.append(f"""<rect x="{cx:.0f}" y="204" width="{cw:.0f}" height="27" rx="7" fill="{ACCENT}" fill-opacity="0.10" stroke="{ACCENT}" stroke-opacity="0.34"/>
<text x="{cx+cw/2:.0f}" y="222" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{ACCENT2}">{esc(c)}</text>""")
        cx += cw + 9
    body = "".join(
        f'<text x="30" y="{122 + i*23}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{esc(l)}</text>'
        for i, l in enumerate(lines)
    )
    live_svg = f"""<g font-family="{MONO}" font-size="10.5" letter-spacing="2">
<circle cx="{w-30-len(live)*7.0-15:.0f}" cy="52" r="3.5" fill="{GREEN}">
<animate attributeName="opacity" values="1;0.2;1" dur="2.2s" repeatCount="indefinite"/></circle>
<text x="{w-30:.0f}" y="56" text-anchor="end" fill="{GREEN}">{esc(live)}</text></g>""" if live else ""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
{panel(w, h, 16, gid)}
<defs>{sweep_def(gid)}</defs>
{dotgrid(w, h, gid, 40, False)}
{sweep(w, h, gid, "8s", f"{0.4*int(index)}s")}
<rect x="0" y="0" width="5" height="{h}" fill="{ACCENT}" clip-path="url(#{gid}-clip)"/>
<text x="30" y="56" font-family="{MONO}" font-size="10.5" letter-spacing="2.6" fill="{ACCENT2}">{index} / {esc(kind)}</text>
{live_svg}
<text x="30" y="92" font-family="{SANS}" font-weight="700" font-size="25" letter-spacing="-0.6" fill="{TEXT}">{esc(title)}</text>
{body}
{"".join(chip_svg)}
<text x="{w-30}" y="222" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="2" fill="{MUTED}">{esc(link_label)} &#8594;</text>
{border(w, h, 16)}
</svg>
"""
    (OUT / f"card-{slug}.svg").write_text(svg)


# ---------------------------------------------------------------- 6. terminal
def terminal():
    w, h = 1200, 368
    gid = "tm"
    lines = [
        (MONO, ACCENT2, "parsa@kagu", " ~/touch-padel ", "git:(main)"),
    ]
    rows = [
        ("cmd", "pnpm turbo build --filter=...[origin/main]"),
        ("out", "  web:booking   built in 12.4s"),
        ("out", "  web:site      built in  9.1s"),
        ("out", "  desktop:ops   built in 18.7s"),
        ("ok",  "  3 packages, 0 errors, 0 type errors"),
        ("cmd", "pnpm test && vercel deploy --prod"),
        ("ok",  "  tests passed, deployed to production"),
        ("cmd", "git log --oneline -1"),
        ("out", "  feat(ops): offline-first till, EN/AR, full RTL"),
    ]
    y = 118
    body = []
    t = 0.5
    for kind, text in rows:
        if kind == "cmd":
            body.append(f"""<g opacity="0">
<text x="38" y="{y}" font-family="{MONO}" font-size="14.5" fill="{ACCENT}">$</text>
<text x="60" y="{y}" font-family="{MONO}" font-size="14.5" fill="{TEXT}">{esc(text)}</text>
<animate attributeName="opacity" from="0" to="1" dur="0.28s" begin="{t:.2f}s" fill="freeze"/></g>""")
        else:
            col = GREEN if kind == "ok" else MUTED
            mark = "&#10003; " if kind == "ok" else ""
            body.append(f"""<g opacity="0">
<text x="60" y="{y}" font-family="{MONO}" font-size="14" fill="{col}">{mark}{esc(text.strip())}</text>
<animate attributeName="opacity" from="0" to="1" dur="0.28s" begin="{t:.2f}s" fill="freeze"/></g>""")
        y += 25
        t += 0.34

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="A build and deploy from a normal day">
<defs>
<linearGradient id="{gid}-bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{NAVY_2}"/></linearGradient>
<clipPath id="{gid}-clip"><rect width="{w}" height="{h}" rx="16"/></clipPath>
{sweep_def(gid)}
</defs>
<rect width="{w}" height="{h}" rx="16" fill="url(#{gid}-bg)"/>
{sweep(w, h, gid, "10s", "1.5s")}
<rect x="0" y="0" width="{w}" height="52" fill="{NAVY}" clip-path="url(#{gid}-clip)"/>
<line x1="0" y1="52" x2="{w}" y2="52" stroke="{LINE}"/>
<circle cx="30" cy="26" r="6" fill="#FF5F57"/><circle cx="52" cy="26" r="6" fill="{AMBER}"/><circle cx="74" cy="26" r="6" fill="{GREEN}"/>
<text x="{w/2}" y="31" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{MUTED}">parsa@kagu  /  a normal tuesday</text>
<text x="38" y="86" font-family="{MONO}" font-size="14.5" fill="{DIM}">&#35; four products in flight, one stack, zero drama</text>
{"".join(body)}
<rect x="60" y="{y-14}" width="9" height="17" fill="{ACCENT}" opacity="0">
<animate attributeName="opacity" values="0;1" dur="0.1s" begin="{t:.2f}s" fill="freeze"/>
<animate attributeName="opacity" values="1;1;0;0;1" dur="1.1s" begin="{t+0.1:.2f}s" repeatCount="indefinite"/></rect>
{border(w, h, 16)}
</svg>
"""


# ---------------------------------------------------------------- 7. footer
def footer():
    w, h = 1200, 150
    gid = "ft"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Contact">
{panel(w, h, 18, gid, 0.12, 0.9)}
<defs>{sweep_def(gid)}</defs>
{dotgrid(w, h, gid, 40)}
{sweep(w, h, gid, "8s", "0.5s")}
<text x="60" y="58" font-family="{MONO}" font-size="11" letter-spacing="3.2" fill="{ACCENT2}">LET&#39;S BUILD SOMETHING</text>
<text x="58" y="100" font-family="{SANS}" font-weight="800" font-size="34" letter-spacing="-1.2" fill="{TEXT}">kagusoftware.com</text>
<text x="58" y="126" font-family="{MONO}" font-size="12.5" fill="{MUTED}">parsaa.mansourii@gmail.com<tspan fill="{DIM}">  /  </tspan>Istanbul, Turkiye</text>
<g transform="translate(985 40) scale(0.15) translate(-130 -370)" opacity="0.9">{KAGU_MARK}</g>
{border(w, h, 18)}
</svg>
"""


def build():
    (OUT / "header.svg").write_text(header())
    (OUT / "stats.svg").write_text(stats())
    (OUT / "heat.svg").write_text(heat())
    (OUT / "stack.svg").write_text(stack())
    (OUT / "terminal.svg").write_text(terminal())
    (OUT / "footer.svg").write_text(footer())

    card("touchpadel", "01", "PRODUCT / VENUE OS", "Touch Padel",
         ["One Postgres, three surfaces: a guest booking app, a public",
          "site with QR cafe ordering, and a Windows operator app",
          "running till, front desk, kitchen and stock. EN and AR with",
          "full RTL, and it keeps serving when the venue loses wifi."],
         ["Next.js", "React Native", "Supabase", "Electron"], "VIEW REPO")

    card("kaguos", "02", "PRODUCT / INTERNAL OS", "KaguOS",
         ["The system the studio runs on. Clients, projects, delivery",
          "and the day to day of the company in one place, built the",
          "same way we build for clients: fast, boring stack,",
          "deployed continuously."],
         ["Next.js", "Supabase", "Vercel"], "VIEW REPO")

    card("upperdeck", "03", "CLIENT / HOSPITALITY", "UpperDeck",
         ["Digital menu and website for an American diner in Besiktas,",
          "Istanbul. Kagu also runs the paid social on Meta and TikTok,",
          "so the site is measured on walk-ins and orders, not on",
          "how it looks in a portfolio."],
         ["Next.js", "Vercel", "Meta Ads"], "upperdeckk.com")

    card("turkcure", "04", "CLIENT / HEALTH TOURISM", "TurkCure Ops",
         ["Back office for a health tourism team: the patient pipeline",
          "from first lead to aftercare, plus the network behind it,",
          "doctors, hospitals and partners. It replaced a folder",
          "of spreadsheets."],
         ["Next.js", "Supabase", "TypeScript"], "VIEW REPO")


if __name__ == "__main__":
    build()
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.name:22} {p.stat().st_size/1024:6.1f} KB")
