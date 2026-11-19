#!/usr/bin/env python3
"""Draw the Manifold mesh: the wireframe surface from manifold-llc.com, without data points.

This one file is the source of every drawing in this folder. It needs only the
Python standard library to write SVG; PDF and PNG need `pip install cairosvg pillow`.

    python3 mesh_kit.py list                      # designs, colours, views
    python3 mesh_kit.py draw -d classic -c navy -o mesh.svg
    python3 mesh_kit.py draw -d band -c "#2F8BFF" --stroke-scale 1.6 -o band.png --dpi 600
    python3 mesh_kit.py draw -d classic --elev 0.8 --azim 1.2 --width-in 3 --fade 0 0.5 -o x.pdf
    python3 mesh_kit.py geometry -d classic -o mesh.json   # raw 3D and 2D line coordinates
    python3 mesh_kit.py kit                       # redraw the whole folder (svg/, pdf/, png/, preview.png)

See AGENTS.md in this folder for what each option does and common recipes.
"""
import argparse
import io
import json
import math
import os
import sys
from xml.sax.saxutils import escape

PT = 72.0  # points per inch; sizes inside the SVG are in points
HERE = os.path.dirname(os.path.abspath(__file__))
EQUATION = "z = 0.70*sin(1.15u)*cos(0.85v) + 0.20*sin(2.1u + 0.7v) - 0.10*u*v"


def surface(u, v):
    return 0.70*math.sin(1.15*u)*math.cos(0.85*v) + 0.20*math.sin(2.1*u + 0.7*v) - 0.10*u*v


def project(u, v, elev, azim):
    """Turn the surface by azim about the vertical axis, tilt it by elev, and look along y.

    Returns screen x, screen y (pointing down) and depth (larger is farther)."""
    x, y, z = u, v, surface(u, v)
    ca, sa = math.cos(azim), math.sin(azim)
    x, y = x*ca - y*sa, x*sa + y*ca
    ce, se = math.cos(elev), math.sin(elev)
    y, z = y*ce - z*se, y*se + z*ce
    return x, -z, y


# ----------------------------------------------------------------------------
# Views: where the camera is and which part of the surface is drawn.
#   elev  tilt in radians: 0 looks at the surface edge-on, pi/2 looks straight down
#   azim  turn in radians about the vertical axis
#   grid  (lines of constant u, lines of constant v, points along the longest line)
#   span  (u min, u max, v min, v max)
SPAN = (-2.4, 2.4, -1.9, 1.9)
VIEWS = {
    "classic": {"elev": 1.12, "azim": 0.50, "grid": (22, 15, 90), "span": SPAN},
    "wave": {"elev": 0.48, "azim": 0.10, "grid": (22, 15, 90), "span": SPAN},
    "peak": {"elev": 0.62, "azim": -0.75, "grid": (22, 15, 90), "span": SPAN},
    "turned": {"elev": 0.95, "azim": 2.35, "grid": (22, 15, 90), "span": SPAN},
    "overhead": {"elev": 1.42, "azim": 0.78, "grid": (22, 18, 90), "span": (-2.2, 2.2, -2.2, 2.2)},
    "fine": {"elev": 1.12, "azim": 0.50, "grid": (44, 30, 120), "span": SPAN},
    "icon": {"elev": 1.12, "azim": 0.50, "grid": (8, 6, 60), "span": (-2.2, 2.2, -1.75, 1.75)},
    # a long strip of the same surface, for bands that run the width of a page
    "strip": {"elev": 0.45, "azim": 0.0, "grid": (96, 8, 300), "span": (-12.0, 12.0, -0.9, 0.9)},
}

# ----------------------------------------------------------------------------
# Designs: a view plus how it sits on its canvas.
#   place "fit"    canvas is width_in wide and as tall as the drawing needs
#         "strip"  canvas is width_in wide; the drawing is `scale` times wider and is cut at both sides
#         "bleed"  canvas is width_in x height_in; the drawing is `scale` times the canvas width,
#                  centred at `centre` (fractions of the canvas), and cut at the edges
#   stroke         line width in points at the drawn size, (nearest, farthest)
#   opacity        multiplies the colour's opacities (letter-watermark is paler)
DESIGNS = {
    "classic": {"view": "classic", "place": "fit", "width_in": 6, "stroke": (0.75, 0.32)},
    "wave": {"view": "wave", "place": "fit", "width_in": 7, "stroke": (0.75, 0.32)},
    "peak": {"view": "peak", "place": "fit", "width_in": 7, "stroke": (0.75, 0.32)},
    "turned": {"view": "turned", "place": "fit", "width_in": 6, "stroke": (0.75, 0.32)},
    "overhead": {"view": "overhead", "place": "fit", "width_in": 5, "stroke": (0.7, 0.3)},
    "fine": {"view": "fine", "place": "fit", "width_in": 6, "stroke": (0.45, 0.2)},
    "icon": {"view": "icon", "place": "fit", "width_in": 1.5, "margin": 0.06, "stroke": (1.6, 1.0)},
    "band": {"view": "strip", "place": "strip", "width_in": 8.5, "scale": 1.12, "centre": (0.5, 0.5),
             "stroke": (0.65, 0.28)},
    "corner": {"view": "classic", "place": "bleed", "width_in": 4, "height_in": 4,
               "scale": 1.6, "centre": (0.8, 0.2), "stroke": (0.75, 0.32)},
    "letter-corner": {"view": "classic", "place": "bleed", "width_in": 8.5, "height_in": 11,
                      "scale": 1.15, "centre": (0.9, 0.05), "stroke": (0.75, 0.32)},
    "letter-footer": {"view": "strip", "place": "bleed", "width_in": 8.5, "height_in": 11,
                      "scale": 1.12, "centre": (0.5, 0.95), "stroke": (0.65, 0.28)},
    "letter-watermark": {"view": "classic", "place": "bleed", "width_in": 8.5, "height_in": 11,
                         "scale": 0.92, "centre": (0.5, 0.5), "stroke": (0.75, 0.32), "opacity": 0.55},
}

# ----------------------------------------------------------------------------
# Colours. Opacity runs from the nearest line to the farthest, which gives the depth.
# The first four are drawn into this folder by `kit`; any of these names, or any
# #rrggbb value, works with `draw`.
COLOURS = {
    "ink": {"hex": "#16181d", "opacity": (0.95, 0.28)},    # site text colour
    "navy": {"hex": "#1e3a5f", "opacity": (0.95, 0.28)},   # site accent
    "white": {"hex": "#ffffff", "opacity": (0.95, 0.28)},  # for dark backgrounds
    "faint": {"hex": "#1e3a5f", "opacity": (0.26, 0.09)},  # pale enough to sit under text
}
KIT_COLOURS = ["ink", "navy", "white", "faint"]
NAMED = {  # brand board and letter colours, usable by name with `draw`
    "letter-navy": "#142133", "near-black": "#0B0C0D", "charcoal": "#1A1E22", "graphite": "#2E3238",
    "gunmetal": "#4A5058", "silver": "#C9CDD3", "off-white": "#E8EAED", "electric": "#2F8BFF",
}


def colour_of(name_or_hex, opacity=None):
    if name_or_hex in COLOURS:
        c = dict(COLOURS[name_or_hex])
    elif name_or_hex in NAMED:
        c = {"hex": NAMED[name_or_hex], "opacity": (0.95, 0.28)}
    elif name_or_hex.startswith("#") and len(name_or_hex) == 7:
        c = {"hex": name_or_hex, "opacity": (0.95, 0.28)}
    else:
        sys.exit(f"unknown colour {name_or_hex!r}; use a name from `list` or #rrggbb")
    if opacity:
        c["opacity"] = tuple(opacity)
    return c


# ----------------------------------------------------------------------------
def grid_lines(view):
    """Every grid line of the surface: kind ('u' or 'v'), index, and points (u, v, z, x, y, depth)."""
    n_u, n_v, steps = view["grid"]
    u0, u1, v0, v1 = view["span"]
    e, a = view["elev"], view["azim"]
    longest = max(u1 - u0, v1 - v0)
    sv = max(24, round(steps*(v1 - v0)/longest))  # points along a line of constant u
    su = max(24, round(steps*(u1 - u0)/longest))  # points along a line of constant v

    def point(u, v):
        return (u, v, surface(u, v)) + project(u, v, e, a)

    lines = []
    for i in range(n_u + 1):
        u = u0 + (u1 - u0)*i/n_u
        lines.append({"kind": "u", "index": i, "value": u,
                      "points": [point(u, v0 + (v1 - v0)*k/sv) for k in range(sv + 1)]})
    for j in range(n_v + 1):
        v = v0 + (v1 - v0)*j/n_v
        lines.append({"kind": "v", "index": j, "value": v,
                      "points": [point(u0 + (u1 - u0)*k/su, v) for k in range(su + 1)]})
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


def layout(spec):
    """Place the drawing on its canvas. Returns lines, canvas size and the screen-to-canvas mapping."""
    view = spec["view"]
    lines = grid_lines(view)
    xs = [p[3] for l in lines for p in l["points"]]
    ys = [p[4] for l in lines for p in l["points"]]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    bw, bh = bx1 - bx0, by1 - by0
    W = spec["width_in"]*PT
    if spec["place"] == "fit":
        m = spec.get("margin", 0.03)
        sc = W*(1 - 2*m)/bw
        H = bh*sc + 2*m*W
        ox, oy = m*W - bx0*sc, m*W - by0*sc
    elif spec["place"] == "strip":
        sc = spec["scale"]*W/bw
        pad = spec.get("pad_in", 0.06)*PT
        H = bh*sc + 2*pad
        ox, oy = spec["centre"][0]*W - (bx0 + bx1)/2*sc, pad - by0*sc
    else:  # bleed
        H = spec["height_in"]*PT
        sc = spec["scale"]*W/bw
        cx, cy = spec["centre"]
        ox, oy = cx*W - (bx0 + bx1)/2*sc, cy*H - (by0 + by1)/2*sc
    return lines, W, H, (sc, ox, oy)


def compose(spec, colour, command=None):
    """Return (svg text, width pt, height pt) for a design spec and a colour."""
    lines, W, H, (sc, ox, oy) = layout(spec)
    k = spec.get("stroke_scale", 1.0)
    near, far = spec["stroke"][0]*k, spec["stroke"][1]*k
    op_near, op_far = colour["opacity"]
    m = spec.get("opacity", 1.0)
    op_near, op_far = op_near*m, op_far*m

    depths = [sum(p[5] for p in l["points"])/len(l["points"]) for l in lines]
    dmin, dmax = min(depths), max(depths)
    order = sorted(range(len(lines)), key=lambda i: -depths[i])  # far lines first

    paths = []
    for i in order:
        l = lines[i]
        t = (depths[i] - dmin)/(dmax - dmin + 1e-9)  # 0 nearest, 1 farthest
        op = op_near - (op_near - op_far)*t
        sw = near - (near - far)*t
        pts = [(ox + p[3]*sc, oy + p[4]*sc) for p in l["points"]]
        runs = [pts] if spec["place"] == "fit" else clip_polyline(pts, W, H)
        for run in runs:
            d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in run)
            paths.append(f'<path data-line="{l["kind"]}{l["index"]}" data-depth="{t:.3f}" '
                         f'stroke-opacity="{op:.3f}" stroke-width="{sw:.3f}" d="{d}"/>')

    stroke, defs = colour["hex"], []
    if spec.get("fade"):
        f0, f1 = spec["fade"]
        flip = f0 > f1  # fade out to the right instead of the left
        a, b = (f1, f0) if flip else (f0, f1)
        s0, s1 = ("1", "0") if flip else ("0", "1")
        defs.append(f'<defs><linearGradient id="fade" gradientUnits="userSpaceOnUse" x1="{a*W:.2f}" y1="0" '
                    f'x2="{b*W:.2f}" y2="0"><stop offset="0" stop-color="{colour["hex"]}" stop-opacity="{s0}"/>'
                    f'<stop offset="1" stop-color="{colour["hex"]}" stop-opacity="{s1}"/></linearGradient></defs>')
        stroke = "url(#fade)"

    note = [
        "Manifold mesh: the wireframe surface from manifold-llc.com, drawn by mesh_kit.py.",
        f"Surface: {EQUATION}",
        "Each <path> is one grid line: data-line is u<i> (u held fixed) or v<j> (v held fixed);",
        "data-depth runs from 0 (nearest) to 1 (farthest). Nearer lines are darker and heavier.",
        "Recolour: change stroke on <g id=\"mesh\"> (or the gradient stops if it fades).",
        "Units are points (1/72 in). The settings and command that drew it are in <desc>.",
        "Redraw rather than edit: see AGENTS.md.",
    ]
    params = {k2: v for k2, v in spec.items() if k2 != "view"}
    params["view"] = spec["view"]
    params["colour"] = colour
    if command:
        params["command"] = command  # kept out of the comment above: XML comments cannot hold "--"
    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!--\n  " + "\n  ".join(note) + "\n-->",
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W/PT:.3f}in" height="{H/PT:.3f}in" '
        f'viewBox="0 0 {W:.2f} {H:.2f}">',
        "<title>Manifold mesh</title>",
        f"<desc>{escape(json.dumps(params))}</desc>",
        *defs,
        f'<g id="mesh" fill="none" stroke="{stroke}" stroke-linecap="round" stroke-linejoin="round">',
        *paths,
        "</g>",
        "</svg>",
        "",
    ]
    return "\n".join(svg), W, H


# ----------------------------------------------------------------------------
def write(svg, W, H, path, hex_colour, dpi=None, background=None):
    """Write svg to path; the extension picks the format (.svg, .pdf or .png)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".svg":
        with open(path, "w") as f:
            f.write(svg)
        return
    try:
        import cairosvg
    except ImportError:
        sys.exit("PDF and PNG need cairosvg: pip install cairosvg pillow (or write .svg and convert it)")
    if ext == ".pdf":
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=path)
    elif ext == ".png":
        # default: 300 dpi at the drawn size, and never less than 3000 px on the long side
        scale = dpi/PT if dpi else max(300/PT, 3000/max(W, H))
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=round(W*scale),
                               output_height=round(H*scale), background_color=background)
        write_png(png, hex_colour, scale*PT, path, background)
    else:
        sys.exit(f"unknown output type {ext!r}; use .svg, .pdf or .png")


def write_png(png, hex_colour, dpi, path, background=None):
    """Store a one-colour drawing as a palette PNG: same pixels, about a quarter of the size.

    Every pixel is the drawing colour at some opacity, so 256 palette entries of that
    colour, one per opacity, hold it exactly. The dpi is recorded so Word and Google
    Docs place the picture at its drawn size."""
    from PIL import Image
    im = Image.open(io.BytesIO(png))
    d = (round(dpi), round(dpi))
    if background:
        im.convert("RGB").save(path, dpi=d, optimize=True)
        return
    img = im.getchannel("A").copy()
    rgb = tuple(int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    img.putpalette(list(rgb)*256)
    img.save(path, transparency=bytes(range(256)), dpi=d, optimize=True)


def kit(out):
    for sub in ("svg", "pdf", "png"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    for name in DESIGNS:
        for cname in KIT_COLOURS:
            spec = resolve(name)
            colour = COLOURS[cname]
            svg, W, H = compose(spec, colour, f"python3 mesh_kit.py draw -d {name} -c {cname} -o OUT.svg")
            base = f"manifold-mesh-{name}-{cname}"
            for ext in ("svg", "pdf", "png"):
                write(svg, W, H, os.path.join(out, ext, f"{base}.{ext}"), colour["hex"])
            print(base)
    geometry_file(resolve("classic"), os.path.join(out, "mesh-geometry.json"))
    preview(out)


def geometry_file(spec, path):
    """Write the raw lines: 3D surface points and their 2D position on the design's canvas."""
    lines, W, H, (sc, ox, oy) = layout(spec)
    data = {
        "about": "Manifold mesh grid lines. 'uvz' are points on the surface; 'xy' are the same points on "
                 "the canvas in points (1/72 in), origin top left, y down. 'depth' is the camera distance "
                 "(larger is farther). Lines are not clipped to the canvas.",
        "equation": EQUATION,
        "design": {k: v for k, v in spec.items()},
        "canvas_pt": [round(W, 2), round(H, 2)],
        "lines": [{"kind": l["kind"], "index": l["index"], "value": round(l["value"], 4),
                   "uvz": [[round(p[0], 4), round(p[1], 4), round(p[2], 4)] for p in l["points"]],
                   "xy": [[round(ox + p[3]*sc, 2), round(oy + p[4]*sc, 2)] for p in l["points"]],
                   "depth": [round(p[5], 4) for p in l["points"]]} for l in lines],
    }
    with open(path, "w") as f:
        json.dump(data, f, separators=(",", ":"))


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
    y = pad + 110
    placed = []
    for title, items, size in sections:
        placed.append(("title", title, (pad, y)))
        y += 60
        x, row_h = pad, 0
        for n, c in items:
            box = (1100, 300) if n == "band" else (size, size)
            im = tile(n, c, box, text_lines=n.startswith("letter"))
            if x + im.width > W - pad:
                x, y = pad, y + row_h + 50
                row_h = 0
            placed.append(("img", (f"{n}-{c}", im), (x, y)))
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


# ----------------------------------------------------------------------------
def resolve(design, args=None):
    """A design's settings, with any command-line overrides applied."""
    spec = dict(DESIGNS[design])
    spec["view"] = dict(VIEWS[spec["view"]])
    if args is None:
        return spec
    v = spec["view"]
    for key in ("elev", "azim"):
        if getattr(args, key) is not None:
            v[key] = getattr(args, key)
    if args.grid:
        v["grid"] = (args.grid[0], args.grid[1], v["grid"][2])
    if args.steps:
        v["grid"] = (v["grid"][0], v["grid"][1], args.steps)
    if args.span:
        v["span"] = tuple(args.span)
    for key in ("place", "width_in", "height_in", "scale", "margin"):
        if getattr(args, key) is not None:
            spec[key] = getattr(args, key)
    if args.centre:
        spec["centre"] = tuple(args.centre)
    if args.stroke:
        spec["stroke"] = tuple(args.stroke)
    if args.stroke_scale:
        spec["stroke_scale"] = args.stroke_scale
    if args.fade:
        spec["fade"] = tuple(args.fade)
    if spec["place"] == "bleed" and "height_in" not in spec:
        sys.exit("--place bleed needs --height-in")
    if spec["place"] != "fit" and "scale" not in spec:
        spec["scale"] = 1.0
    if spec["place"] != "fit" and "centre" not in spec:
        spec["centre"] = (0.5, 0.5)
    return spec


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="show designs, views and colours")
    k = sub.add_parser("kit", help="redraw every file in this folder")
    k.add_argument("out", nargs="?", default=HERE)
    for name in ("draw", "geometry"):
        q = sub.add_parser(name, help="draw one file" if name == "draw" else "write raw line coordinates as JSON")
        q.add_argument("-d", "--design", default="classic", choices=sorted(DESIGNS))
        q.add_argument("-o", "--out", required=True, help=".svg, .pdf or .png (draw); .json (geometry)")
        q.add_argument("--elev", type=float, help="tilt in radians (0 edge-on, 1.57 straight down)")
        q.add_argument("--azim", type=float, help="turn in radians about the vertical axis")
        q.add_argument("--grid", type=int, nargs=2, metavar=("NU", "NV"), help="number of grid lines")
        q.add_argument("--steps", type=int, help="points along the longest line (smoothness)")
        q.add_argument("--span", type=float, nargs=4, metavar=("U0", "U1", "V0", "V1"))
        q.add_argument("--place", choices=["fit", "strip", "bleed"])
        q.add_argument("--width-in", type=float, help="canvas width in inches")
        q.add_argument("--height-in", type=float, help="canvas height in inches (bleed)")
        q.add_argument("--scale", type=float, help="drawing width as a multiple of canvas width (strip, bleed)")
        q.add_argument("--centre", type=float, nargs=2, metavar=("CX", "CY"),
                       help="drawing centre as fractions of the canvas (bleed; CX for strip)")
        q.add_argument("--margin", type=float, help="margin as a fraction of the width (fit)")
        if name == "draw":
            q.add_argument("-c", "--colour", default="navy", help="name from `list` or #rrggbb")
            q.add_argument("--opacity", type=float, nargs=2, metavar=("NEAR", "FAR"))
            q.add_argument("--stroke", type=float, nargs=2, metavar=("NEAR", "FAR"), help="line widths in points")
            q.add_argument("--stroke-scale", type=float, help="multiply line widths, e.g. 2 for a small print size")
            q.add_argument("--fade", type=float, nargs=2, metavar=("X0", "X1"),
                           help="fade in from transparent at X0 to full at X1 (fractions of the width); "
                                "X0 > X1 fades out to the right")
            q.add_argument("--dpi", type=float, help="PNG resolution at the drawn size")
            q.add_argument("--background", help="PNG background colour; default transparent")
        else:
            for opt in ("stroke", "stroke_scale", "fade"):
                q.set_defaults(**{opt: None})
    a = p.parse_args(argv)

    if a.cmd == "list":
        print("designs:", ", ".join(DESIGNS))
        for n, d in DESIGNS.items():
            print(f"  {n:17} view={d['view']:8} place={d['place']:6} width={d['width_in']} in")
        print("views:", ", ".join(VIEWS))
        print("colours (drawn by kit):", ", ".join(f"{n} {COLOURS[n]['hex']}" for n in KIT_COLOURS))
        print("more colours by name:", ", ".join(f"{n} {h}" for n, h in NAMED.items()))
        return
    if a.cmd == "kit":
        kit(a.out)
        return
    spec = resolve(a.design, a)
    if a.cmd == "geometry":
        geometry_file(spec, a.out)
        return
    colour = colour_of(a.colour, a.opacity)
    command = "python3 mesh_kit.py " + " ".join(sys.argv[1:] if argv is None else argv)
    svg, W, H = compose(spec, colour, command)
    write(svg, W, H, a.out, colour["hex"], a.dpi, a.background)
    print(f"{a.out}: {W/PT:.2f} x {H/PT:.2f} in")


if __name__ == "__main__":
    main()
