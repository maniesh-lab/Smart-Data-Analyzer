# Smart Sales Data Analyzer

A Python pipeline that turns any sales CSV into 4 charts and a multi-page PDF
report. You tell it which columns hold the date, amount, product, region and
category, so it isn't tied to one dataset.

It cleans the data first (duplicates, blank values and unreadable dates or
amounts are dropped, and it tells you how many), then charts sales by month,
product, category and region, and puts the charts and summary numbers into a
PDF with the date and time it was made.

---

## Features

- Works on your own CSV: column names, date format, input and output paths are all command-line options
- Data cleaning — removes duplicates and rows missing a value the analysis needs (a blank, unrelated column like Postal Code doesn't throw a sale away)
- Clear error if a column is missing, listing the columns the file actually has
- Prints how many rows were read and how many were kept after cleaning
- Sales trend analysis
- Automatic chart generation
- Summary metrics calculation
- Multi-page PDF report generation

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Language |
| `pandas` | Reading, cleaning and grouping the CSV |
| `matplotlib` | Drawing the 4 charts |
| `fpdf2` | Building the PDF report |

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
├── screenshots/
│   ├── report_preview_1.png
│   └── report_preview_2.png
│
├── main.py              # entry point: options, cleaning, analysis, charts
├── generate_report.py   # build_report(): turns summary + charts into the PDF
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

---

## How It Works

### 1. Data Processing

`main.py` reads the dataset and performs:

- Column check (stops with a helpful message if a column is missing)
- Data cleaning — duplicates, and rows missing a date, amount, product, region or category
- Date and amount conversion (unreadable values are dropped, not crashed on)
- Grouping and aggregation

### 2. Visualization

Charts are generated using **matplotlib**:

- Monthly sales trend
- Sales by category
- Sales by region
- Top selling products

The charts are automatically saved in the `charts/` folder.

### 3. Report Generation

`generate_report.py` creates a **multi-page PDF report** using **FPDF2**;
`main.py` calls it automatically at the end of the run.

The report includes:

- Report title
- Generation timestamp
- Summary statistics
- Visual charts

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline
```bash
python main.py
```

This runs the analysis, saves the charts to `charts/`, and builds the PDF
report at `output/sales_report.pdf`.

### 3. Use your own CSV
```bash
python main.py --input my_sales.csv \
    --date-col "Date" --sales-col "Revenue" --product-col "Item" \
    --region-col "Area" --category-col "Type" --order-col "Invoice No"
```

- Pass `--region-col ""` or `--category-col ""` to skip a chart your data has no column for
- Pass `--order-col ""` to count rows instead of unique orders
- Add `--month-first` if your dates are MM/DD/YYYY (the default is DD/MM/YYYY)
- `--charts-dir` and `--output` change where the charts and PDF are saved

Run `python main.py --help` for the full list.

---

## Example Output

The generated PDF report includes:

- Sales summary metrics
- Monthly sales trends
- Regional sales distribution
- Category sales comparison
- Top performing products

> **Note:** The 4 charts in `charts/` and `output/sales_report.pdf` are sample outputs from the included dataset. Running `main.py` replaces them with your own.

![Report Preview](screenshots/report_preview_1.png)

![Report Preview](screenshots/report_preview_2.png)

---

## Known Limitations

- Money is always shown with a `$` sign
- Dates must be day-first (DD/MM/YYYY) or, with `--month-first`, month-first. A file that mixes both will have some dates read the wrong way round
- The chart and report file names are fixed, so each run replaces the last one

---

## Author

**Manish Pandeya** · [github.com/maniesh-lab](https://github.com/maniesh-lab)

