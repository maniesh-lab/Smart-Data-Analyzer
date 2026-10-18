"""
Builds the PDF report from the summary numbers and chart images that
main.py produces. Run `python main.py` — it calls build_report() for you.
"""

from datetime import datetime
from pathlib import Path

from fpdf import FPDF, XPos, YPos


def _line(pdf, height, text, align="L"):
    # new_x=LMARGIN: after this cell, move back to the left margin.
    # new_y=NEXT: then move down to the next line.
    pdf.cell(0, height, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align=align)


def build_report(summary, charts, output_path):
    """
    summary: list of (label, value) pairs, e.g. [("Total Sales", "$1,234.00")]
    charts:  list of (heading, image_path) pairs; the first goes on page 1
             under the summary, every other chart gets its own page
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)  # same idea as os.makedirs(..., exist_ok=True)

    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)  # content reaching the bottom starts a new page
    pdf.add_page()

    # Title and timestamp
    pdf.set_font("Helvetica", "B", 22)  # Helvetica is a core font that works in all PDF viewers
    _line(pdf, 12, "Sales Analysis Report", align="C")
    pdf.set_font("Helvetica", size=12)
    _line(pdf, 10, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C")
    pdf.ln(10)

    # Summary section
    pdf.set_font("Helvetica", "B", 16)
    _line(pdf, 10, "Summary Metrics")
    pdf.set_font("Helvetica", size=12)
    for label, value in summary:
        _line(pdf, 8, f"{label}: {value}")
    pdf.ln(10)

    # Charts: the first one shares page 1, the rest get a page each
    for i, (heading, image_path) in enumerate(charts):
        if i > 0:
            pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        _line(pdf, 10, heading)
        pdf.image(str(image_path), x=10, w=180)

    pdf.output(str(output_path))


if __name__ == "__main__":
    # Kept so the old `python generate_report.py` command still works.
    from main import main

    main()
