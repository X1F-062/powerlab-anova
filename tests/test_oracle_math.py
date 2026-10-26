"""Katman 1: matematik doğruluğu, G*Power'dan BAĞIMSIZ.
(a) Poisson-beta karışımı formülü (ncf'ten farklı yol), (b) Monte Carlo."""
import numpy as np
from scipy import stats
from src.powerlab import engine as E


def power_mixture(f, alpha, k, n):
    df1, df2, lam = k - 1, n - k, f * f * n
    fc = stats.f.ppf(1 - alpha, df1, df2)
    x = df1 * fc / (df1 * fc + df2)
    j = np.arange(0, int(lam + 20 * np.sqrt(lam + 1) + 50))
    return float(np.sum(stats.poisson.pmf(j, lam / 2) * stats.beta.sf(x, df1 / 2 + j, df2 / 2)))


def test_mixture_formula():
    for f, a, k, n in [(.25, .05, 3, 159), (.4, .01, 4, 60), (.1, .05, 3, 969), (.8, .05, 3, 12)]:
        assert abs(E.power(f, a, k, n) - power_mixture(f, a, k, n)) < 1e-9


def test_monte_carlo():
    rng = np.random.default_rng(7)
    f, a, k, m, reps = .25, .05, 3, 53, 100_000
    mu = np.array([-1., 0., 1.]); mu = mu / np.sqrt((mu ** 2).mean()) * f
    x = rng.standard_normal((reps, k, m)) + mu[None, :, None]
    gm = x.mean(2); g = gm.mean(1)
    F = (m * ((gm - g[:, None]) ** 2).sum(1) / (k - 1)) / (((x - gm[:, :, None]) ** 2).sum((1, 2)) / (k * m - k))
    mc = (F > stats.f.ppf(1 - a, k - 1, k * m - k)).mean()
    se = np.sqrt(mc * (1 - mc) / reps)
    assert abs(mc - E.power(f, a, k, k * m)) < 5 * se
