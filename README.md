# Smart Sales Data Analyzer

## Overview

A Python pipeline that turns raw sales data into a professional PDF report — 
automatically.

Point it at any sales CSV and it will:
- Clean and validate the data
- Identify trends by month, region, and category
- Generate 4 charts (monthly trend, category breakdown, regional distribution, top products)
- Compile everything into a timestamped, multi-page PDF report

Built with pandas, matplotlib, and FPDF2. No manual work required after setup.

---

## Features

- Data cleaning (remove duplicates and missing values)
- Sales trend analysis
- Automatic chart generation
- Summary metrics calculation
- Multi-page PDF report generation

---

## Tools & Libraries

- Python 3.7+
- pandas
- numpy
- matplotlib
- fpdf2

---

## Project Structure

```
Smart-Data-Analyzer/
│
├── charts/              # Generated charts
│   ├── monthly_sales.png
│   ├── sales_by_category.png
│   ├── sales_by_region.png
│   └── top_10_products.png
│
├── data/
│   └── sales_data.csv
│
├── output/
│   └── sales_report.pdf
│
├── main.py              # Data analysis and chart generation
├── generate_report.py   # PDF report generation
├── requirements.txt
└── README.md
```

---

## How It Works

### 1. Data Processing

`main.py` reads the dataset and performs:

- Data cleaning
- Date conversion
- Grouping and aggregation

### 2. Visualization

Charts are generated using **matplotlib**:

- Monthly sales trend
- Sales by category
- Sales by region
- Top selling products

The charts are automatically saved in the `charts/` folder.

### 3. Report Generation

`generate_report.py` creates a **multi-page PDF report** using **FPDF2**.

The report includes:

- Report title
- Generation timestamp
- Summary statistics
- Visual charts

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline
```bash
python main.py && python generate_report.py
```

This runs the analysis and generates the PDF report automatically.
The final report will be saved to `output/sales_report.pdf`

---

## Example Output

The generated PDF report includes:

- Sales summary metrics
- Monthly sales trends
- Regional sales distribution
- Category sales comparison
- Top performing products

> **Note:** Charts are generated when you run `main.py`. The `charts/` folder will be populated after the first run.

![Report Preview](screenshots/report_preview_1.png)

![Report Preview](screenshots/report_preview_2.png)

---

## Author

Manish Pandeya
