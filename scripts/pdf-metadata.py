"""Set Author and Subject on the rendered capability statement. Run by scripts/render.js after Chromium writes the PDF."""
import sys
from pypdf import PdfReader, PdfWriter
path = sys.argv[1]
subject = sys.argv[2] if len(sys.argv) > 2 else "Capability statement"
w = PdfWriter(clone_from=PdfReader(path))
w.add_metadata({"/Author": "Manifold LLC", "/Subject": subject, "/Keywords": "Manifold LLC, AI/ML, " + subject.lower() + ", UEI C6P2G6PQLEB8, CAGE 23X60"})
w.write(path)
