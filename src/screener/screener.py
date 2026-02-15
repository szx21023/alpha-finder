import sys

import pandas as pd

from src.data import get_tw_financials, get_us_financials
from src.screener.universe import get_tw_universe, get_sp500_tickers


def _passes_filter(financials: dict, criteria: dict) -> bool:
    """檢查單檔股票是否通過所有篩選條件。資料為 None 時跳過該條件。"""
    checks = [
        ("pe", "pe_max", lambda v, t: v <= t),
        ("roe", "roe_min", lambda v, t: v >= t),
        ("dividend_yield", "dividend_yield_min", lambda v, t: v >= t),
        ("revenue_growth", "revenue_growth_min", lambda v, t: v >= t),
    ]
    for field, config_key, compare in checks:
        threshold = criteria.get(config_key)
        value = financials.get(field)
        if threshold is None or value is None:
            continue
        if not compare(value, threshold):
            return False
    return True


def screen(market: str, config: dict) -> pd.DataFrame:
    """執行基本面篩選。

    Args:
        market: 'tw' 或 'us'
        config: 完整的 settings.yaml 設定 dict

    Returns:
        DataFrame with qualifying stocks and their fundamental metrics
    """
    if market == "tw":
        tickers = get_tw_universe()
        get_financials = get_tw_financials
        criteria = config["tw_stock"]["screener"]
        label = "台股"
    else:
        tickers = get_sp500_tickers()
        get_financials = get_us_financials
        criteria = config["us_stock"]["screener"]
        label = "美股"

    total = len(tickers)
    results = []

    for i, ticker in enumerate(tickers, 1):
        sys.stdout.write(f"\r正在篩選{label}... ({i}/{total})")
        sys.stdout.flush()

        try:
            financials = get_financials(ticker)
        except Exception:
            continue

        if _passes_filter(financials, criteria):
            financials["ticker"] = ticker
            results.append(financials)

    # 換行，結束進度顯示
    print()

    if not results:
        print(f"\n沒有符合條件的{label}標的。")
        return pd.DataFrame()

    df = pd.DataFrame(results)

    # 整理欄位順序
    if market == "tw":
        columns = ["ticker", "name", "pe", "pb", "roe", "dividend_yield", "revenue_growth"]
    else:
        columns = ["ticker", "name", "pe", "forward_pe", "pb", "roe",
                    "dividend_yield", "revenue_growth", "market_cap"]

    # 只保留存在的欄位
    columns = [c for c in columns if c in df.columns]
    df = df[columns].sort_values("ticker").reset_index(drop=True)

    print(f"\n{'=' * 70}")
    print(f" {label}篩選結果（共 {len(df)} 檔符合條件）")
    print(f"{'=' * 70}")
    print(f" 篩選條件: ", end="")
    cond_parts = []
    if criteria.get("pe_max") is not None:
        cond_parts.append(f"PE <= {criteria['pe_max']}")
    if criteria.get("roe_min") is not None:
        cond_parts.append(f"ROE >= {criteria['roe_min']}%")
    if criteria.get("dividend_yield_min") is not None:
        cond_parts.append(f"殖利率 >= {criteria['dividend_yield_min']}%")
    if criteria.get("revenue_growth_min") is not None:
        cond_parts.append(f"營收成長 >= {criteria['revenue_growth_min']}%")
    print(" | ".join(cond_parts))
    print(f"{'=' * 70}")
    print(df.to_string(index=False))

    return df
