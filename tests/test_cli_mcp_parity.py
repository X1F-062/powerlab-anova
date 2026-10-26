"""CLI ile ortak katman (MCP'nin çağırdığı api.solve) aynı girdide aynı çıktıyı vermeli."""
import json, subprocess, sys, os
from src.powerlab.api import solve

ROOT = os.path.dirname(os.path.dirname(__file__))
CASES = [
    (["--mode", "a-priori", "--f", "0.25", "--alpha", "0.05", "--power", "0.8", "--groups", "3"],
     dict(mode="a-priori", f=.25, alpha=.05, power=.8, groups=3)),
    (["--mode", "post-hoc", "--f", "0.25", "--alpha", "0.05", "--n_total", "100", "--groups", "3"],
     dict(mode="post-hoc", f=.25, alpha=.05, n_total=100, groups=3)),
]


def run(args):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "gpower-clone")] + args, capture_output=True, text=True)
    return r.returncode, json.loads(r.stdout)


def test_parity():
    for args, d in CASES:
        rc, out = run(args)
        assert rc == 0 and out == solve(d)


def test_error_contract():
    rc, out = run(["--mode", "a-priori", "--f", "0", "--alpha", "0.05", "--power", "0.8"])
    assert rc != 0 and "error" in out


def test_known_sanity():
    # [AJAN]/[DOK]-düzeyi: G*Power'da KENDİNİZ doğrulayana kadar golden değildir.
    assert solve(CASES[0][1])["n_total"] == 159
    assert solve(dict(mode="a-priori", f=.25, alpha=.05, power=.95))["n_total"] == 252
