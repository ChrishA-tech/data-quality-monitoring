import pandas as pd, sqlite3, os
from dq import run, root_cause
if os.path.exists("data/dq.sqlite"): os.remove("data/dq.sqlite")
ref, new = pd.read_csv("data/batch_ref.csv"), pd.read_csv("data/batch_new.csv")
res = run(ref, new); print(res.to_string(index=False)); print(root_cause(new, "amount").head(5).to_string(index=False))
