import sys; sys.path.insert(0, "src")
import numpy as np, pandas as pd
from dq import missing, duplicates, outliers, psi, root_cause
def test_missing_and_dups():
    df = pd.DataFrame({"order_id": [1,1,2], "a": [1, None, 3]})
    assert duplicates(df) == 1 and abs(missing(df)["a"] - 1/3) < 1e-9
def test_outlier_detected():
    s = pd.Series([10]*100 + [1000]); assert outliers(s) == 1
def test_psi_zero_for_same_and_high_for_shift():
    r = np.random.default_rng(0); a = pd.Series(r.normal(0,1,5000)); b = pd.Series(r.normal(0,1,5000)); c = pd.Series(r.normal(2,1,5000))
    assert psi(a, b) < .05 and psi(a, c) > .2
def test_root_cause_finds_concentrated_null():
    df = pd.DataFrame({"channel": ["store"]*50 + ["web"]*50, "country": ["UK"]*100, "product": ["A"]*100, "amount": [None]*20 + [1.0]*30 + [1.0]*50})
    assert root_cause(df, "amount").iloc[0].value == "store"
