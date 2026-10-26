"""MCP adaptörü (+15). İnce katman: yalnızca api.solve çağırır.
Kurulum: pip install mcp   |  Çalıştır: python -m src.powerlab.mcp_server
NOT: Bu dosya yazarken test ortamında 'mcp' paketi yoktu; kendi makinenizde
çalıştırıp doğrulayın (README'deki MCP bölümü)."""
from mcp.server.fastmcp import FastMCP
from .api import solve
from . import engine as E

mcp = FastMCP("powerlab-anova")


@mcp.tool()
def anova_oneway(mode: str, alpha: float, groups: int = 3, f: float | None = None,
                 eta2: float | None = None, power: float | None = None,
                 n_total: int | None = None) -> dict:
    """Tek yonlu ANOVA: mode='a-priori' (power ver, N hesapla) veya 'post-hoc' (n_total ver, guc hesapla)."""
    args = {"test": "anova-oneway", "mode": mode, "alpha": alpha, "groups": groups,
            "f": f, "eta2": eta2, "power": power, "n_total": n_total}
    try:
        return solve({k: v for k, v in args.items() if v is not None})
    except E.InputError as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()
