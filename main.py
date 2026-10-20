"""
Smart Sales Data Analyzer — turns a sales CSV into 4 charts and a PDF report.

Run with the bundled sample data:
    python main.py

Or point it at your own CSV and tell it which columns to use:
    python main.py --input my_sales.csv --date-col "Date" --sales-col "Revenue" \
        --product-col "Item" --region-col "Area" --category-col "Type"

Run `python main.py --help` to see every option.
"""

import argparse
import os

import matplotlib

matplotlib.use("Agg")  # draw charts straight to files, no window needed
import matplotlib.pyplot as plt  # noqa: E402  (must come after matplotlib.use)
import pandas as pd  # noqa: E402

from generate_report import build_report  # noqa: E402

TITLE_STYLE = dict(fontsize=30, fontstyle="normal", fontweight="bold", color="red")
LABEL_STYLE = dict(fontsize=20, fontstyle="normal", fontweight="bold")


def parse_args():
    parser = argparse.ArgumentParser(description="Turn a sales CSV into charts and a PDF report.")
    parser.add_argument("--input", default="data/sales_data.csv", help="path to the sales CSV")
    parser.add_argument("--date-col", default="Order Date", help="column with the order date")
    parser.add_argument("--sales-col", default="Sales", help="column with the sale amount")
    parser.add_argument("--product-col", default="Product Name", help="column with the product name")
    parser.add_argument("--region-col", default="Region", help='column with the region ("" to skip this chart)')
    parser.add_argument("--category-col", default="Category", help='column with the category ("" to skip this chart)')
    parser.add_argument("--order-col", default="Order ID", help='column with the order ID, used to count orders ("" to count rows)')
    parser.add_argument("--month-first", action="store_true", help="dates are MM/DD/YYYY (default is DD/MM/YYYY)")
    parser.add_argument("--charts-dir", default="charts", help="folder to save chart images in")
    parser.add_argument("--output", default="output/sales_report.pdf", help="where to save the PDF report")
    return parser.parse_args()


def load_data(path, date_col, sales_col, needed_cols, dayfirst=True):
    """Read the CSV and clean only what the analysis needs."""
    df = pd.read_csv(path)
    rows_read = len(df)

    missing = [col for col in needed_cols if col not in df.columns]
    if missing:
        raise SystemExit(
            f"Column(s) not found in {path}: {missing}\n"
            f"Columns in this file: {list(df.columns)}\n"
            f"Use the --*-col options to tell me which columns to use."
        )

    df = df.drop_duplicates()

    # Only drop rows that are missing something we actually use. Dropping
    # rows with ANY empty cell would throw away real sales just because an
    # unrelated column (like Postal Code) happens to be blank.
    df = df.dropna(subset=needed_cols)

    # dayfirst=True reads 08/11/2017 as 8 November, not 11 August.
    # errors="coerce" turns unreadable dates/amounts into NaN instead of crashing;
    # those rows are then dropped.
    df[date_col] = pd.to_datetime(df[date_col], dayfirst=dayfirst, errors="coerce")
    df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce")
    df = df.dropna(subset=[date_col, sales_col])

    if df.empty:
        raise SystemExit("No usable rows left after cleaning — check the column names and date format.")

    dropped = rows_read - len(df)
    print(f"Read {rows_read:,} rows, kept {len(df):,} ({dropped:,} dropped as duplicates, blank or unreadable)")
    return df


def monthly_sales_chart(df, date_col, sales_col, path):
    # Group by each date's month (a transformed version of the column,
    # so we pass df[date_col].dt.to_period("M"), not just the column name).
    monthly_sales = df.groupby(df[date_col].dt.to_period("M"))[sales_col].sum()
    # Periods ("January 2015") become timestamps (an exact point in time),
    # which matplotlib needs to place gridlines correctly.
    monthly_sales.index = monthly_sales.index.to_timestamp()

    plt.figure(figsize=(20, 10))
    monthly_sales.plot(kind="line", linewidth=4, marker="o", mfc="gold", markersize=10, mec="black", color="cyan")

    # Titles and labels go AFTER .plot(): pandas sets its own axis label from
    # the column name while plotting, which would overwrite ours otherwise.
    plt.title("Monthly Sales Trend", **TITLE_STYLE)
    plt.xlabel("Month", **LABEL_STYLE)
    plt.ylabel("Total Sales", **LABEL_STYLE)
    plt.tick_params(axis="both", labelsize=14, colors="purple")
    plt.ylim(bottom=0)

    ax = plt.gca()
    ax.set_axisbelow(True)  # grid goes behind the line and markers
    plt.grid(True, which="major", color="gray", linestyle="--", linewidth=0.7, alpha=0.7)
    plt.xlim(
        monthly_sales.index.min() - pd.DateOffset(months=2),  # a little space before the first point
        monthly_sales.index.max() + pd.DateOffset(months=2),  # and after the last
    )

    plt.tight_layout()
    plt.savefig(path)
    plt.close()  # free the figure's memory before drawing the next one


def bar_chart(series, title, xlabel, ylabel, color, path, label_size=14):
    plt.figure(figsize=(22, 12))
    series.plot(kind="barh", color=color)
    plt.title(title, **TITLE_STYLE)
    plt.xlabel(xlabel, **LABEL_STYLE)
    plt.ylabel(ylabel, **LABEL_STYLE)
    plt.tick_params(axis="both", labelsize=label_size, colors="purple")
    plt.grid(True, axis="x", color="grey")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def main():
    args = parse_args()
    optional_cols = [c for c in (args.region_col, args.category_col) if c]
    needed = [args.date_col, args.sales_col, args.product_col] + optional_cols

    df = load_data(args.input, args.date_col, args.sales_col, needed, dayfirst=not args.month_first)
    os.makedirs(args.charts_dir, exist_ok=True)

    charts = []  # (heading for the report, image path), in report order

    path = os.path.join(args.charts_dir, "monthly_sales.png")
    monthly_sales_chart(df, args.date_col, args.sales_col, path)
    charts.append(("Monthly Sales Trend", path))

    # barh draws the first row at the bottom, so sort smallest-first to put
    # the biggest bar on top.
    top_10 = df.groupby(args.product_col)[args.sales_col].sum().nlargest(10).sort_values()
    path = os.path.join(args.charts_dir, "top_10_products.png")
    bar_chart(top_10, "Top 10 Products by Sales", "Total Sales", "Product", "#4cbb17", path, label_size=12)
    charts.append(("Top 10 Selling Products", path))

    if args.category_col:
        by_category = df.groupby(args.category_col)[args.sales_col].sum().sort_values()
        path = os.path.join(args.charts_dir, "sales_by_category.png")
        bar_chart(by_category, "Sales by Category", "Sales", "Category", "cyan", path)
        charts.append(("Sales by Category", path))

    if args.region_col:
        by_region = df.groupby(args.region_col)[args.sales_col].sum().sort_values()
        path = os.path.join(args.charts_dir, "sales_by_region.png")
        bar_chart(by_region, "Sales by Region", "Sales", "Region", "yellow", path)
        charts.append(("Sales by Region", path))

    if args.order_col and args.order_col in df.columns:
        order_label, order_count = "Total Orders", df[args.order_col].nunique()
    else:
        order_label, order_count = "Total Rows", len(df)

    sales = df[args.sales_col]
    summary = [
        (order_label, f"{order_count:,}"),
        ("Total Sales", f"${sales.sum():,.2f}"),
        ("Average Sale (per row)", f"${sales.mean():,.2f}"),
        ("Highest Sale", f"${sales.max():,.2f}"),
    ]

    build_report(summary, charts, args.output)
    print(f"Charts saved to {args.charts_dir}/ and report saved to {args.output}")


if __name__ == "__main__":
    main()
