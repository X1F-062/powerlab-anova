"""CLI ve MCP'nin ORTAK giriş noktası: dict -> dict. Hesap mantığı burada YOK."""
from . import engine as E


def solve(p: dict) -> dict:
    test = p.get("test", "anova-oneway")
    if test != "anova-oneway":
        raise E.InputError(f"desteklenmeyen test: {test}")
    mode = p.get("mode")
    k = int(p.get("groups", 3))
    f = p.get("f")
    if f is None and p.get("eta2") is not None:
        f = E.f_from_eta2(p["eta2"])
    if f is None and p.get("means"):
        f = E.f_from_means(p["means"], p.get("sd"), p.get("ns"))
    if f is None:
        raise E.InputError("etki buyuklugu gerekli: f, eta2 veya means+sd")
    alpha = p.get("alpha")
    if mode == "a-priori":
        n = E.apriori_n(f, alpha, p.get("power"), k)
    elif mode == "post-hoc":
        n = p.get("n_total")
        if n is None:
            raise E.InputError("post-hoc icin n_total gerekli")
        n = float(n)
        if int(n) != n:
            raise E.InputError("n_total tam sayi olmali")
        n = int(n)
    else:
        raise E.InputError("mode a-priori veya post-hoc olmali")
    d = E.PARAMS["out_digits"]
    return {
        "n_total": n,
        "n_per_group": round(n / k, d),
        "actual_power": round(E.power(f, alpha, k, n), d),
        "critical": round(E.critical(alpha, k, n), d),
        "df1": k - 1,
        "df2": n - k,
        "ncp": round(E.ncp(f, n), d),
    }
