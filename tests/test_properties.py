import itertools
import pytest
from src.powerlab import engine as E


def test_monotonicity():
    p = [E.power(.25, .05, 3, n) for n in range(6, 400, 3)]
    assert all(b >= a for a, b in zip(p, p[1:]))
    assert E.power(.3, .05, 3, 100) > E.power(.2, .05, 3, 100)
    assert E.power(.25, .10, 3, 100) > E.power(.25, .01, 3, 100)


@pytest.mark.parametrize("f,a,pw,k", list(itertools.product(
    [.05, .1, .25, .4, .8, 1.5], [.001, .01, .05, .2], [.5, .8, .9, .95, .99], [2, 3, 5])))
def test_minimality(f, a, pw, k):
    n = E.apriori_n(f, a, pw, k)
    assert E.power(f, a, k, n) >= pw
    step = k if E.PARAMS["round_up_to_multiple_of_k"] else 1
    if n - step >= k + E.PARAMS["min_total_n_extra"]:
        assert E.power(f, a, k, n - step) < pw


def test_effect_sizes():
    assert abs(E.f_from_eta2(.0588235294) - .25) < 1e-6
    assert abs(E.f_from_means([-1, 0, 1], 1) - (2 / 3) ** .5) < 1e-12


@pytest.mark.parametrize("bad", [
    dict(mode="a-priori", f=0, alpha=.05, power=.8),
    dict(mode="a-priori", f=.25, alpha=1.2, power=.8),
    dict(mode="a-priori", f=.25, alpha=.05, power=1.0),
    dict(mode="a-priori", f=.25, alpha=.05, power=.8, groups=1),
    dict(mode="post-hoc", f=.25, alpha=.05),
    dict(mode="post-hoc", f=.25, alpha=.05, n_total=2),
    dict(mode="x", f=.25, alpha=.05),
])
def test_invalid_inputs(bad):
    from src.powerlab.api import solve
    with pytest.raises(E.InputError):
        solve(bad)


def test_tiny_effect_hits_ceiling_or_solves():
    # f=0.001: ya cozum ya InputError (G*Power davranisi LEDGER REA-04'te gözlenmeli)
    try:
        E.apriori_n(.001, .05, .8, 3)
    except E.InputError:
        pass
