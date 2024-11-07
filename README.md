# binance-public-data
执行命令:  python3 ./binance-public-data/python/download-aggTrade.py -s USDT -d '2024-01-01' -t um -c 1
会下载 https://data.binance.vision/?prefix=data/futures/um/daily/aggTrades/地址下所有以USDT结尾的文件夹中
2024年1月1日的zip压缩文件数据，并存储在 data 目录下。

启动 main.py 文件将对下载的数据进行解压及完整性校验，并将其转换为.pickle文件进行存储。