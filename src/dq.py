"""Data-quality checks: missing values, duplicates, outliers (IQR), drift (PSI), and root-cause attribution."""
import numpy as np, pandas as pd, sqlite3, datetime as dt
def missing(df): return {c: float(df[c].isna().mean()) for c in df.columns if df[c].isna().any()}
def duplicates(df, key="order_id"): return int(df.duplicated(subset=[key]).sum())
def outliers(s, k=3.0):
    s = s.dropna(); q1, q3 = s.quantile([.25, .75]); i = q3 - q1
    return int(((s < q1 - k*i) | (s > q3 + k*i)).sum())
def psi(ref, new, bins=10):
    ref, new = ref.dropna(), new.dropna(); e = np.quantile(ref, np.linspace(0, 1, bins+1)); e[0], e[-1] = -np.inf, np.inf
    a = np.histogram(ref, e)[0]/len(ref) + 1e-6; b = np.histogram(new, e)[0]/len(new) + 1e-6
    return float(((b-a)*np.log(b/a)).sum())
def root_cause(df, col, dims=("channel","country","product")):
    """Share of nulls in `col` by dimension value vs share of rows; lift>1 means the null is concentrated there."""
    rows = []
    bad = df[df[col].isna()]
    for d in dims:
        for v, n in bad[d].value_counts().items():
            share_bad, share_all = n/len(bad), (df[d] == v).mean()
            rows.append((col, d, v, int(n), round(share_bad/share_all, 2)))
    return pd.DataFrame(rows, columns=["column","dimension","value","bad_rows","lift"]).sort_values("lift", ascending=False)
def run(ref, new, db="data/dq.sqlite", run_id=None):
    run_id = run_id or dt.datetime.utcnow().isoformat(timespec="seconds"); rows = []
    for c, p in missing(new).items(): rows.append((run_id, "missing_rate", c, p, p > .01))
    rows.append((run_id, "duplicate_rows", "order_id", duplicates(new), duplicates(new) > 0))
    rows.append((run_id, "outliers_iqr", "amount", outliers(new.amount), outliers(new.amount) > 0))
    for c in ["amount"]: v = psi(ref[c], new[c]); rows.append((run_id, "psi_drift", c, v, v > .2))
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE IF NOT EXISTS dq_log (run_id TEXT, check_name TEXT, column_name TEXT, value REAL, failed INT)")
    con.executemany("INSERT INTO dq_log VALUES (?,?,?,?,?)", [(a,b,c,float(d),int(e)) for a,b,c,d,e in rows]); con.commit(); con.close()
    return pd.DataFrame(rows, columns=["run_id","check","column","value","failed"])
