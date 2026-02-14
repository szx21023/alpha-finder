import argparse
import yaml
from src.data import get_us_price, get_us_financials, get_tw_price, get_tw_financials


def load_config(path="config/settings.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def parse_args():
    config = load_config()
    parser = argparse.ArgumentParser(description="Alpha Finder - 股票数据收集工具")
    parser.add_argument("--ticker", required=True, help="股票代码（例如 AAPL、2330）")
    parser.add_argument("--market", choices=["us", "tw"], required=True, help="市场：us（美股）或 tw（台股）")
    parser.add_argument("--start", default=config["backtest"]["start_date"], help="开始日期（YYYY-MM-DD）")
    parser.add_argument("--end", default=config["backtest"]["end_date"], help="结束日期（YYYY-MM-DD）")
    return parser.parse_args()


def show_stock(ticker, market, start_date, end_date):
    if market == "us":
        get_price = get_us_price
        get_financials = get_us_financials
    else:
        get_price = get_tw_price
        get_financials = get_tw_financials

    # 股价数据
    print("=" * 60)
    price = get_price(ticker, start_date, end_date)
    if not price.empty:
        name_label = f"{market.upper()} - {ticker}"
        print(f"{name_label}  股价数据（{start_date} ~ {end_date}）")
        print("=" * 60)
        print(f"\n最近 10 笔:")
        print(price.tail(10).to_string(index=False))
        print(f"\n总共 {len(price)} 笔数据")
        print(f"最高收盘: {price['Close'].max()}")
        print(f"最低收盘: {price['Close'].min()}")

        first_close = price.iloc[0]["Close"]
        last_close = price.iloc[-1]["Close"]
        change = (last_close - first_close) / first_close * 100
        print(f"区间涨跌幅: {change:+.2f}%")

    # 基本面数据
    print(f"\n基本面数据:")
    financials = get_financials(ticker)
    for key, value in financials.items():
        print(f"  {key}: {value}")


def main():
    args = parse_args()
    show_stock(args.ticker, args.market, args.start, args.end)


if __name__ == "__main__":
    main()
