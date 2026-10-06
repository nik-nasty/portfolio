#!/usr/bin/env python3
"""Generates every page of the portfolio as a standalone HTML file.

Run from the repo root:  python3 _build/build.py
Output: index.html, all-work.html, work/<slug>.html
Textures come from _build/textures.py (run once; they are committed in assets/).
"""
import os, sys, html, math
sys.path.insert(0, os.path.dirname(__file__))
from content import SITE, CASES, ALL_WORK  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Glyphs: one small line drawing per case study.
# ---------------------------------------------------------------------------
G = 'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
GLYPHS = {
    "route": f'<svg viewBox="0 0 48 48" {G}><path d="M8 24h10"/><circle cx="4.5" cy="24" r="2.5"/><path d="M18 24c6 0 6-10 12-10h8M18 24c6 0 6 10 12 10h8M18 24h20"/><circle cx="42" cy="14" r="2.5"/><circle cx="42" cy="24" r="2.5"/><circle cx="42" cy="34" r="2.5"/></svg>',
    "phone": f'<svg viewBox="0 0 48 48" {G}><rect x="15" y="5" width="18" height="38" rx="4"/><path d="M21 9h6M24 36v.5"/><path d="M37 15c3 3 3 9 0 12M41 11c6 6 6 14 0 20"/></svg>',
    "pipeline": f'<svg viewBox="0 0 48 48" {G}><circle cx="8" cy="24" r="3"/><circle cx="24" cy="24" r="3"/><circle cx="40" cy="24" r="3"/><path d="M11 24h10M27 24h10"/><path d="M24 14v-6M24 40v-6"/></svg>',
    "swatch": f'<svg viewBox="0 0 48 48" {G}><rect x="6" y="8" width="12" height="32" rx="3"/><rect x="18" y="8" width="12" height="32" rx="3"/><rect x="30" y="8" width="12" height="32" rx="3"/><path d="M12 32v.5M24 32v.5M36 32v.5"/></svg>',
    "page": f'<svg viewBox="0 0 48 48" {G}><rect x="9" y="5" width="30" height="38" rx="3"/><path d="M9 20h30"/><path d="M15 27h18M15 33h12"/><path d="M15 12h8"/></svg>',
    "book": f'<svg viewBox="0 0 48 48" {G}><path d="M24 12c-4-4-10-4-16-3v27c6-1 12-1 16 3 4-4 10-4 16-3V9c-6-1-12-1-16 3z"/><path d="M24 12v27"/></svg>',
    "grid": f'<svg viewBox="0 0 48 48" {G}><rect x="7" y="9" width="34" height="32" rx="3"/><path d="M7 19h34M18 19v22M30 19v22M14 9V5M34 9V5"/></svg>',
    "browser": f'<svg viewBox="0 0 48 48" {G}><rect x="5" y="9" width="38" height="30" rx="3"/><path d="M5 17h38"/><circle cx="10" cy="13" r="1"/><circle cx="14" cy="13" r="1"/><path d="M11 24h14M11 30h22"/></svg>',
    "ticket": f'<svg viewBox="0 0 48 48" {G}><path d="M6 15a4 4 0 0 1 4-4h28a4 4 0 0 1 4 4v5a4 4 0 0 0 0 8v5a4 4 0 0 1-4 4H10a4 4 0 0 1-4-4v-5a4 4 0 0 0 0-8z"/><path d="M30 13v22" stroke-dasharray="2 3"/></svg>',
    "form": f'<svg viewBox="0 0 48 48" {G}><rect x="8" y="9" width="32" height="8" rx="2"/><rect x="8" y="20" width="32" height="8" rx="2"/><rect x="8" y="31" width="18" height="8" rx="2"/><path d="M32 35l3 3 5-6"/></svg>',
    "chips": f'<svg viewBox="0 0 48 48" {G}><circle cx="14" cy="16" r="7"/><circle cx="32" cy="16" r="7"/><circle cx="14" cy="34" r="7"/><circle cx="32" cy="34" r="7"/><path d="M29 34h6"/></svg>',
}


def moons():
    """A quiet row of moon phases, new to full to new, drawn as SVG."""
    parts = []
    r = 7
    ks = [0.0, 0.25, 0.5, 0.75, 1.0, 0.75, 0.5, 0.25, 0.0]
    for i, k in enumerate(ks):
        cx = 12 + i * 26
        cy = 10
        lit_right = i <= 4
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-opacity=".45"/>')
        if k >= 0.999:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="currentColor" fill-opacity=".85"/>')
        elif k > 0.001:
            rx = abs(r * math.cos(math.pi * k))
            if lit_right:
                sweep_outer = 1
                term_sweep = 1 if k < 0.5 else 0
            else:
                sweep_outer = 0
                term_sweep = 0 if k < 0.5 else 1
            d = f"M{cx},{cy - r} A{r},{r} 0 0 {sweep_outer} {cx},{cy + r} A{rx:.2f},{r} 0 0 {term_sweep} {cx},{cy - r} Z"
            parts.append(f'<path d="{d}" fill="currentColor" fill-opacity=".85"/>')
    return f'<svg class="moons" viewBox="0 0 232 20" aria-hidden="true">{"".join(parts)}</svg>'


# ---------------------------------------------------------------------------
# Stylesheet, inlined into every page so each file stands alone.
# ---------------------------------------------------------------------------
CSS = r"""
:root{
  --night:#120a1c; --plum:#1b1130; --panel:rgba(255,255,255,.045); --panel2:rgba(255,255,255,.075);
  --line:rgba(236,226,250,.14); --line2:rgba(236,226,250,.28); --ink:#f3edf9; --mist:#c2b5d4; --dim:#9486aa;
  --orchid:#d6b0f4; --pearl:#efe3fb;
  --light:linear-gradient(90deg, rgba(246,214,228,0) 0%, #f6d6e4 20%, #d4ebf2 45%, #f3e5c9 70%, rgba(243,229,201,0) 100%);
  --serif:"Cormorant Garamond", "Cormorant", Georgia, "Times New Roman", serif;
  --sans:"Figtree", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --maxw:1080px; --col:70ch;
  color-scheme:dark;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{margin:0;background:var(--night);color:var(--ink);font:400 17px/1.6 var(--sans);overflow-x:hidden;-webkit-font-smoothing:antialiased}
body{min-height:100vh;animation:fadein .8s ease-out both;position:relative}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.07;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
@keyframes fadein{from{opacity:0}to{opacity:1}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}body{animation:none}}
a{color:var(--orchid);text-decoration:none}
a:hover{text-decoration:underline;text-underline-offset:3px}
a:focus-visible,button:focus-visible{outline:2px solid var(--orchid);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:-999px;top:8px;background:var(--plum);padding:8px 12px;border-radius:8px;z-index:9}
.skip:focus{left:16px}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px;position:relative;z-index:1}
h1,h2,h3,h4{font-family:var(--serif);font-weight:600;line-height:1.06;margin:0;letter-spacing:-.005em}
p{margin:0 0 1em}
ul,ol{margin:0 0 1em;padding-left:1.3em}
li{margin:0 0 .5em}
li::marker{color:var(--dim)}
b{font-weight:600;color:var(--pearl)}

/* the window: a picture that stays still while the page slides over it */
.pin{position:relative;clip-path:inset(0);isolation:isolate}
.pin-img{position:fixed;inset:0;z-index:0;background-position:center;background-size:cover;background-repeat:no-repeat}
.pin-in{position:relative;z-index:1}
@supports not (clip-path:inset(0)){.pin{overflow:hidden}.pin-img{position:absolute}}

/* top bar */
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:24px 0 8px}
.bar .me{font-family:var(--serif);font-weight:600;font-size:22px;color:var(--ink)}
.bar nav{display:flex;gap:24px;font-size:15px}
.bar nav a{color:var(--pearl);opacity:.85}
.bar nav a[aria-current]{opacity:1;border-bottom:1px solid var(--orchid);padding-bottom:2px}

/* home hero */
.hero .pin-img{background-image:url("assets/hero.jpg")}
.hero .pin-img::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg, rgba(18,10,28,.25) 0%, rgba(18,10,28,.10) 40%, rgba(18,10,28,.55) 85%, var(--night) 100%)}
.hero-body{padding-top:54px}
.hero h1{font-size:clamp(50px,9vw,112px);font-weight:500;line-height:.94;text-shadow:0 2px 30px rgba(18,10,28,.6)}
.hero .role{font-family:var(--serif);font-size:clamp(25px,3.4vw,38px);font-weight:500;color:var(--pearl);margin:22px 0 0;line-height:1.15;display:flex;gap:14px;flex-wrap:wrap}
.hero .role span{white-space:nowrap}
.hero .intro{max-width:54ch;color:var(--pearl);opacity:.9;font-size:18px;margin:20px 0 0;text-shadow:0 1px 14px rgba(18,10,28,.6)}
.pano{margin:40px 0 0;border-radius:18px;overflow:hidden;outline:1px solid var(--line2);box-shadow:0 30px 80px rgba(0,0,0,.45);aspect-ratio:1576/672;background:var(--plum)}
.pano img{width:100%;height:100%;object-fit:cover;display:block}
.moons{display:block;width:232px;height:20px;color:var(--pearl);margin:34px auto 0;opacity:.8}
.hero-end{height:54px}

/* sections */
.section{padding:70px 0 20px}
.section>h2{font-size:clamp(34px,4.4vw,48px);margin:0 0 8px}
.section>.sub{color:var(--mist);margin:0 0 34px;max-width:60ch;font-size:17px}
.features{list-style:none;padding:0;margin:0;display:grid;gap:56px}
.feature{display:grid;grid-template-columns:1.15fr 1fr;gap:34px;align-items:center;color:var(--ink)}
.features li:nth-child(even) .fimg{order:2}
.feature:hover{text-decoration:none}
.feature:hover .fimg img{transform:scale(1.025)}
.fimg{border-radius:18px;overflow:hidden;outline:1px solid var(--line);box-shadow:0 24px 60px rgba(0,0,0,.4);aspect-ratio:16/10;position:relative;background:var(--plum)}
.fimg img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .9s ease}
@media (prefers-reduced-motion:reduce){.fimg img{transition:none}}
.fimg .g{position:absolute;left:16px;bottom:14px;width:44px;height:44px;border-radius:12px;background:rgba(18,10,28,.55);backdrop-filter:blur(6px);border:1px solid var(--line);color:var(--pearl);display:grid;place-items:center}
.fimg .g svg{width:28px;height:28px}
.ftxt h3{font-size:clamp(28px,3.2vw,38px);margin:0 0 12px}
.ftxt p{color:var(--mist);margin:0 0 14px}
.ftxt .meta{font-size:14px;color:var(--dim);margin:0 0 16px}
.ftxt .cta{color:var(--orchid);font-size:15.5px}
.how{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.how div{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:24px 22px;backdrop-filter:blur(10px);position:relative;overflow:hidden}
.how div::before{content:"";position:absolute;left:0;right:0;top:0;height:1px;background:var(--light);opacity:.6}
.how h3{font-size:25px;margin:0 0 10px}
.how p{color:var(--mist);font-size:16px;margin:0}
.contact p{max-width:52ch;color:var(--mist)}
.contact .links{display:flex;flex-wrap:wrap;gap:12px 14px}
.contact .links a{border:1px solid var(--line2);border-radius:999px;padding:10px 20px;color:var(--pearl);font-size:16px;background:var(--panel)}
.contact .links a:hover{text-decoration:none;background:var(--panel2)}

/* case study cover */
.cover{min-height:58vh}
.cover .pin-img::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg, rgba(18,10,28,.25) 0%, rgba(18,10,28,.15) 45%, rgba(18,10,28,.78) 100%)}
.cover-body{min-height:58vh;display:flex;flex-direction:column;justify-content:flex-end;padding-top:40px;padding-bottom:44px}
.cover .meta{color:var(--pearl);opacity:.85;font-size:16px;margin:0 0 12px}
.cover h1{font-size:clamp(38px,6vw,68px);font-weight:500;max-width:18ch;text-shadow:0 2px 30px rgba(18,10,28,.7)}
.lede-wrap{padding-top:34px;padding-bottom:8px;max-width:var(--col)}
.lede{font-size:21px;line-height:1.5;color:var(--pearl);margin:0 0 16px}
.tools{font-size:15px;color:var(--dim)}
.light{height:2px;background:var(--light);opacity:.7;margin:26px 0 8px;border-radius:2px}
article{max-width:var(--col);padding:0 0 40px}
article section{padding:28px 0 6px}
article h2{font-size:32px;margin:0 0 14px}
article p,article li{color:var(--ink)}
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:8px 6px;margin:6px 0 20px}
.node{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:7px 12px;font-size:15px;line-height:1.3;backdrop-filter:blur(6px)}
.arr{width:14px;height:14px;position:relative;flex:0 0 auto}
.arr::before{content:"";position:absolute;inset:3px 4px;border-top:1.5px solid var(--dim);border-right:1.5px solid var(--dim);transform:rotate(45deg)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:6px 0 18px}
.pane{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px;backdrop-filter:blur(10px);position:relative;overflow:hidden}
.pane::before{content:"";position:absolute;left:0;right:0;top:0;height:1px;background:var(--light);opacity:.5}
.pane h4{font-size:22px;margin:0 0 8px}
.pane p,.pane li{font-size:15.5px;color:var(--mist)}
.pane p:last-child,.pane ul{margin-bottom:0}
.shots{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:8px 0 0}
.shot{margin:0}
.shot-box{aspect-ratio:16/10;border:1px dashed var(--line2);border-radius:12px;display:grid;place-items:center;color:var(--dim);font-size:14px;background:var(--panel)}
.shot figcaption{font-size:14.5px;color:var(--mist);margin:8px 2px 0}
.next{border-top:1px solid var(--line);padding:26px 0 48px;max-width:var(--col)}
.next .k{color:var(--dim);font-size:14px;margin:0 0 6px}
.next a{font-family:var(--serif);font-size:30px;font-weight:600}

/* all work */
.client{padding:34px 0 8px}
.client h2{font-size:36px;margin:0}
.client .k{color:var(--dim);margin:4px 0 0}
.grp{padding:18px 0 4px;max-width:var(--col)}
.grp h3{font-size:23px;color:var(--pearl);margin:0 0 8px}
.grp ul{list-style:none;padding:0;margin:0}
.grp li{padding:9px 0;border-top:1px solid var(--line);color:var(--mist);font-size:16px}
.grp li a{color:var(--ink)}
.grp li a::after{content:"Case study";font-size:12.5px;color:var(--orchid);margin-left:10px;border:1px solid var(--line);border-radius:999px;padding:1px 8px;vertical-align:1px}

footer{border-top:1px solid var(--line);margin-top:48px;padding:26px 0 48px;color:var(--dim);font-size:14.5px;display:flex;flex-wrap:wrap;gap:10px 28px;justify-content:space-between}
footer a{color:var(--mist)}

@media (max-width:820px){
  .feature,.how,.pair,.shots{grid-template-columns:1fr}
  .feature{gap:18px}
  .features li:nth-child(even) .fimg{order:0}
  .features{gap:46px}
  .bar nav{gap:16px;font-size:14px}
  .hero-body{padding-top:34px}
  .pano{margin-top:28px}
  .flow{flex-direction:column;align-items:stretch}
  .arr{width:100%;height:14px}
  .arr::before{inset:0 0 0 calc(50% - 7px);width:10px;height:10px;transform:rotate(135deg);border-width:1.5px}
  .cover,.cover-body{min-height:48vh}
}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">'


def head(title, desc, root):
    css = CSS.replace('url("assets/', f'url("{root}assets/')
    return (
        '<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc)}">\n'
        f'<meta name="color-scheme" content="dark">\n<meta name="theme-color" content="#120a1c">\n{FONTS}\n<style>{css}</style>\n</head>\n<body>\n'
        '<a class="skip" href="#main">Skip to content</a>\n'
    )


def bar(root, current):
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{root}{href}"{cur}>{label}</a>'
    return (
        '<div class="wrap bar">'
        f'<a class="me" href="{root}index.html">{SITE["short"]} Feldmann</a>'
        f'<nav aria-label="Site">{nav("index.html#work","Work","work")}{nav("all-work.html","All work","all")}{nav("index.html#contact","Contact","contact")}</nav>'
        "</div>\n"
    )


def footer(root):
    return (
        '<footer class="wrap">'
        f'<span>{SITE["name"]}. Based in {SITE["location"]}, working with UK clients.</span>'
        f'<span><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></span>'
        "</footer>\n</body>\n</html>\n"
    )


def home():
    feats = []
    for c in CASES:
        feats.append(
            f'<li><a class="feature" href="work/{c["slug"]}.html">'
            f'<span class="fimg"><img src="assets/cover-{c["slug"]}.jpg" alt="" loading="lazy" width="1600" height="1000">'
            f'<span class="g" aria-hidden="true">{GLYPHS[c["glyph"]]}</span></span>'
            f'<span class="ftxt"><h3>{c["title"]}</h3><p>{c["card"]}</p>'
            f'<p class="meta">{c["client"]}. {c["dates"]}.</p><span class="cta">Read the case study</span></span>'
            "</a></li>"
        )
    how = "".join(f"<div><h3>{h}</h3><p>{p}</p></div>" for h, p in SITE["how"])
    first, last = SITE["name"].rsplit(" ", 1)
    out = head(f'{SITE["name"]}: automation engineer', SITE["intro"], "")
    out += (
        '<header class="hero pin"><div class="pin-img" aria-hidden="true"></div><div class="pin-in">'
        + bar("", "home") +
        '<div class="wrap hero-body">'
        f'<h1>{first}<br>{last}</h1>'
        f'<p class="role"><span>{SITE["title_a"]}</span><span>{SITE["title_b"]}</span></p>'
        f'<p class="intro">{SITE["intro"]}</p>'
        f'<div class="pano"><img src="assets/nikki_pano.jpg" alt="{SITE["name"]}" width="1576" height="672"></div>'
        f'{moons()}<div class="hero-end"></div>'
        "</div></div></header>\n"
    )
    out += (
        '<main id="main" class="wrap">'
        '<section class="section" id="work"><h2>Selected work</h2>'
        '<p class="sub">Eleven pieces from the last four months: the problem, what I built, how it works and what changed. Client names, prices and figures are kept out.</p>'
        f'<ul class="features">{"".join(feats)}</ul>'
        '<p style="margin:40px 0 0"><a href="all-work.html">See every project</a></p>'
        "</section>"
        f'<section class="section" id="how"><h2>How I work</h2><p class="sub">Three rules I keep coming back to.</p><div class="how">{how}</div></section>'
        '<section class="section contact" id="contact"><h2>Contact</h2>'
        "<p>If you have a process that runs on people remembering things, or pages that no longer match the business, I would like to hear about it.</p>"
        f'<div class="links"><a href="mailto:{SITE["email"]}">Email {SITE["short"]}</a><a href="{SITE["upwork"]}">Upwork profile</a></div>'
        "</section></main>\n"
    )
    out += footer("")
    return out


def case_page(c, i):
    root = "../"
    nxt = CASES[(i + 1) % len(CASES)]
    body = "".join(f"<section><h2>{h}</h2>{b}</section>" for h, b in c["sections"])
    shots = "".join(
        f'<figure class="shot"><div class="shot-box"><span>Screenshot to add</span></div><figcaption>{s}</figcaption></figure>'
        for s in c["shots"]
    )
    out = head(f'{c["title"]}: {SITE["short"]} Feldmann', c["card"], root)
    out += (
        f'<header class="cover pin"><div class="pin-img" aria-hidden="true" style="background-image:url(\'{root}assets/cover-{c["slug"]}.jpg\')"></div><div class="pin-in">'
        + bar(root, "work") +
        f'<div class="wrap cover-body"><p class="meta">{c["client"]}. {c["dates"]}.</p><h1>{c["title"]}</h1></div>'
        "</div></header>\n"
    )
    out += (
        f'<main id="main" class="wrap"><div class="lede-wrap"><p class="lede">{c["lede"]}</p><p class="tools">{c["tools"]}</p>'
        '<div class="light" aria-hidden="true"></div></div>'
        f"<article>{body}"
        f'<section><h2>Visuals coming to this page</h2><div class="shots">{shots}</div></section>'
        "</article>"
        f'<div class="next"><p class="k">Next</p><a href="{nxt["slug"]}.html">{nxt["title"]}</a></div></main>\n'
    )
    out += footer(root)
    return out


def all_work():
    out = head(f"All work: {SITE['short']} Feldmann", "Every project, one line each.", "")
    out += (
        '<header class="cover pin"><div class="pin-img" aria-hidden="true" style="background-image:url(\'assets/hero.jpg\')"></div><div class="pin-in">'
        + bar("", "all") +
        '<div class="wrap cover-body"><p class="meta">June to October 2026</p><h1>All work</h1></div></div></header>\n'
    )
    out += '<main id="main" class="wrap"><div class="lede-wrap"><p class="lede">Every project, one line each. The ones with a case study link through.</p><div class="light" aria-hidden="true"></div></div>'
    for client, dates, groups in ALL_WORK:
        out += f'<section class="client"><h2>{client}</h2><p class="k">{dates}</p></section>'
        for gname, items in groups:
            lis = []
            for label, slug in items:
                if slug:
                    lis.append(f'<li><a href="work/{slug}.html">{label}</a></li>')
                else:
                    lis.append(f"<li>{label}</li>")
            out += f'<div class="grp"><h3>{gname}</h3><ul>{"".join(lis)}</ul></div>'
    out += "</main>\n" + footer("")
    return out


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"{path}  {len(text.encode('utf-8'))//1024}KB")


if __name__ == "__main__":
    write("index.html", home())
    write("all-work.html", all_work())
    for i, c in enumerate(CASES):
        write(f"work/{c['slug']}.html", case_page(c, i))
    open(os.path.join(ROOT, ".nojekyll"), "w").close()
