import csv, os, pytest
from src.powerlab.api import solve
P = os.path.join(os.path.dirname(__file__), "..", "oracle", "scale_vectors.csv")

@pytest.mark.skipif(not os.path.exists(P), reason="gen_scale_vectors.py calistirilmadi")
def test_scale_agreement():
    rows = list(csv.DictReader(open(P)))
    from src.powerlab import engine as E
    up = (lambda n, k: -(-n // k) * k) if E.PARAMS["round_up_to_multiple_of_k"] else (lambda n, k: n)
    bad = [r for r in rows if solve(dict(mode="a-priori", f=float(r["f"]), alpha=float(r["alpha"]),
           power=float(r["power"]), groups=int(r["groups"])))["n_total"] != up(int(r["n_int"]), int(r["groups"]))]
    assert not bad, bad[:3]
