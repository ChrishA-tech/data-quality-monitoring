"""Synthetic orders data with injected quality problems; a second 'drifted' batch for drift checks."""
import numpy as np, pandas as pd
def make(n=50000, seed=1, drift=False):
    r = np.random.default_rng(seed)
    df = pd.DataFrame({
        "order_id": np.arange(n), "customer_id": r.integers(1, 5000, n),
        "product": r.choice(["A","B","C","D","E"], n), "country": r.choice(["UK","DE","FR","ES","IT"], n),
        "channel": r.choice(["web","app","store"], n, p=[.5,.3,.2]),
        "amount": r.lognormal(3.5 + (0.4 if drift else 0), .5, n).round(2),
        "order_date": pd.Timestamp("2026-10-01") + pd.to_timedelta(r.integers(0, 30, n), unit="D")})
    d = df.copy()
    d.loc[r.choice(n, int(.03*n), replace=False), "customer_id"] = np.nan          # missing
    d.loc[r.choice(n, int(.02*n), replace=False), "country"] = None                 # missing, concentrated below
    d.loc[d.channel.eq("store") & (r.random(n) < .08), "amount"] = np.nan          # root cause: store channel
    d.loc[r.choice(n, 150, replace=False), "amount"] *= 40                          # outliers
    d = pd.concat([d, d.sample(int(.01*n), random_state=seed)])                     # duplicates
    return d.reset_index(drop=True)
if __name__ == "__main__":
    make().to_csv("data/batch_ref.csv", index=False); make(seed=2, drift=True).to_csv("data/batch_new.csv", index=False)
