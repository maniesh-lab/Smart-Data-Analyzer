import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ax = plt.gca()   # get the current axes

df = pd.read_csv("data/sales_data.csv")

df = df.drop_duplicates()
df = df.dropna(axis= 0, how="any") #axis = 0 is to drop rows having missing values, how="any" is for: If any NA values are present, drop that row or column.

# print(df.dtypes)

# print(df.info())
# print(df.describe())
print(df.columns)

#converts str date to datetime in pd, and dayfirst=True tells pandas dateformat is DD/MM/YYYY, meaning day is first in dataset
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True) 
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

# print(df.dtypes)   #changed into datetime64[ns]





# ──---- MONTHLY SALES CHART ──────────────────────────────────────────



# Here we are not grouping by the column itself. so we can NOT do .groupby("Order Date")["Sales"]
# We are grouping by a transformed version of it. so we do df["Order Date"] instead of just "Order Date."

# df["Order Date"]        → get the column
# .dt                     → use datetime tools
# .to_period("M")         → convert each date to its month

monthly_sales = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()

monthly_sales.index = monthly_sales.index.to_timestamp()  #converting into actual point in time, not periods. 
# Periods are like saying "January 2015" (a range). Timestamps are like saying
# "January 1st, 2015 at midnight" (an exact point). Matplotlib needs exact points to draw grids correctly.

plt.figure(figsize=(20, 10))          # ✅ BEFORE plotting
plt.title("Monthly Sales Trend", fontsize=30,fontstyle="normal",fontweight= "bold",color = "red")
plt.xlabel("Month", fontsize=20,fontstyle="normal",fontweight= "bold")
plt.ylabel("Total Sales", fontsize=20,fontstyle="normal",fontweight= "bold")
plt.tick_params(axis="both", labelsize=14, colors="purple")


monthly_sales.plot(
    kind="line",
    linewidth=4,
    marker="o",
    mfc="gold",
    markersize=10,
    mec="black",
    color="cyan"    
    )

plt.ylim(bottom=0)   #ylim mesans y-axis limits. 


#Align grid to actual axis ticks

ax = plt.gca()   #means "get current axes"
ax.set_axisbelow(True)   # grid goes BEHIND the line/markers/data-plots


# which="major" :  Only draw grid at major ticks (the labeled ones), not every minor subdivision
#alpha : transparency (0.0 to 1.0)
plt.grid(True, which="major", color="gray", linestyle="--", linewidth=0.7, alpha=0.7) #after .plot , otherwise, grid won't show


#xlim = x-axis limits
plt.xlim(
    monthly_sales.index.min() - pd.DateOffset(months=2),   # start 2 months BEFORE first data point
    monthly_sales.index.max() + pd.DateOffset(months=2)    # end 2 months AFTER last data point
)


plt.tight_layout()

# ensure output folder exists and save chart with a filename  and also name of file too at end
plt.savefig("charts/monthly_sales.png")  # save first, otherwise image gets cleared, then show().
# plt.show()




# ──------ Top 10 Products Chart ────────────────────────────────────────



top_products =  df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False)
top_10_products = top_products.head(10)

plt.figure(figsize=(22, 12))           # ✅ New figure for second chart

top_10_products.plot(kind="barh",color="#4cbb17") # pandas is overwriting labels


plt.title("Top 10 Products by Sales", fontsize=30,fontstyle="normal",fontweight= "bold",color="red")
plt.ylabel("Product Name", fontsize=20,fontstyle="normal",fontweight= "bold")
plt.xlabel("Total Sales", fontsize=20,fontstyle="normal",fontweight= "bold")
plt.tick_params(axis="both", labelsize=12,colors="purple")


plt.grid(True,axis="x",color="grey")
plt.tight_layout()
plt.savefig("charts/top_10_products.png")  # ✅ BEFORE show()
# plt.show()




# ------------ SALES BY REGION ----------------------------------------------------------------------------------------------------



regional_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=True)


plt.figure(figsize=(22, 12))

regional_sales.plot(kind="barh",color="yellow")

plt.title("Sales by Region", fontsize=30,fontstyle="normal",fontweight= "bold",color="red")
plt.xlabel("Sales", fontsize=20,fontstyle="normal",fontweight= "bold")
plt.ylabel("Region", fontsize=20,fontstyle="normal",fontweight= "bold")
plt.tick_params(axis="both", labelsize=14,colors="purple")

# print(df["Region"].nunique())   #counting unique values in a dataframe column


plt.grid(True,axis="x",color="grey")
plt.tight_layout()
plt.savefig("charts/sales_by_region")
# plt.show()




# -------- SALES BY CATEGORY ------------------------------------------------------------------------------------




sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=True)

plt.figure(figsize=(22, 12))
sales_by_category.plot(kind="barh",color="cyan")

plt.title("Sales By Category", fontsize=30,fontstyle="normal",fontweight= "bold",color="red")
plt.xlabel("Sales", fontsize=20,fontstyle="normal",fontweight= "bold")
plt.ylabel("Category", fontsize=20,fontstyle="normal",fontweight= "bold")
plt.tick_params(axis="both", labelsize=14,colors="purple")

# print(df["Region"].nunique())   #counting unique values in a dataframe column


plt.grid(True,axis="x",color="grey")
plt.tight_layout()
plt.savefig("charts/sales_by_category")
# plt.show()


