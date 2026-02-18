#!/usr/bin/env python3
"""Convert all .md product files to PDF using markdown2 + fpdf2 (pure Python, no system deps)."""

import re
from fpdf import FPDF
from pathlib import Path

SRC_DIR = Path(__file__).parent
OUT_DIR = SRC_DIR / "pdfs"
OUT_DIR.mkdir(exist_ok=True)

PRODUCT_NAMES = {
    "01_73_COLD_EMAIL_SUBJECT_LINES": ("73 Cold Email Subject Lines That Actually Get Opens", "$5"),
    "02_FUNNEL_TEARDOWN_PACK": ("Funnel Teardown Pack: $50-100K/mo Community Reverse-Engineered", "$9"),
    "03_AI_AUTOMATION_BLUEPRINT": ("The AI Automation Blueprint for Solopreneurs", "$19"),
    "04_SOLOPRENEUR_OPS_SYSTEM": ("The Solopreneur Ops System", "$29"),
    "05_COLD_EMAIL_PLAYBOOK": ("The Cold Email Playbook", "$9"),
}

LEFT_MARGIN = 15


class ProductPDF(FPDF):
    def __init__(self, title, price):
        super().__init__()
        self.product_title = title
        self.product_price = price
        self.set_auto_page_break(auto=True, margin=25)
        self.set_left_margin(LEFT_MARGIN)
        self.set_right_margin(LEFT_MARGIN)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_x(LEFT_MARGIN)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        tw = self.w - 2 * LEFT_MARGIN
        self.cell(tw, 8, f"PRINTMAXX  |  {self.product_title}", align="L", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(220, 220, 220)
        self.line(LEFT_MARGIN, self.get_y(), self.w - LEFT_MARGIN, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def cover_page(self):
        self.add_page()
        self.ln(60)
        self.set_font("Helvetica", "B", 26)
        self.set_text_color(0, 0, 0)
        self.set_x(LEFT_MARGIN)
        self.multi_cell(self.w - 2 * LEFT_MARGIN, 13, self.product_title, align="C")
        self.ln(10)
        mid = self.w / 2
        self.set_draw_color(0, 0, 0)
        self.line(mid - 40, self.get_y(), mid + 40, self.get_y())
        self.ln(10)
        self.set_font("Helvetica", "", 13)
        self.set_text_color(80, 80, 80)
        self.set_x(LEFT_MARGIN)
        self.cell(self.w - 2 * LEFT_MARGIN, 10, "PRINTMAXX  |  printmaxxer.gumroad.com", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(30)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(120, 120, 120)
        self.set_x(LEFT_MARGIN)
        self.cell(self.w - 2 * LEFT_MARGIN, 8, "This product is for personal use only. Do not redistribute.", align="C", new_x="LMARGIN", new_y="NEXT")


def safe_text(text):
    """Make text safe for latin-1 encoding used by fpdf2."""
    return text.encode('latin-1', 'replace').decode('latin-1')


def strip_md(text):
    """Remove markdown bold/italic/code/link markers."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    return text.strip()


def write_line(pdf, text, font="Helvetica", style="", size=10, color=(30, 30, 30), h=6, indent=0):
    """Write a single line/paragraph, always starting from left margin."""
    pdf.set_x(LEFT_MARGIN + indent)
    pdf.set_font(font, style, size)
    pdf.set_text_color(*color)
    w = pdf.w - LEFT_MARGIN - (LEFT_MARGIN + indent)
    pdf.multi_cell(w, h, safe_text(text))


def render_table(pdf, rows):
    """Render a table with auto-sizing columns."""
    if not rows:
        return
    pdf.ln(2)
    num_cols = max(len(r) for r in rows)
    usable = pdf.w - 2 * LEFT_MARGIN
    col_w = usable / max(num_cols, 1)

    # Header
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(235, 235, 235)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(LEFT_MARGIN)
    for cell in rows[0]:
        t = safe_text(strip_md(cell))
        if len(t) > 35:
            t = t[:33] + ".."
        pdf.cell(col_w, 5.5, t, border=1, fill=True)
    pdf.ln()

    # Data rows
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(40, 40, 40)
    for row in rows[1:]:
        pdf.set_x(LEFT_MARGIN)
        for j in range(num_cols):
            t = safe_text(strip_md(row[j])) if j < len(row) else ""
            if len(t) > 35:
                t = t[:33] + ".."
            pdf.cell(col_w, 5, t, border=1)
        pdf.ln()
    pdf.ln(2)


def render_md_to_pdf(md_text, pdf):
    """Parse markdown line-by-line and render to PDF."""
    lines = md_text.split('\n')
    in_code = False
    table_rows = []
    in_table = False

    for line in lines:
        raw = line
        stripped = line.strip()

        # Code fence
        if stripped.startswith('```'):
            if in_code:
                in_code = False
                pdf.ln(2)
            else:
                in_code = True
                pdf.ln(2)
            continue

        # Inside code block
        if in_code:
            t = raw.replace('\t', '    ')
            pdf.set_x(LEFT_MARGIN)
            pdf.set_font("Courier", "", 7.5)
            pdf.set_text_color(40, 40, 40)
            pdf.set_fill_color(244, 244, 244)
            w = pdf.w - 2 * LEFT_MARGIN
            pdf.multi_cell(w, 4.5, safe_text(f"  {t}"), fill=True)
            continue

        # Empty line
        if not stripped:
            # Flush table if we were in one
            if in_table and table_rows:
                render_table(pdf, table_rows)
                table_rows = []
                in_table = False
            pdf.ln(2)
            continue

        # Horizontal rule
        if stripped in ('---', '***', '___'):
            if in_table and table_rows:
                render_table(pdf, table_rows)
                table_rows = []
                in_table = False
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(LEFT_MARGIN, pdf.get_y(), pdf.w - LEFT_MARGIN, pdf.get_y())
            pdf.ln(4)
            continue

        # Table row
        if stripped.startswith('|') and stripped.endswith('|'):
            # Skip separator rows
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            in_table = True
            table_rows.append(cells)
            continue

        # If we were in a table but this line is not a table row, flush
        if in_table and table_rows:
            render_table(pdf, table_rows)
            table_rows = []
            in_table = False

        # H1
        if stripped.startswith('# ') and not stripped.startswith('## '):
            pdf.ln(4)
            write_line(pdf, strip_md(stripped[2:]), style="B", size=17, color=(0, 0, 0), h=9)
            pdf.set_draw_color(0, 0, 0)
            pdf.line(LEFT_MARGIN, pdf.get_y() + 1, pdf.w - LEFT_MARGIN, pdf.get_y() + 1)
            pdf.ln(3)
            continue

        # H2
        if stripped.startswith('## '):
            pdf.ln(5)
            write_line(pdf, strip_md(stripped[3:]), style="B", size=14, color=(20, 20, 20), h=8)
            pdf.ln(2)
            continue

        # H3
        if stripped.startswith('### '):
            pdf.ln(3)
            write_line(pdf, strip_md(stripped[4:]), style="B", size=12, color=(40, 40, 40), h=7)
            pdf.ln(1)
            continue

        # H4
        if stripped.startswith('#### '):
            pdf.ln(2)
            write_line(pdf, strip_md(stripped[5:]), style="B", size=11, color=(50, 50, 50), h=6)
            pdf.ln(1)
            continue

        # Bullet points
        if stripped.startswith('- ') or stripped.startswith('* '):
            text = strip_md(stripped[2:])
            write_line(pdf, f"- {text}", size=10, indent=6)
            continue

        # Sub-bullet
        if raw.startswith('  - ') or raw.startswith('  * '):
            text = strip_md(stripped[2:])
            write_line(pdf, f"- {text}", size=9, indent=14, color=(60, 60, 60))
            continue

        # Numbered list
        num_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if num_match:
            num = num_match.group(1)
            text = strip_md(num_match.group(2))
            write_line(pdf, f"{num}. {text}", size=10, indent=6)
            continue

        # Regular paragraph
        write_line(pdf, strip_md(stripped))

    # Flush remaining table
    if in_table and table_rows:
        render_table(pdf, table_rows)


def convert_file(md_path):
    """Convert a single .md file to PDF."""
    stem = md_path.stem
    title, price = PRODUCT_NAMES.get(stem, (stem, ""))

    pdf = ProductPDF(title, price)
    pdf.cover_page()
    pdf.add_page()

    md_text = md_path.read_text(encoding="utf-8")
    render_md_to_pdf(md_text, pdf)

    pdf_path = OUT_DIR / f"{stem}.pdf"
    pdf.output(str(pdf_path))
    size_kb = pdf_path.stat().st_size / 1024
    print(f"  -> {pdf_path.name} ({size_kb:.0f} KB, {pdf.page_no()} pages)")
    return pdf_path


if __name__ == "__main__":
    md_files = sorted(SRC_DIR.glob("*.md"))
    converted = 0
    for md_file in md_files:
        print(f"Converting: {md_file.name}")
        try:
            convert_file(md_file)
            converted += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
    print(f"\nDone. {converted} PDFs in {OUT_DIR}")
