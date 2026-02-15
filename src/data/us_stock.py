import yfinance as yf
import pandas as pd


def get_price(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """抓取美股历史股价数据。

    Args:
        ticker: 股票代码（例如 'AAPL'）
        start_date: 开始日期（'YYYY-MM-DD'）
        end_date: 结束日期（'YYYY-MM-DD'）

    Returns:
        DataFrame with columns: Date, Open, High, Low, Close, Volume
    """
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    if df.empty:
        print(f"[警告] 无法取得 {ticker} 的股价数据")
        return pd.DataFrame()

    df = df[["Open", "High", "Low", "Close", "Volume"]].reset_index()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    return df


def get_financials(ticker: str) -> dict:
    """抓取美股基本面数据。

    Args:
        ticker: 股票代码（例如 'AAPL'）

    Returns:
        dict with keys: name, pe, forward_pe, pb, roe, dividend_yield,
                        revenue_growth, market_cap
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "name": info.get("shortName", "N/A"),
        "pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "pb": info.get("priceToBook"),
        "roe": round(info["returnOnEquity"] * 100, 2) if info.get("returnOnEquity") is not None else None,
        "dividend_yield": round(info["dividendYield"] * 100, 2) if info.get("dividendYield") is not None else None,
        "revenue_growth": round(info["revenueGrowth"] * 100, 2) if info.get("revenueGrowth") is not None else None,
        "market_cap": info.get("marketCap"),
    }
