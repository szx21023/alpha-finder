from loguru import logger
logger.disable("FinMind")

import twstock
import pandas as pd
from FinMind.data import DataLoader


def get_price(stock_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    """抓取台股历史股价数据。

    Args:
        stock_id: 股票代码（例如 '2330'）
        start_date: 开始日期（'YYYY-MM-DD'）
        end_date: 结束日期（'YYYY-MM-DD'）

    Returns:
        DataFrame with columns: Date, Open, High, Low, Close, Volume
    """
    dl = DataLoader()
    df = dl.taiwan_stock_daily(
        stock_id=stock_id,
        start_date=start_date,
        end_date=end_date,
    )
    if df.empty:
        print(f"[警告] 无法取得 {stock_id} 的股价数据")
        return pd.DataFrame()

    df = df.rename(columns={
        "date": "Date",
        "open": "Open",
        "max": "High",
        "min": "Low",
        "close": "Close",
        "Trading_Volume": "Volume",
    })
    return df[["Date", "Open", "High", "Low", "Close", "Volume"]]


def get_financials(stock_id: str) -> dict:
    """抓取台股基本面数据（最近一期财报）。

    Args:
        stock_id: 股票代码（例如 '2330'）

    Returns:
        dict with keys: name, pe, pb, roe, dividend_yield, revenue_growth
    """
    dl = DataLoader()

    # 取得股票名称
    info = twstock.codes.get(stock_id)
    name = info.name if info else "N/A"

    # 取得本益比、股价净值比、殖利率
    pe = None
    dividend_yield = None
    pb = None
    per_pbr = dl.taiwan_stock_per_pbr(stock_id=stock_id, start_date="2024-01-01")
    if not per_pbr.empty:
        latest = per_pbr.iloc[-1]
        pe = latest.get("PER")
        dividend_yield = latest.get("dividend_yield")
        pb = latest.get("PBR")

    # 取得营收数据计算年增率
    revenue_growth = None
    revenue = dl.taiwan_stock_month_revenue(stock_id=stock_id, start_date="2023-01-01")
    if not revenue.empty and "revenue" in revenue.columns:
        revenue = revenue.sort_values("date")
        if len(revenue) >= 13:
            latest_rev = revenue.iloc[-1]["revenue"]
            prev_year_rev = revenue.iloc[-13]["revenue"]
            if prev_year_rev and prev_year_rev > 0:
                revenue_growth = round((latest_rev - prev_year_rev) / prev_year_rev * 100, 2)

    return {
        "name": name,
        "pe": pe,
        "pb": pb,
        "dividend_yield": dividend_yield,
        "revenue_growth": revenue_growth,
    }
