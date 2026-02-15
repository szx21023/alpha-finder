import argparse
import yaml
from src.data import get_us_price, get_us_financials, get_tw_price, get_tw_financials
from src.screener import screen


def load_config(path="config/settings.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def cmd_show(args):
    """個股查詢命令。"""
    config = load_config()
    start = args.start or config["backtest"]["start_date"]
    end = args.end or config["backtest"]["end_date"]

    if args.market == "us":
        get_price = get_us_price
        get_financials = get_us_financials
    else:
        get_price = get_tw_price
        get_financials = get_tw_financials

    # 股价数据
    print("=" * 60)
    price = get_price(args.ticker, start, end)
    if not price.empty:
        name_label = f"{args.market.upper()} - {args.ticker}"
        print(f"{name_label}  股价数据（{start} ~ {end}）")
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
    financials = get_financials(args.ticker)
    for key, value in financials.items():
        print(f"  {key}: {value}")


def cmd_screen(args):
    """篩選命令。"""
    config = load_config()
    screen(args.market, config)


def main():
    parser = argparse.ArgumentParser(description="Alpha Finder - 股票分析工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # show 子命令
    show_parser = subparsers.add_parser("show", help="查詢個股數據")
    show_parser.add_argument("--ticker", required=True, help="股票代碼（例如 AAPL、2330）")
    show_parser.add_argument("--market", choices=["us", "tw"], required=True, help="市場：us 或 tw")
    show_parser.add_argument("--start", default=None, help="開始日期（YYYY-MM-DD）")
    show_parser.add_argument("--end", default=None, help="結束日期（YYYY-MM-DD）")

    # screen 子命令
    screen_parser = subparsers.add_parser("screen", help="基本面篩選")
    screen_parser.add_argument("--market", choices=["us", "tw"], required=True, help="市場：us 或 tw")

    args = parser.parse_args()

    if args.command == "show":
        cmd_show(args)
    elif args.command == "screen":
        cmd_screen(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
