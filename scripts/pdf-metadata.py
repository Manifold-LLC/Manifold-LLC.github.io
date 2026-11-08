"""Set Author and Subject on the rendered capability statement. Run by scripts/render.js after Chromium writes the PDF."""
import sys
from pypdf import PdfReader, PdfWriter
path = sys.argv[1]
w = PdfWriter(clone_from=PdfReader(path))
w.add_metadata({"/Author": "Manifold LLC", "/Subject": "Capability statement", "/Keywords": "Manifold LLC, AI/ML, capability statement, UEI C6P2G6PQLEB8, CAGE 23X60"})
w.write(path)
