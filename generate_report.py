from datetime import datetime
from pathlib import Path
from fpdf import FPDF, XPos, YPos
import main


OUTPUT_DIR = Path("output")   #Path("output") creates a path object,#and .mkdir(parents=True, exist_ok=True) creates the folder if 
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # it doesn't exist, same idea as os.makedirs, just cleaner.


# Access dataframe from main.py
df = main.df



# Calculate summary metrics
total_sales = df["Sales"].sum()
total_orders = df.shape[0]
avg_sales = df["Sales"].mean()
max_sale = df["Sales"].max()


pdf = FPDF(format="A4")  # creating a pdf object; creates an empty PDF document.
pdf.set_auto_page_break(auto=True, margin=15)  # If content reaches bottom → create new page automatically

pdf.add_page()   #must add a page at first



# Title

pdf.set_font("Helvetica", "B", 22)  # Helvetica is a core font that works in all PDF viewers
pdf.cell(
    0,
    12,
    "Sales Analysis Report",
    new_x=XPos.LMARGIN,  #XPos.LMARGIN means "after this cell, move X position back to the left margin.""
    new_y=YPos.NEXT,     #YPos.NEXT means "move Y position down to the next line."
    align="C",
)

# Timestamp
pdf.set_font("Helvetica", size=12)
pdf.cell(
    0,
    10,
    f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
    align="C",
)

pdf.ln(10)  # adding extra space




# -------- SUMMARY SECTION --------


pdf.set_font("Helvetica", "B", 16)
pdf.cell(
    0,
    10,
    "Summary Metrics",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
)

pdf.set_font("Helvetica", size=12)

pdf.cell(
    0,
    8,
    f"Total Orders: {total_orders}",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
)
pdf.cell(
    0,
    8,
    f"Total Sales: ${total_sales:,.2f}",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
)
pdf.cell(
    0,
    8,
    f"Average Sale: ${avg_sales:,.2f}",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
)
pdf.cell(
    0,
    8,
    f"Highest Sale: ${max_sale:,.2f}",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
)

pdf.ln(10)




# -------- MONTHLY SALES CHART --------


pdf.set_font("Helvetica", "B", 16)
pdf.cell(
    0,
    10,
    "Monthly Sales Trend",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
)

pdf.image("charts/monthly_sales.png", x=10, w=180)

pdf.ln(110)



# ---------------- PAGE 2 ----------------


pdf.add_page()

pdf.set_font("Helvetica", "B", 16)
pdf.cell(
    0,
    10,
    "Top 10 Selling Products",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
)

pdf.image("charts/top_10_products.png", x=10, w=180)

pdf.ln(110)



# ---------------- PAGE 3 ----------------


pdf.add_page()

pdf.set_font("Helvetica", "B", 16)
pdf.cell(
    0,
    10,
    "Sales by Category",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
)

pdf.image("charts/sales_by_category.png", x=10, w=180)

pdf.ln(110)



# ---------------- PAGE 4 ----------------


pdf.add_page()

pdf.set_font("Helvetica", "B", 16)
pdf.cell(
    0,
    10,
    "Sales by Region",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT,
)
pdf.ln(10)

pdf.image("charts/sales_by_region.png", x=10, w=180)

pdf.ln(110)



# -------- SAVE REPORT --------

pdf.output(OUTPUT_DIR / "sales_report.pdf")

# Instead of hardcoding the string "output/sales_report.pdf", it uses the Path object. 
# The / here isn't division — it's pathlib's way of joining paths. 
# It's cleaner and works correctly on Windows, Mac, and Linux


print("Report generated successfully!")
