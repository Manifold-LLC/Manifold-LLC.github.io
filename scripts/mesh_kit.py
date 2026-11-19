"""Draw the Manifold mesh for print and documents.

Writes SVG, PDF and transparent PNG files of the wireframe surface (no data
points) from several views, in several colours, into brand/mesh/.

    pip install cairosvg pillow
    python3 scripts/mesh_kit.py            # writes brand/mesh/
    python3 scripts/mesh_kit.py OUT_DIR    # writes somewhere else

The surface is the same equation as the drawing on the site, and the classic
view uses the same camera. See brand/mesh/README.md for what each design is for.
"""
import io
import math
import os
import sys

import cairosvg

PT = 72.0  # points per inch; every size below is in points


def surface(u, v):
    return 0.70*math.sin(1.15*u)*math.cos(0.85*v) + 0.20*math.sin(2.1*u + 0.7*v) - 0.10*u*v


def project(u, v, elev, azim):
    x, y, z = u, v, surface(u, v)
    ca, sa = math.cos(azim), math.sin(azim)
    x, y = x*ca - y*sa, x*sa + y*ca
    ce, se = math.cos(elev), math.sin(elev)
    y, z = y*ce - z*se, y*se + z*ce
    return x, -z, y  # screen x, screen y (down), depth (larger is farther)


def grid_lines(view):
    n_u, n_v, steps = view["grid"]
    u0, u1, v0, v1 = view.get("span", (-2.4, 2.4, -1.9, 1.9))
    e, a = view["elev"], view["azim"]
    longest = max(u1 - u0, v1 - v0)
    sv = max(24, round(steps*(v1 - v0)/longest))  # points along a line of constant u
    su = max(24, round(steps*(u1 - u0)/longest))  # points along a line of constant v
    lines = []
    for i in range(n_u + 1):
        u = u0 + (u1 - u0)*i/n_u
        lines.append([project(u, v0 + (v1 - v0)*k/sv, e, a) for k in range(sv + 1)])
    for j in range(n_v + 1):
        v = v0 + (v1 - v0)*j/n_v
        lines.append([project(u0 + (u1 - u0)*k/su, v, e, a) for k in range(su + 1)])
    return lines


def clip_polyline(pts, W, H):
    """Cut a polyline to the rectangle 0..W, 0..H (Liang-Barsky per segment)."""
    runs, cur = [], []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = x1 - x0, y1 - y0
        t0, t1, ok = 0.0, 1.0, True
        for p, q in ((-dx, x0), (dx, W - x0), (-dy, y0), (dy, H - y0)):
            if p == 0:
                if q < 0:
                    ok = False
                    break
            else:
                r = q/p
                if p < 0:
                    t0 = max(t0, r)
                else:
                    t1 = min(t1, r)
        if not ok or t0 > t1:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
            continue
        a = (x0 + t0*dx, y0 + t0*dy)
        b = (x0 + t1*dx, y0 + t1*dy)
        if not cur or abs(cur[-1][0] - a[0]) > 1e-6 or abs(cur[-1][1] - a[1]) > 1e-6:
            if len(cur) > 1:
                runs.append(cur)
            cur = [a]
        cur.append(b)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def compose(spec, colour):
    view = spec["view"]
    lines = grid_lines(view)
    xs = [p[0] for l in lines for p in l]
    ys = [p[1] for l in lines for p in l]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    bw, bh = bx1 - bx0, by1 - by0

    if spec["place"] == "fit":
        W = spec["width_in"]*PT
        m = spec.get("margin", 0.03)
        sc = W*(1 - 2*m)/bw
        H = bh*sc + 2*m*W
        ox, oy = m*W - bx0*sc, m*W - by0*sc
    elif spec["place"] == "strip":  # wider than the page, cut at the left and right edges
        W = spec["width_in"]*PT
        sc = spec["scale"]*W/bw
        pad = spec.get("pad_in", 0.06)*PT
        H = bh*sc + 2*pad
        ox, oy = spec["centre_x"]*W - (bx0 + bx1)/2*sc, pad - by0*sc
    else:  # bleed: the surface is larger than the canvas and is cut at its edges
        W, H = spec["width_in"]*PT, spec["height_in"]*PT
        sc = spec["scale"]*W/bw
        cx, cy = spec["centre"]
        ox = cx*W - (bx0 + bx1)/2*sc
        oy = cy*H - (by0 + by1)/2*sc

    near, far = spec["stroke"]
    op_near, op_far = colour["opacity"]
    if "opacity" in spec:
        op_near, op_far = op_near*spec["opacity"], op_far*spec["opacity"]

    drawn = []
    for l in lines:
        depth = sum(p[2] for p in l)/len(l)
        pts = [(ox + p[0]*sc, oy + p[1]*sc) for p in l]
        drawn.append((depth, pts))
    dmin = min(d for d, _ in drawn)
    dmax = max(d for d, _ in drawn)
    drawn.sort(key=lambda t: -t[0])  # far lines first

    paths = []
    for depth, pts in drawn:
        t = (depth - dmin)/(dmax - dmin + 1e-9)
        op = op_near - (op_near - op_far)*t
        sw = near - (near - far)*t
        runs = [pts] if spec["place"] == "fit" else clip_polyline(pts, W, H)
        for run in runs:
            d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in run)
            paths.append(f'<path d="{d}" stroke-opacity="{op:.3f}" stroke-width="{sw:.3f}"/>')

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W/PT:.3f}in" height="{H/PT:.3f}in" '
        f'viewBox="0 0 {W:.2f} {H:.2f}">',
        '<title>Manifold mesh</title>',
        f'<g fill="none" stroke="{colour["hex"]}" stroke-linecap="round" stroke-linejoin="round">',
        *paths,
        '</g>',
        '</svg>',
        '',
    ]
    return "\n".join(svg), W, H


CLASSIC = {"elev": 1.12, "azim": 0.50, "grid": (22, 15, 90)}
WAVE = {"elev": 0.48, "azim": 0.10, "grid": (22, 15, 90)}
# A long strip of the same surface, for bands that run the width of a page
STRIP = {"elev": 0.45, "azim": 0.0, "grid": (96, 8, 300), "span": (-12.0, 12.0, -0.9, 0.9)}

DESIGNS = {
    # Free-standing drawings, cropped close to the surface.
    "classic": {"view": CLASSIC, "place": "fit", "width_in": 6, "stroke": (0.75, 0.32)},
    "wave": {"view": WAVE, "place": "fit", "width_in": 7, "stroke": (0.75, 0.32)},
    "peak": {"view": {"elev": 0.62, "azim": -0.75, "grid": (22, 15, 90)},
             "place": "fit", "width_in": 7, "stroke": (0.75, 0.32)},
    "turned": {"view": {"elev": 0.95, "azim": 2.35, "grid": (22, 15, 90)},
               "place": "fit", "width_in": 6, "stroke": (0.75, 0.32)},
    "overhead": {"view": {"elev": 1.42, "azim": 0.78, "grid": (22, 18, 90),
                          "span": (-2.2, 2.2, -2.2, 2.2)},
                 "place": "fit", "width_in": 5, "stroke": (0.7, 0.3)},
    "fine": {"view": {**CLASSIC, "grid": (44, 30, 120)}, "place": "fit", "width_in": 6,
             "stroke": (0.45, 0.2)},
    "icon": {"view": {**CLASSIC, "grid": (8, 6, 60), "span": (-2.2, 2.2, -1.75, 1.75)},
             "place": "fit", "width_in": 1.5, "margin": 0.06, "stroke": (1.6, 1.0)},
    # Strips and corners that run off the edge, for headers, footers and covers.
    "band": {"view": STRIP, "place": "strip", "width_in": 8.5, "scale": 1.12, "centre_x": 0.5,
             "stroke": (0.65, 0.28)},
    "corner": {"view": CLASSIC, "place": "bleed", "width_in": 4, "height_in": 4,
               "scale": 1.6, "centre": (0.8, 0.2), "stroke": (0.75, 0.32)},
    # Full US Letter pages, to place behind a letter.
    "letter-corner": {"view": CLASSIC, "place": "bleed", "width_in": 8.5, "height_in": 11,
                      "scale": 1.15, "centre": (0.9, 0.05), "stroke": (0.75, 0.32)},
    "letter-footer": {"view": STRIP, "place": "bleed", "width_in": 8.5, "height_in": 11,
                      "scale": 1.12, "centre": (0.5, 0.95), "stroke": (0.65, 0.28)},
    "letter-watermark": {"view": CLASSIC, "place": "bleed", "width_in": 8.5, "height_in": 11,
                         "scale": 0.92, "centre": (0.5, 0.5), "stroke": (0.75, 0.32),
                         "opacity": 0.55},
}

COLOURS = {
    "ink": {"hex": "#16181d", "opacity": (0.95, 0.28)},    # near-black, the site text colour
    "navy": {"hex": "#1e3a5f", "opacity": (0.95, 0.28)},   # the site accent
    "white": {"hex": "#ffffff", "opacity": (0.95, 0.28)},  # for dark backgrounds
    "faint": {"hex": "#1e3a5f", "opacity": (0.26, 0.09)},  # pale enough to sit behind text
}


def main(out):
    for sub in ("svg", "pdf", "png"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    for name, spec in DESIGNS.items():
        for cname, colour in COLOURS.items():
            svg, W, H = compose(spec, colour)
            base = f"manifold-mesh-{name}-{cname}"
            with open(os.path.join(out, "svg", base + ".svg"), "w") as f:
                f.write(svg)
            cairosvg.svg2pdf(bytestring=svg.encode(), write_to=os.path.join(out, "pdf", base + ".pdf"))
            # 300 dpi at the drawn size, and never less than 3000 px on the long side
            scale = max(300/PT, 3000/max(W, H))
            png = cairosvg.svg2png(bytestring=svg.encode(),
                                   output_width=round(W*scale), output_height=round(H*scale))
            write_png(png, colour["hex"], scale*PT, os.path.join(out, "png", base + ".png"))
            print(base)


def write_png(png, hex_colour, dpi, path):
    """Store a one-colour drawing as a palette PNG: same pixels, about a quarter of the size.

    Every pixel is the drawing colour at some opacity, so 256 palette entries of
    that colour, one per opacity, hold the image exactly. The dpi is recorded so
    Word and Google Docs place the picture at its drawn size.
    """
    from PIL import Image
    alpha = Image.open(io.BytesIO(png)).getchannel("A")
    rgb = tuple(int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    img = alpha.copy()
    img.putpalette(list(rgb)*256)
    img.save(path, transparency=bytes(range(256)), dpi=(round(dpi), round(dpi)), optimize=True)


def preview(out):
    """One labelled sheet of every design, written to OUT/preview.png."""
    from PIL import Image, ImageDraw, ImageFont

    def font(size):
        for path in ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                     "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        return ImageFont.load_default()

    def tile(name, colour, box, text_lines=False):
        im = Image.open(os.path.join(out, "png", f"manifold-mesh-{name}-{colour}.png")).convert("RGBA")
        im.thumbnail(box, Image.LANCZOS)
        bg = Image.new("RGBA", im.size, "#1e3a5f" if colour == "white" else "#ffffff")
        bg.alpha_composite(im)
        if text_lines:  # grey bars where the letter's text would sit, on top of the drawing
            d = ImageDraw.Draw(bg)
            w, h = im.size
            step = max(6, h//48)
            for i, y in enumerate(range(int(h*0.30), int(h*0.86), step)):
                right = 0.6 if i % 6 == 5 else 0.88
                d.rectangle([int(w*0.12), y, int(w*right), y + max(2, h//160)], fill="#8a8a8a")
        return bg

    sections = [
        ("Drawings", [(n, "navy") for n in ("classic", "wave", "peak", "turned", "overhead", "fine", "icon")], 300),
        ("Bands and corners", [("band", "navy"), ("corner", "navy")], 300),
        ("Letter pages (shown with stand-in text)",
         [("letter-corner", "faint"), ("letter-footer", "navy"), ("letter-watermark", "faint"),
          ("letter-corner", "navy")], 420),
        ("Colours", [("classic", c) for c in ("ink", "navy", "faint", "white")], 300),
    ]
    W, pad, gap = 2400, 80, 40
    h1, h2, lab = font(54), font(34), font(24)
    rows = []
    for title, items, size in sections:
        tiles = []
        for n, c in items:
            box = (1100, 300) if n == "band" else (size, size)
            tiles.append((f"{n}-{c}", tile(n, c, box, text_lines=n.startswith("letter"))))
        rows.append((title, tiles))
    # lay out tiles left to right, wrapping at the sheet width
    y = pad + 110
    placed = []
    for title, tiles in rows:
        placed.append(("title", title, (pad, y)))
        y += 60
        x, row_h = pad, 0
        for label, im in tiles:
            if x + im.width > W - pad:
                x, y = pad, y + row_h + 50
                row_h = 0
            placed.append(("img", (label, im), (x, y)))
            x += im.width + gap
            row_h = max(row_h, im.height)
        y += row_h + 50 + 40
    sheet = Image.new("RGB", (W, y + pad - 40), "#eeebe3")
    d = ImageDraw.Draw(sheet)
    d.text((pad, pad), "Manifold mesh: drawings for documents", font=h1, fill="#16181d")
    for kind, what, (x, yy) in placed:
        if kind == "title":
            d.text((x, yy), what, font=h2, fill="#1e3a5f")
        else:
            label, im = what
            d.rectangle([x - 1, yy - 1, x + im.width, yy + im.height], outline="#c9c4b8")
            sheet.paste(im.convert("RGB"), (x, yy))
            d.text((x, yy + im.height + 10), label, font=lab, fill="#474b54")
    sheet.save(os.path.join(out, "preview.png"), optimize=True)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "brand/mesh"
    main(target)
    preview(target)
