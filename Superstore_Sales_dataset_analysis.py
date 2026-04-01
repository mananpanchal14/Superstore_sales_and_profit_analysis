import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
df = pd.read_csv("SuperStoreOrders.csv")
#print(df.head(100))

print(df.shape)
df["order_date"] = pd.to_datetime(df["order_date"],dayfirst=True,format="mixed")
df["ship_date"] = pd.to_datetime(df["ship_date"],dayfirst=True,format="mixed")

df["sales"] = (
    df["sales"]
    .astype(str)
    .str.replace(",","")
    .str.strip()
)
#print(df.isnull().sum())
#print(df[df['sales'].isnull()])
df['sales'] = pd.to_numeric(df['sales'])
#print(df.info())
total_sales = df["sales"].sum()
total_profit = df["profit"].sum()
total_profit_margin = total_profit / total_sales
print("Total Sales: ", total_sales)
print("Total Profit: ", total_profit)
print("Total Profit Margin: ",total_profit_margin * 100)

df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month
#print(df["order_year"].dtype)
sales_by_year = df.groupby("order_year")["sales"].sum().reset_index(name="yearly_sales")
#print(sales_by_year)
profit_by_year = df.groupby("order_year")["profit"].sum().reset_index(name="yearly_profit")
#print(profit_by_year)

metrics_by_category = df.groupby("category")[["sales","profit"]].sum().sort_values(by=["category","sales","profit"], ascending=[True,False,False])
metrics_by_category["profit_margin"] = metrics_by_category["profit"] / metrics_by_category["sales"] * 100
#print(metrics_by_category)

metrics_by_sc = df.groupby(["category","sub_category"])[["sales","profit"]].sum().sort_values(by=["category","sales","profit"], ascending=[True,False,False])
metrics_by_sc["profit_margin"] = metrics_by_sc["profit"] / metrics_by_sc["sales"] * 100
#print(metrics_by_sc)

metrics_by_market = df.groupby("market")[["sales","profit"]].sum().sort_values(by=["market","sales","profit"], ascending=[True,False,False])
metrics_by_market["profit_margin"] = metrics_by_market["profit"] / metrics_by_market["sales"] * 100
#print(metrics_by_market)

metrics_by_region = df.groupby(["market","region"])[["sales","profit"]].sum().sort_values(by=["market","region","sales","profit"], ascending=[True,True,False,False])
metrics_by_region["profit_margin"] = metrics_by_region["profit"] / metrics_by_market["sales"] * 100
#print(metrics_by_region)

metrics_by_segment = df.groupby("segment")[["sales","profit"]].sum().sort_values(by=["segment","sales","profit"], ascending=[True,False,False])
metrics_by_segment["profit_margin"] = metrics_by_segment["profit"] / metrics_by_segment["sales"] * 100
#print(metrics_by_segment)

metrics_by_shipmode = df.groupby("ship_mode")[["sales","profit"]].sum().sort_values(by=["ship_mode","sales","profit"], ascending=[True,False,False])
metrics_by_shipmode["profit_margin"] = metrics_by_shipmode["profit"] / metrics_by_shipmode["sales"] * 100
#print(metrics_by_shipmode)

metrics_by_priority = df.groupby("order_priority")[["sales","profit"]].sum().sort_values(by=["order_priority","sales","profit"], ascending=[True,False,False])
metrics_by_priority["profit_margin"] = metrics_by_priority["profit"] / metrics_by_priority["sales"] * 100
#print(metrics_by_priority)

metrics_by_discount = df.groupby("discount")["order_id"].count().reset_index(name="customers_count")
#print(metrics_by_discount)
'''
plt.plot(metrics_by_discount["discount"],metrics_by_discount["customers_count"],label="cust_count",marker="o")
plt.xlabel("Discount")
plt.ylabel("customers_count")
plt.legend()
plt.show()
'''
#print(df["discount"].describe())
df['discount_bins'] = pd.cut(
    df['discount'],
    bins=[0, 0.25, 0.5, 0.85],
    labels=["0-25%","25-50%","50-85%"]
)
by_discounts = df.groupby("discount_bins")[["sales","profit"]].agg(["sum","mean"])
#print(by_discounts)

top_products_by_sales = df.groupby("product_name")[["sales","profit"]].sum().sort_values(by="sales",ascending=False).head(15)
#top_products_by_sales["profit_margin"] = top_products_by_sales["profit"] / top_products_by_sales["sales"] * 100
#print(top_products_by_sales)

top_products_by_profit = df.groupby("product_name")[["sales","profit"]].sum().sort_values(by="profit",ascending=False).head(15)
#top_products_by_profit["profit_margin"] = top_products_by_profit["profit"] / top_products_by_profit["sales"] * 100
#print(top_products_by_profit)

bottom_products_by_sales = df.groupby("product_name")[["sales","profit"]].sum().sort_values(by="sales",ascending=True).head(15)
#bottom_products_by_sales["profit_margin"] = bottom_products_by_sales["profit"] / bottom_products_by_sales["sales"] * 100
#print(bottom_products_by_sales)

bottom_products_by_profit = df.groupby("product_name")[["sales","profit"]].sum().sort_values(by="profit",ascending=True).head(15)
#bottom_products_by_profit["profit_margin"] = bottom_products_by_profit["profit"] / bottom_products_by_profit["sales"] * 100
#print(bottom_products_by_profit)
#print(df.groupby("product_name")["sales"].sum().describe())

product_metrics = df.groupby("product_name")[["sales","profit"]].sum().reset_index()
product_metrics["profit_margin"] = product_metrics["profit"] / product_metrics["sales"] * 100
filtered = product_metrics[product_metrics["sales"] > 5000]
#print("Top 10 products having best profit margins are:\n", filtered[["product_name","profit_margin"]].sort_values(by="profit_margin",ascending=False).head(10))
#print("Bottom 10 products having least profit margins are:\n",filtered[["product_name","profit_margin"]].sort_values(by="profit_margin",ascending=False).tail(10))

product_unit = df.groupby("product_name")[["profit","quantity"]].sum().round(2)
product_unit["profit_per_unit"] = (product_unit["profit"] / product_unit["quantity"]).round(2)
print(product_unit[["profit","profit_per_unit"]].sort_values(by="profit_per_unit",ascending=False).head(10))
print("\n")
print(product_unit[["profit","profit_per_unit"]].sort_values(by="profit_per_unit",ascending=True).head(10))