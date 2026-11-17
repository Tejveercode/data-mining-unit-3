#!/usr/bin/env python3
"""Build printable PDFs from the Unit 3 study-pack Markdown files.

Pure Python (reportlab) so it works without system libraries.
Usage:  .venv/bin/python build_pdf.py
Writes PDFs into pdf/.
"""
import os
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Preformatted,
)
from reportlab.platypus.flowables import HRFlowable

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = BASE
OUT = os.path.join(FILES, "pdf")

ACCENT = colors.HexColor("#7a1f2b")
GREY = colors.HexColor("#444444")
RULE = colors.HexColor("#c9b3b6")

ss = getSampleStyleSheet()


def style(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9.6, leading=13.4, textColor=colors.black,
                spaceAfter=5, alignment=TA_JUSTIFY)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "title": style("t", fontName="Helvetica-Bold", fontSize=26, leading=31,
                   textColor=ACCENT, alignment=TA_CENTER, spaceAfter=10),
    "subtitle": style("st", fontSize=12.5, leading=18, alignment=TA_CENTER,
                      textColor=GREY, spaceAfter=6),
    "h1": style("h1", fontName="Helvetica-Bold", fontSize=17, leading=21,
                textColor=colors.white, backColor=ACCENT, spaceBefore=6, spaceAfter=10,
                alignment=0, borderPadding=(6, 8, 6, 8)),
    "h2": style("h2", fontName="Helvetica-Bold", fontSize=12.6, leading=16,
                textColor=ACCENT, spaceBefore=11, spaceAfter=4, alignment=0),
    "h3": style("h3", fontName="Helvetica-BoldOblique", fontSize=10.8, leading=14,
                textColor=colors.black, spaceBefore=8, spaceAfter=3, alignment=0),
    "h4": style("h4", fontName="Helvetica-Bold", fontSize=9.9, leading=13,
                textColor=GREY, spaceBefore=6, spaceAfter=2, alignment=0),
    "body": style("b"),
    "bullet": style("bu", leftIndent=13, bulletIndent=2, spaceAfter=2.5),
    "quote": style("q", leftIndent=12, textColor=GREY, fontName="Helvetica-Oblique"),
    "cell": style("c", fontSize=8.1, leading=10.4, spaceAfter=0, alignment=0),
    "cellh": style("ch", fontSize=8.1, leading=10.4, spaceAfter=0, fontName="Helvetica-Bold",
                   textColor=colors.white, alignment=0),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=7.9, leading=10.2,
                           textColor=colors.HexColor("#14303f")),
}


def inline(text):
    """Convert a small Markdown subset to reportlab mini-HTML."""
    t = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"`([^`]+)`", r'<font face="Courier" size="8.4" color="#0d4f63">\1</font>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", t)
    return t


def make_table(rows):
    header, body = rows[0], rows[1:]
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    data = [[Paragraph(inline(c), S["cellh"]) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(inline(c), S["cell"]) for c in r])
    usable = A4[0] - 34 * mm
    weights = []
    for i in range(ncols):
        longest = max(len(re.sub(r"[*`\[\]]", "", r[i])) for r in rows)
        weights.append(max(6, min(longest, 46)))
    total = sum(weights)
    widths = [usable * w / total for w in weights]
    tbl = Table(data, colWidths=widths, repeatRows=1, hAlign="CENTER")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#faf7f7")]),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return tbl


def md_to_flowables(md, first_h1=False):
    flow = []
    lines = md.split("\n")
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()

        if s.startswith("```"):
            i += 1
            block = []
            while i < n and not lines[i].strip().startswith("```"):
                block.append(lines[i].rstrip())
                i += 1
            i += 1
            txt = "\n".join(block)
            tbl = Table([[Preformatted(txt, S["code"])]], colWidths=[A4[0] - 34 * mm])
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f6f8")),
                ("BOX", (0, 0), (-1, -1), 0.4, RULE),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            flow += [tbl, Spacer(1, 6)]
            continue

        if s.startswith("|") and i + 1 < n and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1].strip()):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                raw = lines[i].strip().strip("|")
                if not re.match(r"^[\s:\-|]+$", raw):
                    rows.append([c.strip() for c in raw.split("|")])
                i += 1
            flow += [Spacer(1, 3), make_table(rows), Spacer(1, 7)]
            continue

        if not s:
            i += 1
            continue

        if re.match(r"^-{3,}$", s):
            flow += [Spacer(1, 2), HRFlowable(width="100%", thickness=0.7, color=RULE),
                     Spacer(1, 5)]
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            level, text = len(m.group(1)), m.group(2)
            key = f"h{level}"
            if level == 1 and not first_h1:
                flow.append(PageBreak())
            flow.append(Paragraph(inline(text), S[key]))
            i += 1
            continue

        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            flow.append(Paragraph(inline(" ".join(buf)), S["quote"]))
            continue

        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            flow.append(Paragraph(inline(m.group(1)), S["bullet"], bulletText="\u2022"))
            i += 1
            continue

        m = re.match(r"^(\d+)\.\s+(.*)$", s)
        if m:
            flow.append(Paragraph(inline(m.group(2)), S["bullet"],
                                  bulletText=f"{m.group(1)}."))
            i += 1
            continue

        buf = [s]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith(("#", "|", ">", "```", "- ", "* "))
                    or re.match(r"^\d+\.\s", nxt) or re.match(r"^-{3,}$", nxt)):
                break
            buf.append(nxt)
            i += 1
        flow.append(Paragraph(inline(" ".join(buf)), S["body"]))

    return flow


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(GREY)
    if doc.page > 1:
        canvas.drawString(17 * mm, 11 * mm, doc.doc_title)
        canvas.drawRightString(A4[0] - 17 * mm, 11 * mm, f"Page {doc.page}")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(17 * mm, 14 * mm, A4[0] - 17 * mm, 14 * mm)
    canvas.restoreState()


def title_page(title, subtitle, meta_lines):
    flow = [Spacer(1, 55 * mm), Paragraph(title, S["title"])]
    flow.append(HRFlowable(width="45%", thickness=1.6, color=ACCENT, hAlign="CENTER",
                           spaceBefore=4, spaceAfter=12))
    flow.append(Paragraph(subtitle, S["subtitle"]))
    flow.append(Spacer(1, 14))
    for line in meta_lines:
        flow.append(Paragraph(line, style("m", alignment=TA_CENTER, fontSize=9.4,
                                          textColor=GREY, spaceAfter=2)))
    return flow


def build(out_name, title, subtitle, meta_lines, md_files, cover=True):
    path = os.path.join(OUT, out_name)

    class Doc(BaseDocTemplate):
        def __init__(self, fn, **kw):
            BaseDocTemplate.__init__(self, fn, pagesize=A4, leftMargin=17 * mm,
                                     rightMargin=17 * mm, topMargin=16 * mm,
                                     bottomMargin=18 * mm, **kw)
            frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                          id="normal")
            self.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

    doc = Doc(path, title=title)
    doc.doc_title = title
    story = title_page(title, subtitle, meta_lines) + [PageBreak()] if cover else []
    for idx, f in enumerate(md_files):
        with open(f, encoding="utf-8") as fh:
            md = fh.read()
        story += md_to_flowables(md, first_h1=(idx == 0 and not cover))
    doc.build(story)
    return path, os.path.getsize(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    notes = sorted(
        os.path.join(FILES, "notes", f) for f in os.listdir(os.path.join(FILES, "notes"))
        if f.endswith(".md")
    )
    meta = ["Study pack for Unit 3 of the Data Mining course",
            "Notes &middot; worked numericals &middot; question bank &middot; revision sheet",
            "Compiled November 2026"]
    for name, title, sub, files in [
        ("Unit-3-Classification-Clustering-Notes.pdf", "Unit 3 — Classification & Clustering",
         "Complete notes with explanations, solved examples and comparison tables", notes),
        ("Unit-3-Revision-Cheat-Sheet.pdf", "Unit 3 — Revision Sheet",
         "Recall sheet: definitions, formulas, comparisons, mnemonics, key numbers",
         [os.path.join(FILES, "exam", "cheat-sheet.md")]),
        ("Unit-3-Question-Bank.pdf", "Unit 3 — Exam Question Bank",
         "108 questions by mark weight with model answer outlines",
         [os.path.join(FILES, "exam", "question-bank.md")]),
    ]:
        p, size = build(name, title, sub, meta, files)
        print(f"built {os.path.basename(p)}  ({size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
