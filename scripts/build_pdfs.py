"""Build the two PDFs from their canonical Markdown source.

Supports the deliberately small Markdown subset used by this project.
Requires reportlab, matplotlib and Pillow. No network or LaTeX installation.
"""
import html
import os
import re
from pathlib import Path
from io import BytesIO

import matplotlib
matplotlib.use("Agg")
from matplotlib.mathtext import math_to_image
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                               Image, Table, TableStyle, PageBreak, KeepTogether, Flowable)
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "pdf"
DEST.mkdir(exist_ok=True)


def fonts():
    candidates = [os.environ.get("EV_REBOUND_FONT_DIR", ""),
                  "/usr/share/fonts/truetype/dejavu",
                  str(Path(matplotlib.get_data_path()) / "fonts/ttf")]
    for item in candidates:
        folder = Path(item)
        names = ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans-Oblique.ttf",
                 "DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf", "DejaVuSerif-Italic.ttf",
                 "DejaVuSansMono.ttf"]
        if all((folder/n).is_file() for n in names):
            for name, file in zip(["Sans", "SansBold", "SansItalic", "Serif", "SerifBold", "SerifItalic", "Mono"], names):
                pdfmetrics.registerFont(TTFont(name, str(folder/file)))
            pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="SansBold", italic="SansItalic", boldItalic="SansBold")
            pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="SerifBold", italic="SerifItalic", boldItalic="SerifBold")
            return
    raise RuntimeError("DejaVu fonts not found. Set EV_REBOUND_FONT_DIR to their directory.")


fonts()
NAVY = colors.HexColor("#183344")
TEAL = colors.HexColor("#147d92")
INK = colors.HexColor("#243541")
MUTED = colors.HexColor("#63727d")
PALE = colors.HexColor("#eff5f7")
PAGE_W, PAGE_H = A4
MARGIN = 48
WIDTH = PAGE_W - 2*MARGIN


def inline(text):
    result = html.escape(text, quote=False)
    result = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
                    lambda m: f'<a href="{html.escape(html.unescape(m[2]), quote=True)}" color="#147d92">{m[1]}</a>', result)
    result = re.sub(r"`([^`]+)`", r'<font name="Mono" size="8.3">\1</font>', result)
    result = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", result)
    result = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", result)
    return result


class Equation(Flowable):
    def __init__(self, expression):
        super().__init__()
        b = BytesIO()
        math_to_image("$"+expression+"$", b, dpi=220, format="png", color="#183344")
        b.seek(0)
        self.bytes = b.getvalue()
        im = PILImage.open(BytesIO(self.bytes))
        scale = min(.34, WIDTH/im.width)
        self.width, self.height = im.width*scale, im.height*scale+18
        self.hAlign = "CENTER"
    def draw(self):
        self.canv.drawImage(ImageReader(BytesIO(self.bytes)), 0, 9,
                            width=self.width, height=self.height-18, mask="auto")


class PaperDoc(BaseDocTemplate):
    def __init__(self, filename, edition, **kw):
        super().__init__(str(filename), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=51, bottomMargin=48, **kw)
        self.edition = edition
        self.headings = []
        self.addPageTemplates(PageTemplate(id="paper", frames=[Frame(MARGIN, 48, WIDTH,
                                 PAGE_H-99, leftPadding=0, rightPadding=0,
                                 topPadding=0, bottomPadding=0)], onPage=self.page_art))
    def page_art(self, canv, doc):
        canv.saveState()
        canv.setStrokeColor(TEAL)
        canv.setLineWidth(1)
        canv.line(MARGIN, PAGE_H-32, PAGE_W-MARGIN, PAGE_H-32)
        canv.setFont("Sans", 7.3)
        canv.setFillColor(MUTED)
        canv.drawString(MARGIN, PAGE_H-23, "EV REBOUND / MAHARASHTRA")
        canv.drawRightString(PAGE_W-MARGIN, PAGE_H-23, self.edition.upper())
        canv.setStrokeColor(colors.HexColor("#d4dfe4"))
        canv.setLineWidth(.5)
        canv.line(MARGIN, 34, PAGE_W-MARGIN, 34)
        canv.setFont("Sans", 7.1)
        canv.drawString(MARGIN, 22, "Ajinkya  |  20 September 2026  |  v1.0.0")
        canv.drawRightString(PAGE_W-MARGIN, 22, str(doc.page))
        canv.restoreState()
    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name.startswith("H"):
            title = f.getPlainText()
            self.headings.append({"page": self.page, "heading": title})
            key = f"heading-{len(self.headings)}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level=0, closed=False)


def build(source, name, edition, academic=False):
    bodyfont = "Serif" if academic else "Sans"
    size = 10.1 if academic else 10.5
    lead = 14.25 if academic else 15.2
    sty = {
        "Body": ParagraphStyle("Body", fontName=bodyfont, fontSize=size, leading=lead,
                               textColor=INK, spaceAfter=8.3, allowWidows=0, allowOrphans=0),
        "H1": ParagraphStyle("H1", fontName="SansBold", fontSize=25 if academic else 31,
                             leading=30 if academic else 35, textColor=NAVY, spaceBefore=9, spaceAfter=18,
                             keepWithNext=True),
        "H2": ParagraphStyle("H2", fontName="SansBold", fontSize=13.1, leading=17,
                             textColor=TEAL, spaceBefore=12, spaceAfter=9, keepWithNext=True),
        "H3": ParagraphStyle("H3", fontName="SansBold", fontSize=11.1, leading=15,
                             textColor=NAVY, spaceBefore=8, spaceAfter=7, keepWithNext=True),
        "Cell": ParagraphStyle("Cell", fontName="Sans", fontSize=8.8, leading=12.1, textColor=INK),
        "CellHead": ParagraphStyle("CellHead", fontName="SansBold", fontSize=8.8, leading=12.1,
                                   textColor=colors.white),
        "Bullet": ParagraphStyle("Bullet", fontName=bodyfont, fontSize=size, leading=lead,
                                 textColor=INK, spaceAfter=6, leftIndent=12, firstLineIndent=-8),
        "Ref": ParagraphStyle("Ref", fontName=bodyfont, fontSize=8.6 if academic else 8.2,
                              leading=11.7 if academic else 11, textColor=INK, spaceAfter=6.5),
    }
    lines = source.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    refs = False
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1; continue
        if s == "<!-- pagebreak -->":
            story.append(PageBreak()); i += 1; continue
        if s == "$$":
            expr = []; i += 1
            while i < len(lines) and lines[i].strip() != "$$":
                expr.append(lines[i].strip()); i += 1
            story.append(Equation(" ".join(expr))); i += 1; continue
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", s)
        if m:
            path = (source.parent/m[2]).resolve()
            im = PILImage.open(path)
            story.append(Image(str(path), width=WIDTH, height=WIDTH*im.height/im.width))
            story.append(Spacer(1, 7)); i += 1; continue
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [v.strip() for v in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells): rows.append(cells)
                i += 1
            n = len(rows[0])
            if n == 3 and "Policy issue" in rows[0][0]: widths=[.20*WIDTH,.47*WIDTH,.33*WIDTH]
            elif n == 3 and "Question" in rows[0][0]: widths=[.26*WIDTH,.48*WIDTH,.26*WIDTH]
            elif n == 3: widths=[.43*WIDTH,.24*WIDTH,.33*WIDTH]
            elif n == 2: widths=[.30*WIDTH,.70*WIDTH]
            elif n == 4: widths=[.43*WIDTH,.19*WIDTH,.19*WIDTH,.19*WIDTH]
            else: widths=[WIDTH/n]*n
            cells = [[Paragraph(inline(c), sty["CellHead" if ri == 0 else "Cell"])
                      for c in row] for ri,row in enumerate(rows)]
            table = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), NAVY), ("VALIGN",(0,0),(-1,-1),"TOP"),
                ("ROWBACKGROUNDS",(0,1),(-1,-1),[PALE,colors.white]),
                ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),8),
                ("TOPPADDING",(0,0),(-1,-1),7), ("BOTTOMPADDING",(0,0),(-1,-1),7),
                ("LINEBELOW",(0,-1),(-1,-1),.5,colors.HexColor("#d2dfe5")),
            ]))
            story.extend([table, Spacer(1, 10)]); continue
        h = re.match(r"(#{1,3}) (.+)", s)
        if h:
            refs = h[2] in ("References", "Sources and project note")
            story.append(Paragraph(inline(h[2]), sty[f"H{len(h[1])}"]))
            i += 1; continue
        if s.startswith("- "):
            story.append(Paragraph(("" if refs else "&#8226; ")+inline(s[2:]),
                                   sty["Ref" if refs else "Bullet"]))
            i += 1; continue
        para = [s]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||\$\$|<!--|!\[|- )",lines[i].strip()):
            para.append(lines[i].strip()); i += 1
        story.append(Paragraph(inline(" ".join(para)), sty["Ref" if refs else "Body"]))
    doc = PaperDoc(DEST/name, edition, title=("Low-Cost Electric Mobility and Travel Rebound in Maharashtra"
                   if academic else "The EV Rebound Effect: Why Cheaper Journeys Can Mean More Journeys"),
                   author="Ajinkya", subject="Independent conceptual analysis; illustrative scenarios; AI assistance disclosed")
    doc.build(story)
    print(f"{name}: {doc.page} pages")
    return {"filename":name, "pages":doc.page, "headings":doc.headings}


if __name__ == "__main__":
    import json
    logs = [build(ROOT/"public/EV_Rebound_Explained.md", "EV_Rebound_Explained.pdf", "Public edition"),
            build(ROOT/"academic/EV_Rebound_Working_Paper.md", "EV_Rebound_Working_Paper.pdf", "Academic working paper", True)]
    audit = ROOT/"tmp"
    audit.mkdir(exist_ok=True)
    (audit/"pdf-build.json").write_text(json.dumps(logs, indent=2))
