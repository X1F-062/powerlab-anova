"""Diferansiyel test: oracle/gpower_vectors.csv (GERÇEK G*Power gözlemleri) vs motor.
CSV başlığı: id,f,alpha,power,groups,n_total,actual_power,critical,df1,df2,ncp,screenshot
KAPI: n_total tam eşleşme >= %90. CSV yoksa test ATLANIR (sahte veri yok)."""
import csv, os, pytest
from src.powerlab.api import solve

P = os.path.join(os.path.dirname(__file__), "..", "oracle", "gpower_vectors.csv")


@pytest.mark.skipif(not os.path.exists(P), reason="oracle/gpower_vectors.csv henuz yok")
def test_gate_and_report():
    rows = list(csv.DictReader(open(P)))
    assert len(rows) >= 30, "en az 30 GUI vektoru gerekli"
    ok, diffs = 0, []
    for r in rows:
        o = solve(dict(mode="a-priori", f=float(r["f"]), alpha=float(r["alpha"]),
                       power=float(r["power"]), groups=int(r["groups"])))
        if o["n_total"] == int(r["n_total"]):
            ok += 1
        else:
            diffs.append((r["id"], o["n_total"], r["n_total"]))
    rate = ok / len(rows)
    with open(os.path.join(os.path.dirname(P), "..", "tests", "COMPLIANCE_REPORT.md"), "w") as fh:
        fh.write(f"# Uyum raporu\n\nN tam eslesme: {ok}/{len(rows)} = {rate:.1%}\n\n")
        fh.write("Uyusmazliklar (id, bizim, G*Power):\n" + "\n".join(map(str, diffs)) + "\n")
    assert rate >= 0.90, f"KAPI TUTMADI: {rate:.1%}; uyusmazliklar: {diffs[:5]}"
