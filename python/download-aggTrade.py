#!/usr/bin/env python

import sys
from enums import *
from utility import download_file, get_all_symbols, get_parser, get_path


def download_daily_aggTrades(
        trading_type,
        symbols,
        num_symbols,
        dates,
        folder,
        checksum
):
    current = 0
    date_range = None

    for symbol in symbols:
        print("[{}/{}] - start download daily {} aggTrades ".format(current + 1, num_symbols, symbol))
        for date in dates:
            path = get_path(trading_type, "aggTrades", "daily", symbol)
            file_name = "{}-aggTrades-{}.zip".format(symbol.upper(), date)
            print(f" ==== {path} ===== {file_name} ====")
            download_file(path, file_name, date_range, folder)

            if checksum == 1:
                checksum_path = get_path(trading_type, "aggTrades", "daily", symbol)
                checksum_file_name = "{}-aggTrades-{}.zip.CHECKSUM".format(symbol.upper(), date)
                download_file(checksum_path, checksum_file_name, date_range, folder)

        current += 1


if __name__ == "__main__":
    parser = get_parser('aggTrades')
    args = parser.parse_args(sys.argv[1:])

    if not args.symbols:
        print("fetching all symbols from exchange")
        symbols = get_all_symbols(args.type)
        num_symbols = len(symbols)
    else:
        symbols = args.symbols
        if "USDT" in symbols:
            symbols = [item for item in SYMBOL_LIST if item.endswith("USDT")]
        num_symbols = len(symbols)
        print("fetching {} symbols from exchange".format(num_symbols))

    if args.dates:
      dates = args.dates
    else:
      dates = []

    download_daily_aggTrades(
        args.type,
        symbols,
        num_symbols,
        dates,
        args.folder,
        args.checksum
    )
