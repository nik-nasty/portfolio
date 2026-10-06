#!/usr/bin/env python3
"""Generates every page of the portfolio as a standalone HTML file.

Run from anywhere:  python3 _build/build.py
Output: index.html, all-work.html, work/<slug>.html at the repo root.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from content import SITE, CASES, ALL_WORK  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Glyphs: one small line drawing per case study, drawn once, reused on cards.
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

STAR = '<svg class="star" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2c.6 6 4 9.4 10 10-6 .6-9.4 4-10 10-.6-6-4-9.4-10-10 6-.6 9.4-4 10-10z" fill="currentColor"/></svg>'

# ---------------------------------------------------------------------------
# Stylesheet, inlined into every page so each file stands alone.
# ---------------------------------------------------------------------------
CSS = r"""
:root{
  --night:#140b1f; --plum:#1d1230; --panel:#281a3c; --panel2:#33234b;
  --line:rgba(236,226,250,.13); --ink:#f1ebf8; --mist:#bcafcf; --dim:#8f82a4;
  --orchid:#d2abf2; --pearl:#efe3fb;
  --light:linear-gradient(90deg, rgba(246,214,228,0) 0%, #f6d6e4 20%, #d4ebf2 45%, #f3e5c9 70%, rgba(243,229,201,0) 100%);
  --serif:"Cormorant Garamond", "Cormorant", Georgia, "Times New Roman", serif;
  --sans:"Figtree", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --maxw:1040px; --col:70ch;
  color-scheme:dark;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
html,body{margin:0;background:var(--plum);color:var(--ink);font:400 17px/1.6 var(--sans);overflow-x:hidden;-webkit-font-smoothing:antialiased}
body{background:radial-gradient(1200px 700px at 85% -10%, rgba(220,190,255,.14), transparent 60%), linear-gradient(180deg, var(--plum) 0%, var(--night) 100%);min-height:100vh}
a{color:var(--orchid);text-decoration:none}
a:hover{text-decoration:underline;text-underline-offset:3px}
a:focus-visible,button:focus-visible{outline:2px solid var(--orchid);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:-999px;top:8px;background:var(--panel2);padding:8px 12px;border-radius:8px;z-index:9}
.skip:focus{left:16px}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 20px}
h1,h2,h3,h4{font-family:var(--serif);font-weight:600;line-height:1.08;margin:0;letter-spacing:-.005em}
p{margin:0 0 1em}
ul,ol{margin:0 0 1em;padding-left:1.3em}
li{margin:0 0 .5em}
li::marker{color:var(--dim)}
b{font-weight:600;color:var(--pearl)}

/* top bar */
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:22px 0 8px}
.bar .me{font-family:var(--serif);font-weight:600;font-size:21px;color:var(--ink)}
.bar nav{display:flex;gap:22px;font-size:15px}
.bar nav a{color:var(--mist)}
.bar nav a[aria-current]{color:var(--ink);border-bottom:1px solid var(--orchid);padding-bottom:2px}

/* hero (home) */
.hero{display:grid;grid-template-columns:1fr auto;gap:40px;align-items:end;padding:56px 0 40px}
.hero h1{font-size:clamp(46px,8vw,86px);font-weight:500;line-height:.98}
.hero .role{font-family:var(--serif);font-size:clamp(24px,3.2vw,34px);font-weight:500;color:var(--pearl);margin:18px 0 0;line-height:1.15;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.hero .role span{white-space:nowrap}
.star{width:18px;height:18px;color:var(--orchid);flex:0 0 auto}
.hero .intro{max-width:52ch;color:var(--mist);font-size:18px;margin:22px 0 0}
.arch{width:230px;height:300px;border-radius:115px 115px 18px 18px;overflow:hidden;background:var(--panel);outline:1px solid var(--line);justify-self:end}
.arch img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(.9)}
.light{height:2px;background:var(--light);opacity:.7;margin:8px 0 48px;border-radius:2px}

/* sections */
.section{padding:12px 0 56px}
.section>h2{font-size:34px;margin:0 0 6px}
.section>.sub{color:var(--mist);margin:0 0 26px;max-width:60ch}
.work{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;list-style:none;padding:0;margin:0}
.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:24px 24px 20px;color:var(--ink);height:100%}
.card:hover{text-decoration:none;border-color:rgba(236,226,250,.3)}
.card .g{display:block;width:40px;height:40px;color:var(--orchid);margin:0 0 16px}
.card .g svg{width:100%;height:100%}
.card h3{font-size:27px;margin:0 0 10px;line-height:1.1}
.card p{color:var(--mist);margin:0 0 14px;font-size:16px}
.card .meta{font-size:13.5px;color:var(--dim);margin:0}
.how{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
.how h3{font-size:24px;margin:0 0 8px}
.how p{color:var(--mist);font-size:16px;margin:0}
.contact p{max-width:52ch;color:var(--mist)}
.contact .links{display:flex;flex-wrap:wrap;gap:12px 28px;font-size:17px}

/* case study */
.case{max-width:var(--col);padding:40px 0 32px}
.case .meta{color:var(--mist);font-size:16px;margin:0 0 14px}
.case h1{font-size:clamp(36px,5.4vw,56px);font-weight:500;margin:0 0 18px}
.case .lede{font-size:20px;line-height:1.55;color:var(--pearl);margin:0 0 18px}
.case .tools{font-size:15px;color:var(--dim)}
.case .light{margin:28px 0 8px}
article{max-width:var(--col);padding:0 0 40px}
article section{padding:26px 0 6px}
article h2{font-size:30px;margin:0 0 14px}
article p{color:var(--ink)}
article ul li,article ol li{color:var(--ink)}
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:8px 6px;margin:6px 0 20px}
.node{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:7px 12px;font-size:15px;line-height:1.3}
.arr{width:14px;height:14px;position:relative;flex:0 0 auto}
.arr::before{content:"";position:absolute;inset:3px 4px;border-top:1.5px solid var(--dim);border-right:1.5px solid var(--dim);transform:rotate(45deg)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:6px 0 18px}
.pane{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.pane h4{font-size:21px;margin:0 0 8px}
.pane p,.pane li{font-size:15.5px;color:var(--mist)}
.pane p:last-child,.pane ul{margin-bottom:0}
.shots{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:8px 0 0}
.shot{margin:0}
.shot-box{aspect-ratio:16/10;border:1px dashed rgba(236,226,250,.3);border-radius:12px;display:grid;place-items:center;color:var(--dim);font-size:14px;background:rgba(255,255,255,.02)}
.shot figcaption{font-size:14.5px;color:var(--mist);margin:8px 2px 0}
.next{border-top:1px solid var(--line);padding:26px 0 40px;max-width:var(--col)}
.next .k{color:var(--dim);font-size:14px;margin:0 0 6px}
.next a{font-family:var(--serif);font-size:28px;font-weight:600}

/* all work */
.client{padding:28px 0 8px}
.client h2{font-size:34px;margin:0}
.client .k{color:var(--dim);margin:4px 0 0}
.grp{padding:18px 0 4px;max-width:var(--col)}
.grp h3{font-size:22px;color:var(--pearl);margin:0 0 8px}
.grp ul{list-style:none;padding:0;margin:0}
.grp li{padding:9px 0;border-top:1px solid var(--line);color:var(--mist);font-size:16px}
.grp li a{color:var(--ink)}
.grp li a::after{content:"Case study";font-size:12.5px;color:var(--orchid);margin-left:10px;border:1px solid var(--line);border-radius:99px;padding:1px 8px;vertical-align:1px}

footer{border-top:1px solid var(--line);margin-top:28px;padding:26px 0 48px;color:var(--dim);font-size:14.5px;display:flex;flex-wrap:wrap;gap:10px 28px;justify-content:space-between}
footer a{color:var(--mist)}

@media (max-width:800px){
  .work,.how,.pair,.shots{grid-template-columns:1fr}
  .hero{grid-template-columns:1fr;gap:28px;padding:36px 0 28px}
  .arch{justify-self:start;width:170px;height:220px;border-radius:85px 85px 14px 14px;order:-1}
  .bar nav{gap:16px;font-size:14px}
  .flow{flex-direction:column;align-items:stretch}
  .arr{width:100%;height:14px}
  .arr::before{inset:0 0 0 calc(50% - 7px);width:10px;height:10px;transform:rotate(135deg);border-width:1.5px}
}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">'


def head(title, desc, root):
    return (
        '<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc)}">\n'
        f'<meta name="color-scheme" content="dark">\n{FONTS}\n<style>{CSS}</style>\n</head>\n<body>\n'
        '<a class="skip" href="#main">Skip to content</a>\n'
    )


def bar(root, current):
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{root}{href}"{cur}>{label}</a>'
    return (
        '<header class="wrap bar">'
        f'<a class="me" href="{root}index.html">{SITE["short"]} Feldmann</a>'
        f'<nav aria-label="Site">{nav("index.html#work","Work","work")}{nav("all-work.html","All work","all")}{nav("index.html#contact","Contact","contact")}</nav>'
        "</header>\n"
    )


def footer(root):
    return (
        '<footer class="wrap">'
        f'<span>{SITE["name"]}. Based in {SITE["location"]}, working with UK clients.</span>'
        f'<span><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></span>'
        "</footer>\n</body>\n</html>\n"
    )


def home():
    cards = []
    for c in CASES:
        cards.append(
            f'<li><a class="card" href="work/{c["slug"]}.html">'
            f'<span class="g" aria-hidden="true">{GLYPHS[c["glyph"]]}</span>'
            f'<h3>{c["title"]}</h3><p>{c["card"]}</p>'
            f'<p class="meta">{c["client"]}. {c["dates"]}.</p></a></li>'
        )
    how = "".join(f"<div><h3>{h}</h3><p>{p}</p></div>" for h, p in SITE["how"])
    first, last = SITE["name"].rsplit(" ", 1)
    out = head(f'{SITE["name"]}: automation engineer', SITE["intro"], "")
    out += bar("", "home")
    out += (
        '<main id="main" class="wrap">'
        '<section class="hero">'
        f'<div><h1>{first}<br>{last}</h1>'
        f'<p class="role">{STAR}<span>{SITE["title_a"]}</span><span>{SITE["title_b"]}</span></p>'
        f'<p class="intro">{SITE["intro"]}</p></div>'
        f'<div class="arch"><img src="nikki_photo.jpg" alt="{SITE["name"]}" width="304" height="304"></div>'
        "</section>"
        '<div class="light" aria-hidden="true"></div>'
        '<section class="section" id="work"><h2>Selected work</h2>'
        '<p class="sub">Eleven pieces from the last four months, each with the problem, what I built, how it works and what changed. Client names, prices and figures are kept out.</p>'
        f'<ul class="work">{"".join(cards)}</ul>'
        '<p style="margin:22px 0 0"><a href="all-work.html">See every project</a></p>'
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
    out += bar(root, "work")
    out += (
        f'<main id="main" class="wrap"><header class="case"><p class="meta">{c["client"]}. {c["dates"]}.</p>'
        f'<h1>{c["title"]}</h1><p class="lede">{c["lede"]}</p><p class="tools">{c["tools"]}</p>'
        '<div class="light" aria-hidden="true"></div></header>'
        f"<article>{body}"
        f'<section><h2>Visuals coming to this page</h2><div class="shots">{shots}</div></section>'
        "</article>"
        f'<div class="next"><p class="k">Next</p><a href="{nxt["slug"]}.html">{nxt["title"]}</a></div></main>\n'
    )
    out += footer(root)
    return out


def all_work():
    out = head(f"All work: {SITE['short']} Feldmann", "Every project, one line each.", "")
    out += bar("", "all")
    out += '<main id="main" class="wrap"><header class="case"><h1>All work</h1><p class="lede">Every project from June to October 2026, one line each. The ones with a case study link through.</p><div class="light" aria-hidden="true"></div></header>'
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
