# Manifold mesh: notes for an agent

This folder is self-contained. Give the whole folder to an agent; nothing outside it is needed.

## What it is

The wireframe surface from manifold-llc.com, without data points: grid lines on the surface
`z = 0.70 sin(1.15u) cos(0.85v) + 0.20 sin(2.1u + 0.7v) - 0.10uv`, seen from a chosen camera.
Nearer lines are darker and heavier, which is what makes it read as 3D. Keep that depth cue and
keep the equation; everything else (angle, crop, size, colour, line weight, fade) is free to change.

## Files

| Path | What it is |
|---|---|
| `mesh_kit.py` | The source of every drawing. Standard-library Python for SVG; PDF and PNG need `pip install cairosvg pillow`. |
| `svg/`, `pdf/`, `png/` | 12 designs x 4 colours, named `manifold-mesh-<design>-<colour>.<ext>`. |
| `mesh-geometry.json` | Raw grid lines of the `classic` design: surface points (u, v, z), canvas points (x, y) and depth. |
| `preview.png` | Every design on one sheet. |
| `README.md` | Guide for people: which file to use where, Word and Google Docs steps. |

## Redraw, don't edit

To change a drawing, run `mesh_kit.py` again with different options rather than editing SVG text.
Every SVG records the options that drew it in its `<desc>` element (a JSON object with a
`command` field when drawn from the command line), so start from that.

```bash
python3 mesh_kit.py list                                   # designs, views, colours
python3 mesh_kit.py draw -d classic -c navy -o out.svg     # same as svg/manifold-mesh-classic-navy.svg
```

Output type follows the extension: `.svg`, `.pdf` or `.png`. The command prints the drawn size.

## Recipes

| Want | Command |
|---|---|
| Another colour | `draw -d classic -c "#2F8BFF" -o x.svg` (or a name: `electric`, `letter-navy`, `graphite`, ...) |
| Heavier lines for a small print size | `draw -d classic --stroke-scale 2.5 --width-in 2 -o x.png` |
| Exact line widths (points) | `draw -d classic --stroke 1.2 0.5 -o x.svg` (nearest, farthest) |
| Paler or stronger | `draw -d classic --opacity 0.5 0.15 -o x.svg` (nearest, farthest) |
| Another angle | `draw -d classic --elev 0.8 --azim 1.2 -o x.svg` (radians; elev 0 is edge-on, 1.57 straight down) |
| More or fewer lines | `draw -d classic --grid 30 20 -o x.svg` |
| A different part of the surface | `draw -d classic --span -3 3 -1 1 -o x.svg` (u0 u1 v0 v1) |
| A crop that runs off the edges | `draw -d classic --place bleed --width-in 4 --height-in 1.2 --scale 1.4 --centre 0.6 0.4 -o x.svg` |
| Fade in from the left | `draw -d band --fade 0.1 0.55 -o x.svg` (transparent at 10% of the width, full at 55%) |
| Fade out to the right | `draw -d band --fade 0.9 0.5 -o x.svg` |
| A PNG at a given resolution | `draw -d classic -o x.png --dpi 600` (transparent unless `--background "#ffffff"`) |
| Raw coordinates to draw your own way | `geometry -d classic -o lines.json` (takes the same view and placement options) |
| Redraw this whole folder | `kit` |

Sizes: `--width-in` sets the canvas width in inches. With `--place fit` (the free-standing designs)
the height follows from the drawing; `strip` (the band) is cut at both sides; `bleed` needs
`--height-in` and is cut on every side it crosses. Line widths are in points at the drawn size,
so if you scale a drawing after drawing it, its lines scale too; redraw at the target size instead.

## Colours

Kit colours (drawn into the folders): `navy` #1e3a5f and `ink` #16181d from the website, `white`
for dark backgrounds, `faint` (navy at about a quarter strength, for use under text).
Named colours for `draw`: `letter-navy` #142133 (offer letters), and the brand board:
`near-black` #0B0C0D, `charcoal` #1A1E22, `graphite` #2E3238, `gunmetal` #4A5058, `silver` #C9CDD3,
`off-white` #E8EAED, `electric` #2F8BFF.

## SVG structure

- Units are points (1/72 in); `width` and `height` are in inches.
- `<g id="mesh">` carries the colour (`stroke`) and the round caps and joins. Recolour there; if the
  drawing fades, the colour is in the `<linearGradient id="fade">` stops instead.
- Each `<path>` is one grid line: `data-line="u7"` (u held fixed) or `v3`; `data-depth` 0 is the
  nearest line and 1 the farthest; paths are ordered far to near. Opacity and width are per path.
- `bleed` and `strip` designs are cut to the canvas in the geometry, not with a clip path, so they
  survive any renderer.

## Placing in Word

Word on desktop shows SVG; some mobile and preview viewers do not, and floating (anchored) pictures
can move in mobile viewers. For a header that must look the same everywhere, use an inline PNG at
300 dpi or more, drawn at the size it will be shown.
