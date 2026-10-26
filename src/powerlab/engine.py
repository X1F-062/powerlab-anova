"""TEK hesap motoru. CLI, MCP ve ajan yalnızca bunu (api.solve üzerinden) çağırır.

Matematik (standart, [DOK]): df1=k-1, df2=N-k, lambda=f^2*N,
guc = P(F'(df1,df2,lambda) > Fcrit), Fcrit = merkezi F'nin (1-alpha) kantili.

G*Power'a ÖZGÜ davranışlar PARAMS'ta toplanır. Her biri LEDGER.md'de bir [REA]
kaydına bağlanana kadar VARSAYIMDIR (değerin yanında 'ASSUMED' yazar).
"""
from __future__ import annotations
import math
from scipy import stats

PARAMS = {
    "min_total_n_extra": 1,          # ASSUMED: N >= k+1 (df2 >= 1). LEDGER: REA-05
    "n_ceiling": 10_000_000,         # ASSUMED. LEDGER: REA-04
    "round_up_to_multiple_of_k": True,   # HIPOTEZ [AJAN]: 158->159, 251->252 ile tutarli. GUI/REA ile dogrula: REA-01
    "tie_rule": ">=",                # ASSUMED (guc == hedef kabul). LEDGER: REA-02
    "out_digits": 4,                 # sözleşme örneği (4 hane). LEDGER: REA-03
}


class InputError(ValueError):
    pass


def _check(f=None, alpha=None, k=None, n=None, power=None):
    if k is not None and (int(k) != k or k < 2):
        raise InputError("groups (k) >= 2 tam sayi olmali")
    if f is not None and not (math.isfinite(f) and f > 0):
        raise InputError("f > 0 olmali")
    if alpha is not None and not (0 < alpha < 1):
        raise InputError("alpha (0,1) araliginda olmali")
    if power is not None and not (0 < power < 1):
        raise InputError("power (0,1) araliginda olmali")
    if n is not None and k is not None and not (n >= k + PARAMS["min_total_n_extra"]):
        raise InputError(f"n_total >= {k + PARAMS['min_total_n_extra']} olmali")


# ---------- etki büyüklüğü ----------
def f_from_eta2(eta2: float) -> float:
    if not (0 < eta2 < 1):
        raise InputError("eta2 (0,1) araliginda olmali")
    return math.sqrt(eta2 / (1 - eta2))


def f_from_means(means, sd, ns=None) -> float:
    """f = sigma_m / sigma (ns verilirse n-agirlikli)."""
    if sd is None or sd <= 0:
        raise InputError("sd > 0 olmali")
    if len(means) < 2:
        raise InputError("en az 2 ortalama gerekli")
    ns = ns or [1] * len(means)
    if len(ns) != len(means) or any(x <= 0 for x in ns):
        raise InputError("ns gecersiz")
    tot = sum(ns)
    gm = sum(m * n for m, n in zip(means, ns)) / tot
    var_m = sum(n * (m - gm) ** 2 for m, n in zip(means, ns)) / tot
    return math.sqrt(var_m) / sd


# ---------- çekirdek ----------
def ncp(f, n_total):
    return f * f * n_total


def critical(alpha, k, n_total):
    return float(stats.f.ppf(1 - alpha, k - 1, n_total - k))


def power(f, alpha, k, n_total):
    _check(f=f, alpha=alpha, k=k, n=n_total)
    return float(stats.ncf.sf(critical(alpha, k, n_total), k - 1, n_total - k, ncp(f, n_total)))


def _ok(p, target):
    return p >= target if PARAMS["tie_rule"] == ">=" else p > target


def apriori_n(f, alpha, power_target, k):
    """En küçük tam sayı toplam N: guc(N) >= hedef (güç N'de monoton)."""
    _check(f=f, alpha=alpha, k=k, power=power_target)
    lo = k + PARAMS["min_total_n_extra"]
    if _ok(power(f, alpha, k, lo), power_target):
        n = lo
    else:
        hi = lo
        while not _ok(power(f, alpha, k, hi), power_target):
            lo, hi = hi, hi * 2
            if hi > PARAMS["n_ceiling"]:
                raise InputError("N tavani asildi (etki cok kucuk)")
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if _ok(power(f, alpha, k, mid), power_target):
                hi = mid
            else:
                lo = mid
        n = hi
    if PARAMS["round_up_to_multiple_of_k"]:
        n = int(math.ceil(n / k) * k)
    return n
