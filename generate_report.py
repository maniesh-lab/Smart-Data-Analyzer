from fpdf import FPDF  # FPDF class import
import main
from datetime import datetime

# Access dataframe from main.py
df = main.df


# Calculate summary metrics
total_sales = df["Sales"].sum()
total_orders = df.shape[0]  #returns no. of rows in a dataframe | df[Row ID].count()-likish ; if there are no null values . BUT, shape[0] returns total rows
avg_sales = df["Sales"].mean()
max_sale = df["Sales"].max()


pdf = FPDF()      #creating a pdf object; creates an empty PDF documexnt. 
pdf.set_auto_page_break(auto=True, margin=15)       #If content reaches bottom → create new page automatically


pdf.add_page()   #must add a page at first



# Title
pdf.set_font("Arial", "B", 22)    #first set then .cell
pdf.cell(0, 12, "Sales Analysis Report", ln=True, align="C")
# width, height, /content/next_line = True
# width = 0 means use full page width, align aligns the text at "C" = center



# Timestamp
pdf.set_font("Arial", size=12)
pdf.cell(
    0,
    10,
    f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    ln=True,
    align="C",
)

pdf.ln(10)   #adding extra space




# -------- SUMMARY SECTION --------


pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Summary Metrics", ln=True)

pdf.set_font("Arial", size=12)

pdf.cell(0, 8, f"Total Orders: {total_orders}", ln=True)
pdf.cell(0, 8, f"Total Sales: ${total_sales:,.2f}", ln=True)
pdf.cell(0, 8, f"Average Sale: ${avg_sales:,.2f}", ln=True)
pdf.cell(0, 8, f"Highest Sale: ${max_sale:,.2f}", ln=True)

pdf.ln(10)



# -------- MONTHLY SALES CHART --------


pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Monthly Sales Trend", ln=True)

pdf.image("charts/monthly_sales.png", x=10, w=180)
# image location, horizontal, vertical position, and w = width
# x and y are auto adjusted and there is height; h parameter also auto calculates, mostly width is only necessary
#x= 10 means 10mm from left ( horizontal position)

pdf.ln(110)



# ---------------- PAGE 2 ----------------

pdf.add_page()

pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Top 10 Selling Products", ln=True)

pdf.image("charts/top_10_products.png", x=10, w=180)

pdf.ln(110)



# ---------------- PAGE 3 ----------------

pdf.add_page()

pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Sales by Category", ln=True)

pdf.image("charts/sales_by_category.png", x=10, w=180)

pdf.ln(110)



# ---------------- PAGE 4 ----------------

pdf.add_page()

pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Sales by Region", ln=True)

pdf.image("charts/sales_by_region.png", x=10, w=180)

pdf.ln(110)



# -------- SAVE REPORT --------
pdf.output("output/sales_report.pdf")

print("Report generated successfully!")
