"""İnce CLI. Sözleşme: tek satır JSON; hata -> {"error":...} + çıkış kodu 2.
UYARI: anova-oneway parametre adları CONTRACT.md ile karşılaştırılmalı."""
import argparse, json, sys
from . import engine as E
from .api import solve


def main(argv=None):
    p = argparse.ArgumentParser(prog="gpower-clone")
    p.add_argument("--test", default="anova-oneway")
    p.add_argument("--mode", required=True, choices=["a-priori", "post-hoc"])
    p.add_argument("--f", type=float)
    p.add_argument("--eta2", type=float)
    p.add_argument("--means", type=float, nargs="+")
    p.add_argument("--sd", type=float)
    p.add_argument("--ns", type=float, nargs="+")
    p.add_argument("--alpha", type=float, required=True)
    p.add_argument("--power", type=float)
    p.add_argument("--n_total", type=float)
    p.add_argument("--groups", type=int, default=3)
    try:
        a = p.parse_args(argv)
    except SystemExit:
        print(json.dumps({"error": "gecersiz arguman"}))
        return 2
    try:
        out = solve({k: v for k, v in vars(a).items() if v is not None})
    except (E.InputError, TypeError) as e:
        print(json.dumps({"error": str(e)}))
        return 2
    print(json.dumps(out, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
