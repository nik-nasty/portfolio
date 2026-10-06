#!/usr/bin/env python3
"""Generates the iridescent purple textures used as the hero and the case study covers.

Run from the repo root: python3 _build/textures.py
Writes assets/hero.jpg and assets/cover-<slug>.jpg
"""
import os, sys
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from content import CASES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)


def noise(rng, h, w, sigma):
    n = rng.standard_normal((h, w)).astype(np.float32)
    n = gaussian_filter(n, sigma)
    n -= n.min()
    n /= max(n.max(), 1e-6)
    return n


def ramp(t, stops):
    """t in 0..1 -> rgb float array via piecewise linear colour stops."""
    xs = np.array([s[0] for s in stops], dtype=np.float32)
    cs = np.array([s[1] for s in stops], dtype=np.float32) / 255.0
    out = np.zeros(t.shape + (3,), dtype=np.float32)
    for c in range(3):
        out[..., c] = np.interp(t, xs, cs[:, c])
    return out


def veins(rng, h, w, npts, warp, width):
    """Wing-like cell edges: distance to nearest minus second nearest Voronoi seed, warped by noise."""
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    wx = (noise(rng, h, w, 60) - 0.5) * warp
    wy = (noise(rng, h, w, 60) - 0.5) * warp
    px = xs + wx
    py = ys + wy
    pts = rng.uniform([0, 0], [w, h], size=(npts, 2)).astype(np.float32)
    d1 = np.full((h, w), 1e9, dtype=np.float32)
    d2 = np.full((h, w), 1e9, dtype=np.float32)
    for (x, y) in pts:
        d = np.sqrt((px - x) ** 2 + (py - y) ** 2)
        m = d < d1
        d2 = np.where(m, d1, np.minimum(d2, d))
        d1 = np.where(m, d, d1)
    edge = np.clip(1.0 - (d2 - d1) / width, 0, 1)
    return gaussian_filter(edge, 0.8)


def texture(seed, w, h, hue_shift=0.0, sheen=1.0, bright=1.0):
    rng = np.random.default_rng(seed)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    u = xs / w
    v = ys / h
    # large soft light field, mid detail, fine shimmer
    n = 0.55 * noise(rng, h, w, w / 6) + 0.3 * noise(rng, h, w, w / 22) + 0.15 * noise(rng, h, w, w / 90)
    n -= n.min(); n /= n.max()
    # patchy mask so parts of the field stay deep purple
    mask = noise(rng, h, w, w / 5)
    mask = np.clip((mask - 0.42) * 2.2, 0, 1) ** 1.3
    # one beam of light crossing the field diagonally
    ang = rng.uniform(0.25, 0.75)
    d = u * ang + v * (1 - ang)
    centre = rng.uniform(0.35, 0.7)
    beam = np.exp(-((d - centre) / 0.16) ** 2) * (0.6 + 0.4 * noise(rng, h, w, w / 10))
    lit = np.clip(n * (0.30 + 0.62 * mask) * sheen + beam * 0.30, 0, 1)

    # base purple ramp
    base = ramp(np.clip(lit * 0.75, 0, 1), [(0.00, (22, 12, 36)), (0.25, (40, 24, 66)), (0.5, (78, 50, 122)), (0.75, (128, 92, 176)), (1.0, (176, 142, 212))])

    # iridescent film: three tints chosen by slow noise, like oil on a wing
    a = noise(rng, h, w, w / 7); b = noise(rng, h, w, w / 9); c = noise(rng, h, w, w / 11)
    tot = a + b + c + 1e-6
    pink = np.array([240, 180, 214]) / 255.0
    aqua = np.array([176, 220, 236]) / 255.0
    gold = np.array([240, 206, 166]) / 255.0
    if hue_shift > 0:
        a = a * (1 + hue_shift)
    elif hue_shift < 0:
        b = b * (1 - hue_shift)
    tot = a + b + c + 1e-6
    film = (a / tot)[..., None] * pink + (b / tot)[..., None] * aqua + (c / tot)[..., None] * gold
    amt = np.clip((lit - 0.45) / 0.55, 0, 1) ** 1.3 * 0.95
    img = base * (1 - amt[..., None]) + film * amt[..., None]

    # veins: fine warm lines, stronger where the field is light (as on a wing)
    vn = veins(rng, h, w, npts=int(22 * (w / 1600)), warp=140, width=1.7)
    v2 = veins(rng, h, w, npts=int(110 * (w / 1600)), warp=60, width=1.1) * 0.6
    vv = np.clip(vn + v2, 0, 1) * (0.10 + 0.55 * np.clip(lit - 0.2, 0, 1))
    vein_col = np.array([70, 36, 44], dtype=np.float32) / 255.0
    img = img * (1 - vv[..., None] * 0.6) + vein_col * (vv[..., None] * 0.6)

    # specular sheen on the brightest patches
    spec = gaussian_filter(np.clip(lit - 0.78, 0, 1) * 3.0, w / 140)
    img += spec[..., None] * np.array([0.12, 0.10, 0.08], dtype=np.float32)

    # vignette and brightness
    r = np.sqrt((u - 0.5) ** 2 + (v - 0.5) ** 2)
    vig = 1 - np.clip((r - 0.38) * 0.8, 0, 0.4)
    img *= vig[..., None] * bright

    # grain
    img += rng.standard_normal((h, w, 1)).astype(np.float32) * 0.012
    img = np.clip(img, 0, 1)
    return Image.fromarray((img * 255).astype(np.uint8), "RGB")


if __name__ == "__main__":
    hero = texture(seed=7, w=1920, h=1200, hue_shift=0.6, sheen=1.25, bright=1.0)
    hero.save(os.path.join(OUT, "hero.jpg"), quality=84, optimize=True, progressive=True)
    print("assets/hero.jpg")
    for i, c in enumerate(CASES):
        im = texture(seed=100 + i * 13, w=1600, h=1000, hue_shift=(i % 3) * 0.5 - 0.5, sheen=1.3 + (i % 4) * 0.12, bright=1.0)
        p = os.path.join(OUT, f"cover-{c['slug']}.jpg")
        im.save(p, quality=82, optimize=True, progressive=True)
        print(f"assets/cover-{c['slug']}.jpg", os.path.getsize(p) // 1024, "KB")
