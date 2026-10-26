"""500+ ölçek vektörü (G*Power DEĞİL, scipy'den bağımsız bir yolla: Poisson-beta karışımı).
Çıktı: oracle/scale_vectors.csv. Kesirli N'yi de verir; G*Power yukarı yuvarlar
(bu fark başlı başına bulgudur, LEDGER'a yazın)."""
import csv, itertools, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from scipy import stats, optimize
from tests.test_oracle_math import power_mixture

rows = []
for f, a, pw, k in itertools.product([.05,.08,.1,.12,.15,.2,.25,.3,.35,.4,.45,.5,.6,.7,.8,1.0], [.01, .025, .05, .1],
                                      [.7, .8, .9, .95, .99], [3, 4, 5]):
    lo, hi = k + 1, k + 2
    while power_mixture(f, a, k, hi) < pw:
        lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if power_mixture(f, a, k, mid) >= pw: hi = mid
        else: lo = mid
    n = hi if power_mixture(f, a, k, k + 1) < pw else k + 1
    frac = optimize.brentq(lambda x: power_mixture(f, a, k, x) - pw, k + .5, n + 1)
    rows.append(dict(f=f, alpha=a, power=pw, groups=k, n_int=n, n_fractional=round(frac, 4)))
with open(os.path.join(os.path.dirname(__file__), "..", "oracle", "scale_vectors.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(len(rows), "vektor")
