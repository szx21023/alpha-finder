from __future__ import annotations
from io import StringIO

import requests
import twstock
import pandas as pd


def get_tw_universe() -> list[str]:
    """取得台股上市櫃股票代碼清單（排除 ETF、權證等）。

    Returns:
        list of stock IDs (e.g. ['1101', '1102', '2330', ...])
    """
    codes = []
    for code, info in twstock.codes.items():
        # 只保留上市(TWSE)和上櫃(OTC)的一般股票
        if info.type == "股票" and info.market in ("上市", "上櫃"):
            codes.append(code)
    return sorted(codes)


def get_sp500_tickers() -> list[str]:
    """從 Wikipedia 抓取 S&P 500 成分股清單。

    Returns:
        list of ticker symbols (e.g. ['AAPL', 'MSFT', ...])
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0 (AlphaFinder)"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    tables = pd.read_html(StringIO(resp.text))
    df = tables[0]
    tickers = df["Symbol"].str.replace(".", "-", regex=False).tolist()
    return sorted(tickers)
