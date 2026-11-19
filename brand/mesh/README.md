# Manifold mesh: drawings for documents

The wireframe surface from the home page, without the data points, drawn for offer letters, proposals, slides and anything else printed or shared. `preview.png` shows every design.

Every design comes in four colours and three formats, named `manifold-mesh-<design>-<colour>.<format>`.

## Designs

| Design | Drawn size | Good for |
|---|---|---|
| `classic` | 6 in wide | The drawing on the home page. The default choice. |
| `wave` | 7 in wide | A low side view, wide and short. Section headers, slide titles. |
| `peak` | 7 in wide | A low view from the other side, showing the ridge. Covers, title slides. |
| `turned` | 6 in wide | The surface seen from behind. A change from `classic` in the same document. |
| `overhead` | 5 in wide | Looking down on the surface. A quiet texture for backgrounds. |
| `fine` | 6 in wide | `classic` with twice the lines, drawn thinner. Large backgrounds. |
| `icon` | 1.5 in wide | Few, heavy lines that stay clear when small. Email signatures, badges, footers. |
| `band` | 8.5 x 1.5 in | A strip that runs off both sides. The top or bottom of a letterhead. |
| `corner` | 4 x 4 in | Runs off the top and right edges. Covers and title slides. |
| `letter-corner` | 8.5 x 11 in | A whole letter page with the mesh in the top right corner. |
| `letter-footer` | 8.5 x 11 in | A whole letter page with the strip along the bottom. |
| `letter-watermark` | 8.5 x 11 in | A whole letter page with a pale drawing in the middle, under the text. |

## Colours

| Colour | Use |
|---|---|
| `navy` | The site accent, #1e3a5f. The default choice. |
| `ink` | Near-black, #16181d. Black-and-white printing, faxes, scans. |
| `faint` | Navy at about a quarter strength. Pale enough to sit under text. Use it for watermarks and letter pages. |
| `white` | For dark backgrounds and slides. Looks blank on a white page; that is expected. |

Lines nearer the viewer are darker and heavier, as on the site, so the transparent files show the surface's depth on any background.

## Formats

| Folder | Format | Use it in |
|---|---|---|
| `svg/` | Vector | Word and PowerPoint (Microsoft 365), Keynote, Figma, Illustrator, Inkscape, web pages. Stays sharp at any size. |
| `pdf/` | Vector | Print shops, Illustrator, InDesign, Affinity, LaTeX. Stays sharp at any size. |
| `png/` | Transparent image, 300 dpi or better | Google Docs and Slides, older Word, email signatures, anywhere SVG is refused. |

Line weights are set for the drawn size. Shrinking a drawing to a third of its size or less makes the far lines faint; use `icon` for small sizes.

## Putting a letter page behind a letter in Word

1. Double-click the top margin to open the header.
2. Insert > Pictures > This Device, and choose `svg/manifold-mesh-letter-corner-faint.svg` (or another `letter-` file).
3. With the picture selected: Picture Format > Wrap Text > Behind Text.
4. Picture Format > Size: 8.5 in wide, 11 in high. Then Position > More Layout Options: horizontal 0 in to the right of Page, vertical 0 in below Page.
5. Close the header. Because the picture sits in the header it appears on every page. For the first page only, tick Different First Page and place it in the first-page header.

The same steps with a `band` file make a letterhead strip; skip the resizing in step 4.

## Google Docs

Google Docs does not accept SVG; use the `png/` files. Insert > Image > Upload from computer, then choose Behind text in the bar under the picture and drag it into place.

## Printing

Most office printers leave about a quarter inch unprinted at the edge of the sheet, so the designs that run off the page stop short of the edge there. A print shop can print to the edge (ask for full bleed); give them the PDF.

## Changing or adding designs

All files are drawn by `scripts/mesh_kit.py` from the same equation as the site's drawing. Edit the `DESIGNS` or `COLOURS` table there, then run from the repository root:

```bash
pip install cairosvg pillow
python3 scripts/mesh_kit.py
```

This redraws every file in `brand/mesh/`, including `preview.png`. If you rename or remove a design, delete its old files by hand.
