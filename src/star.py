"""Export a star schema (fact + dims) and the quality log for Power BI."""
import pandas as pd, sqlite3, os
from dq import root_cause
os.makedirs("powerbi", exist_ok=True)
df = pd.read_csv("data/batch_new.csv", parse_dates=["order_date"])
df["is_missing_amount"] = df.amount.isna().astype(int); df["is_duplicate"] = df.duplicated("order_id").astype(int)
for d in ["product","country","channel"]:
    t = pd.DataFrame({d: df[d].dropna().unique()}); t[d+"_key"] = range(1, len(t)+1); t.to_csv(f"powerbi/dim_{d}.csv", index=False)
    df = df.merge(t, on=d, how="left")
dc = pd.DataFrame({"date": pd.date_range(df.order_date.min(), df.order_date.max())}); dc["date_key"] = dc.date.dt.strftime("%Y%m%d").astype(int); dc.to_csv("powerbi/dim_date.csv", index=False)
df["date_key"] = df.order_date.dt.strftime("%Y%m%d").astype(int)
df[["order_id","customer_id","date_key","product_key","country_key","channel_key","amount","is_missing_amount","is_duplicate"]].to_csv("powerbi/fact_orders.csv", index=False)
root_cause(pd.read_csv("data/batch_new.csv"), "amount").to_csv("powerbi/root_cause_amount.csv", index=False)
pd.read_sql("SELECT * FROM dq_log", sqlite3.connect("data/dq.sqlite")).to_csv("powerbi/dq_log.csv", index=False)
