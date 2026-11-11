#!/usr/bin/env python3
"""Convert an itinerary written in Markdown into a styled Word (.docx) file.

Usage: python md_to_docx.py itinerary.md "Trip itinerary.docx" [--font "Microsoft YaHei"]

Requires: pandoc on PATH, and the python-docx package.
Output: A4 pages, a CJK-friendly font for all text, compact tables with
coloured header rows and light grey borders.
"""
import argparse
import os
import subprocess
import sys
import tempfile

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HEADER_FILL = "2E75B6"
TITLE_COLOR = "1F3864"


def set_font(style, font, size=None, bold=None, color=None):
    style.font.name = font
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), font)
    if size:
        style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold
    if color:
        style.font.color.rgb = RGBColor.from_string(color)


def style_document(path_in, path_out, font):
    doc = Document(path_in)
    for section in doc.sections:
        section.page_width, section.page_height = Cm(21), Cm(29.7)
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(section, side, Cm(1.8))

    by_name = {s.name.lower(): s for s in doc.styles}
    for name in ("normal", "body text", "first paragraph", "compact"):
        if name in by_name:
            set_font(by_name[name], font, 10)
    for name, args in (("title", (20, True, TITLE_COLOR)),
                       ("heading 1", (15, True, TITLE_COLOR)),
                       ("heading 2", (12, True, HEADER_FILL))):
        if name in by_name:
            set_font(by_name[name], font, *args)

    for table in doc.tables:
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{edge}")
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "4")
            el.set(qn("w:color"), "BFBFBF")
            borders.append(el)
        table._tbl.tblPr.append(borders)
        for i, row in enumerate(table.rows):
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = Pt(0)
                    for run in p.runs:
                        run.font.size = Pt(9)
                        if i == 0:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(255, 255, 255)
                if i == 0:
                    shd = OxmlElement("w:shd")
                    shd.set(qn("w:val"), "clear")
                    shd.set(qn("w:fill"), HEADER_FILL)
                    cell._tc.get_or_add_tcPr().append(shd)
    doc.save(path_out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("markdown")
    ap.add_argument("output")
    ap.add_argument("--font", default="Microsoft YaHei",
                    help="Font for all text (default: Microsoft YaHei)")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw.docx")
        try:
            subprocess.run(["pandoc", args.markdown, "-o", raw], check=True)
        except FileNotFoundError:
            sys.exit("pandoc not found: install it from https://pandoc.org/")
        style_document(raw, args.output, args.font)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
