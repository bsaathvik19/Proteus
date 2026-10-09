#!/usr/bin/env python3
"""Generate Proteus PWA / apple-touch icons from the brand logomark.

Draws the shape-shifter logomark (ocean ring + sea-teal morph blob + central
node) on the brand "abyss" ground, sized inside the maskable safe zone, then
supersamples 4x and downscales (LANCZOS) for smooth anti-aliased edges.

Outputs static/icon-192.png and static/icon-512.png.
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "..", "static")

# Brand palette
ABYSS = (13, 27, 42)      # #0D1B2A
OCEAN = (55, 138, 221)    # #378ADD
TEAL  = (93, 202, 165)    # #5DCAA5
MIST  = (225, 245, 238)   # #E1F5EE

# Morph blob path (viewBox 0..90), as quadratic beziers.
START = (45, 20)
SEGS = [
    ((62, 22), (68, 38)),
    ((74, 54), (60, 64)),
    ((46, 74), (32, 66)),
    ((18, 58), (20, 42)),
    ((22, 26), (38, 20)),
    ((41, 19), (45, 20)),
]


def quad(p0, p1, p2, t):
    mt = 1 - t
    x = mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0]
    y = mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1]
    return (x, y)


def blob_points(steps=40):
    pts = [START]
    p0 = START
    for c, e in SEGS:
        for i in range(1, steps + 1):
            pts.append(quad(p0, c, e, i / steps))
        p0 = e
    return pts


def render(size):
    SS = 4
    N = size * SS
    img = Image.new("RGBA", (N, N), ABYSS + (255,))
    d = ImageDraw.Draw(img)

    # Logo occupies ~73% of the icon (ring diameter ~60% — well inside the
    # maskable 80% safe zone). Center the 90-unit viewBox on the icon centre.
    frac = 0.73
    scale = frac * N / 90.0
    cx = cy = N / 2.0

    def tx(p):
        return (cx + (p[0] - 45) * scale, cy + (p[1] - 45) * scale)

    # Morph blob — filled sea teal.
    d.polygon([tx(p) for p in blob_points()], fill=TEAL + (255,))

    # Outer ring — ocean blue stroke.
    r = 37 * scale
    ring_w = max(2, int(round(3.5 * scale)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=OCEAN + (255,), width=ring_w)

    # Central node — the constant self. Mist disc + ocean core (pops on teal).
    rn = 7.0 * scale
    d.ellipse([cx - rn, cy - rn, cx + rn, cy + rn], fill=MIST + (255,))
    ri = 3.2 * scale
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=OCEAN + (255,))

    return img.resize((size, size), Image.LANCZOS)


for sz in (192, 512):
    out = os.path.join(STATIC, f"icon-{sz}.png")
    render(sz).save(out, "PNG")
    print("wrote", os.path.normpath(out))

# favicon.png (notification icon) + favicon.ico (multi-size; also resolves the
# browser's automatic /favicon.ico request).
png = os.path.join(STATIC, "favicon.png")
render(128).save(png, "PNG")
print("wrote", os.path.normpath(png))

ico = os.path.join(STATIC, "favicon.ico")
render(256).save(ico, sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote", os.path.normpath(ico))
