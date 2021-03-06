import joblib
from datetime import datetime, timedelta
import time
import requests
import pandas as pd
import numpy as np
import os
import ccxt
import traceback

from features import features,calc_features

#Line通知
class LineNotify:
    def __init__(self):
        self.line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")
        self.line_notify_api = "https://notify-api.line.me/api/notify"
        self.headers = {
            "Authorization": f"Bearer {self.line_notify_token}"
        }

    def send(self, msg):
        msg = { "message": f" {msg}" }
        requests.post(self.line_notify_api, headers = self.headers, data = msg)

#BinanceのOHLCV情報を取得
def get_binance_ohlcv(market,from_time,interval_sec,limit):
    ohlcv_list = ccxt.binance().fapiPublicGetKlines({
        'symbol': market,
        'startTime': from_time,
        'interval': format_interval_sec(interval_sec),
        'limit': limit
    })

    df = pd.DataFrame(ohlcv_list,columns=['timestamp',
                'op',
                'hi',
                'lo',
                'cl',
                'volume',
                'close_time',
                'quote_asset_volume',
                'trades',
                'taker_buy_base_asset_volume',
                'taker_buy_quote_asset_volume',
                'ignore',]) [['timestamp', 'op', 'hi', 'lo', 'cl', 'volume']]

    df = df[from_time <= df['timestamp'].astype('int64')]
    df['timestamp'] = pd.to_datetime(df['timestamp'] , unit='ms')
    df.set_index("timestamp",inplace=True)
    df["op"]=df["op"].astype(float)
    df["hi"]=df["hi"].astype(float)
    df["lo"]=df["lo"].astype(float)
    df["cl"]=df["cl"].astype(float)
    df["volume"]=df["volume"].astype(float)
    df.sort_index(inplace=True)
    return df

def format_interval_sec(interval_sec):
    interval_min = interval_sec // 60
    if interval_min < 60:
        return '{}m'.format(interval_min)
    if interval_min < 24 * 60:
        return '{}h'.format(interval_min // 60)
    else:
        return '{}d'.format(interval_min // (24 * 60))


#ポジション情報を取得

def get_binance_position(binance,market):
    poss = binance.fapiPrivateGetPositionRisk()
    positionAmt = 0.0

    market_history = [d.get('symbol') for d in poss]  #銘柄だけを抽出
    market_index = market_history.index(market) #探している銘柄が何番目に存在するか
    print(poss[market_index])

    positionAmt = float(poss[market_index]['positionAmt'])
    positionSide = str(poss[market_index]['positionSide'])

    if positionAmt == 0:
        positionSide = 'NONE'
    elif positionAmt > 0:
        positionSide = 'BUY'
    else:
        positionSide = 'SELL'
    return {'positionSide':positionSide, 'positionAmt':positionAmt}


#Binanceへ注文
def order_binance(exchange,market,order_side,order_size):
    order = exchange.fapiPrivate_post_order(
        {
            "symbol": market,#銘柄の指定
            "side": order_side, #ロングorショート
            "type": "MARKET", #指値の場合はLIMIT
            "quantity": order_size, #何枚ポジションを持つか
            # "price":order_price,
            # "timeInForce": "GTC",
            # "reduce_only": reduce,
        }
    )
    print(order)


#ボット起動
def start(exchange, interval_sec):

    print("binance Bot is started!\n interval:{0}sec".format(interval_sec))

    #追加
    line_notify = LineNotify()
    line_notify.send("Binance Bot起動")
    line_notify.send("\n{0}分足".format(30))

    while True:

        dt_now = datetime.now()

        #指定した時間間隔ごとに実行
        if dt_now.minute % 30 == 0:

            try:

                line_notify.send("30分経過")

            #OHLCV情報を取得
                time_now = datetime.now()
                from_time = int((time_now + timedelta(minutes= - 100000 * interval_sec)).timestamp())
                limit = 200

                #AVAXUSDT------------------------------
                market_AVAX = 'AVAXUSDT'
                df_AVAX = get_binance_ohlcv(market_AVAX,from_time,interval_sec,limit)

                df_AVAX_features = calc_features(df_AVAX)
                position_AVAX = get_binance_position(exchange, market_AVAX)

                print("{0}のポジションサイド:{1}".format(str(market_AVAX),str(position_AVAX['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_AVAX),str(position_AVAX['positionAmt'])))

                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_AVAX),str(position_AVAX['positionSide'])))
                line_notify.send("{0}のポジションサイズ:{1}".format(str(market_AVAX),str(position_AVAX['positionAmt'])))

                #DOTUSDT------------------------------
                market_DOT = 'DOTUSDT'
                df_DOT = get_binance_ohlcv(market_DOT,from_time,interval_sec,limit)

                df_DOT_features = calc_features(df_DOT)
                position_DOT = get_binance_position(exchange, market_DOT)

                print("{0}のポジションサイド:{1}".format(str(market_DOT),str(position_DOT['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_DOT),str(position_DOT['positionAmt'])))

                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_DOT),str(position_DOT['positionSide'])))
                line_notify.send("{0}のポジションサイズ:{1}".format(str(market_DOT),str(position_DOT['positionAmt'])))

                #VETUSDT------------------------------
                market_VET = 'VETUSDT'
                df_VET = get_binance_ohlcv(market_VET,from_time,interval_sec,limit)

                df_VET_features = calc_features(df_VET)
                position_VET = get_binance_position(exchange, market_VET)

                print("{0}のポジションサイド:{1}".format(str(market_VET),str(position_VET['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_VET),str(position_VET['positionAmt'])))

                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_VET),str(position_VET['positionSide'])))
                line_notify.send("{0}のポジションサイズ:{1}".format(str(market_VET),str(position_VET['positionAmt'])))

                #NEARUSDT------------------------------
                market_NEAR = 'NEARUSDT'
                df_NEAR = get_binance_ohlcv(market_NEAR,from_time,interval_sec,limit)

                df_NEAR_features = calc_features(df_NEAR)
                position_NEAR = get_binance_position(exchange, market_NEAR)

                print("{0}のポジションサイド:{1}".format(str(market_NEAR),str(position_NEAR['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_NEAR),str(position_NEAR['positionAmt'])))

                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_NEAR),str(position_NEAR['positionSide'])))
                line_notify.send("{0}のポジションサイズ:{1}".format(str(market_NEAR),str(position_NEAR['positionAmt'])))

                #MANAUSDT------------------------------
                market_MANA = 'MANAUSDT'
                df_MANA = get_binance_ohlcv(market_MANA,from_time,interval_sec,limit)

                df_MANA_features = calc_features(df_MANA)
                position_MANA = get_binance_position(exchange, market_MANA)

                print("{0}のポジションサイド:{1}".format(str(market_MANA),str(position_MANA['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_MANA),str(position_MANA['positionAmt'])))

                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_MANA),str(position_MANA['positionSide'])))
                line_notify.send("{0}のポジションサイズ:{1}".format(str(market_MANA),str(position_MANA['positionAmt'])))

                #LUNAUSDT------------------------------
#                 market_LUNA = 'LUNAUSDT'
#                 df_LUNA = get_binance_ohlcv(market_LUNA,from_time,interval_sec,limit)

#                 df_LUNA_features = calc_features(df_LUNA)
#                 position_LUNA = get_binance_position(exchange, market_LUNA)

#                 print("{0}のポジションサイド:{1}".format(str(market_LUNA),str(position_LUNA['positionSide'])))
#                 print("{0}のポジションサイズ:{1}".format(str(market_LUNA),str(position_LUNA['positionAmt'])))

#                 # line_notify.send("{0}のポジションサイド:{1}".format(str(market_MANA),str(position_MANA['positionSide'])))
#                 line_notify.send("{0}のポジションサイズ:{1}".format(str(market_LUNA),str(position_LUNA['positionAmt'])))

                #SOLUSDT------------------------------
                market_SOL = 'SOLUSDT'
                df_SOL = get_binance_ohlcv(market_SOL,from_time,interval_sec,limit)

                df_SOL_features = calc_features(df_SOL)
                position_SOL = get_binance_position(exchange, market_SOL)

                print("{0}のポジションサイド:{1}".format(str(market_SOL),str(position_SOL['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_SOL),str(position_SOL['positionAmt'])))

                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_MANA),str(position_MANA['positionSide'])))
                line_notify.send("{0}のポジションサイズ:{1}".format(str(market_SOL),str(position_SOL['positionAmt'])))

                #ENJUSDT------------------------------
                market_ENJ = 'ENJUSDT'
                df_ENJ = get_binance_ohlcv(market_ENJ,from_time,interval_sec,limit)

                df_ENJ_features = calc_features(df_ENJ)
                position_ENJ = get_binance_position(exchange, market_ENJ)

                print("{0}のポジションサイド:{1}".format(str(market_ENJ),str(position_ENJ['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_ENJ),str(position_ENJ['positionAmt'])))

                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_MANA),str(position_MANA['positionSide'])))
                line_notify.send("{0}のポジションサイズ:{1}".format(str(market_ENJ),str(position_ENJ['positionAmt'])))

                #ADAUSDT------------------------------
                market_ADA = 'ADAUSDT'
                df_ADA = get_binance_ohlcv(market_ADA,from_time,interval_sec,limit)

                df_ADA_features = calc_features(df_ADA)
                position_ADA = get_binance_position(exchange, market_ADA)

                print("{0}のポジションサイド:{1}".format(str(market_ADA),str(position_ADA['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_ADA),str(position_ADA['positionAmt'])))

                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_MANA),str(position_MANA['positionSide'])))
                line_notify.send("{0}のポジションサイズ:{1}".format(str(market_ADA),str(position_ADA['positionAmt'])))

            #注文処理ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

                order_side = "NONE"

            #エグジットーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

                #AVAXUSDT------------------------------
                #ロングクローズ
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "SELL"
                    order_size = abs(position_AVAX["positionAmt"])
                    order_binance(exchange,market_AVAX,order_side,order_size)
                #ショートクローズ
                # if position["side"] == "SELL":
                #     order_side = "BUY"
                #     order_size = abs(position["size"])
                #     order_bybit(exchange,order_side,order_size)


                #DOTUSDT------------------------------
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "SELL"
                    order_size = abs(position_DOT["positionAmt"])
                    order_binance(exchange,market_DOT,order_side,order_size)

                #VETUSDT------------------------------
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "SELL"
                    order_size = abs(position_VET["positionAmt"])
                    order_binance(exchange,market_VET,order_side,order_size)

                #NEARUSDT------------------------------
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "SELL"
                    order_size = abs(position_NEAR["positionAmt"])
                    order_binance(exchange,market_NEAR,order_side,order_size)

                #MANAUSDT------------------------------
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "SELL"
                    order_size = abs(position_MANA["positionAmt"])
                    order_binance(exchange,market_MANA,order_side,order_size)

                #LUNAUSDT------------------------------
#                 #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
#                     order_side = "SELL"
#                     order_size = abs(position_LUNA["positionAmt"])
#                     order_binance(exchange,market_LUNA,order_side,order_size)

                #SOLUSDT------------------------------
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "SELL"
                    order_size = abs(position_SOL["positionAmt"])
                    order_binance(exchange,market_SOL,order_side,order_size)

                #ENJUSDT------------------------------
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "SELL"
                    order_size = abs(position_ENJ["positionAmt"])
                    order_binance(exchange,market_ENJ,order_side,order_size)

                #ADAUSDT------------------------------
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "SELL"
                    order_size = abs(position_ADA["positionAmt"])
                    order_binance(exchange,market_ADA,order_side,order_size)

            #エントリーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

                #AVAXUSDT------------------------------
                #ロングエントリー
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "BUY"
                    order_size = 1
                    order_binance(exchange,market_AVAX,order_side,order_size)
                #ショートエントリー
                # if ( ) & () & (position["positionAmt"] == 0):
                #     order_side = "SELL"
                #     order_size = 1
                #     order_binance(exchange,market,order_side,order_size)

                #DOTUSDT------------------------------
                #ロングエントリー
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "BUY"
                    order_size = 5
                    order_binance(exchange,market_DOT,order_side,order_size)

                #VETUSDT------------------------------
                #ロングエントリー
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "BUY"
                    order_size = 1600
                    order_binance(exchange,market_VET,order_side,order_size)

                #NEARUSDT------------------------------
                #ロングエントリー
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "BUY"
                    order_size = 8
                    order_binance(exchange,market_NEAR,order_side,order_size)

                #MANAUSDT------------------------------
                #ロングエントリー
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "BUY"
                    order_size = 30
                    order_binance(exchange,market_MANA,order_side,order_size)

                #LUNAUSDT------------------------------
                #ロングエントリー
#                 #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
#                     order_side = "BUY"
#                     order_size = 1.0
#                     order_binance(exchange,market_LUNA,order_side,order_size)

                #SOLUSDT------------------------------
                #ロングエントリー
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "BUY"
                    order_size = 1.0
                    order_binance(exchange,market_SOL,order_side,order_size)

                #ENJUSDT------------------------------
                #ロングエントリー
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "BUY"
                    order_size = 50
                    order_binance(exchange,market_ENJ,order_side,order_size)

                #ADAUSDT------------------------------
                #ロングエントリー
               #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    order_side = "BUY"
                    order_size = 100
                    order_binance(exchange,market_ADA,order_side,order_size)

            except Exception as e:
                print(traceback.format_exc())
                #追加
                line_notify.send("\n 何らかのエラー")
                pass


        # アノマリーロジック
        weekday = datetime.now().weekday()

        #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
            try:
                line_notify.send("午後の●時です")

                market_ETH = "ETHUSDT"
                position_ETH = get_binance_position(exchange, market_ETH)
                print("{0}のポジションサイド:{1}".format(str(market_ETH),str(position_ETH['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_ETH),str(position_ETH['positionAmt'])))
                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_ETH),str(position_ETH['positionSide'])))
                # line_notify.send("{0}のポジションサイズ:{1}".format(str(market_ETH),str(position_ETH['positionAmt'])))

                #ショートクローズ
                if (position_ETH['positionSide'] == "SELL"):
                    order_side = "BUY"
                    order_size = abs(position_ETH["positionAmt"])
                    order_binance(exchange,market_ETH,order_side,order_size)

                    line_notify.send("ショートクローズ")

                #ロングエントリー
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    line_notify.send("ロングエントリー")

                    order_side = "BUY"
                    order_size = 0.05
                    order_binance(exchange,market_ETH,order_side,order_size)

            except Exception as e:
                print(traceback.format_exc())
                #追加
                line_notify.send("\n 何らかのエラー")
                pass


        #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
            try:
                line_notify.send("午前の●時です")

                market_ETH = "ETHUSDT"
                position_ETH = get_binance_position(exchange, market_ETH)
                print("{0}のポジションサイド:{1}".format(str(market_ETH),str(position_ETH['positionSide'])))
                print("{0}のポジションサイズ:{1}".format(str(market_ETH),str(position_ETH['positionAmt'])))
                # line_notify.send("{0}のポジションサイド:{1}".format(str(market_ETH),str(position_ETH['positionSide'])))
                # line_notify.send("{0}のポジションサイズ:{1}".format(str(market_ETH),str(position_ETH['positionAmt'])))

               
                #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                    line_notify.send("ロングクローズのみ")

                    if (position_ETH['positionSide'] == "BUY"):
                        order_side = "SELL"
                        order_size = abs(position_ETH["positionAmt"])
                        order_binance(exchange,market_ETH,order_side,order_size)

                
                else:
                    if (position_ETH['positionSide'] == "BUY"):
                        order_side = "SELL"
                        order_size = abs(position_ETH["positionAmt"])
                        order_binance(exchange,market_ETH,order_side,order_size)

                    #if ーーーーーーーーーーーーーーーーーーーーーー略ーーーーーーーーーーーーーーーーーーーーーーーーーーー : 
                        line_notify.send("ショートエントリー")

                        order_side = "SELL"
                        order_size = 0.05
                        order_binance(exchange,market_ETH,order_side,order_size)


            except Exception as e:
                print(traceback.format_exc())
                #追加
                line_notify.send("\n 何らかのエラー")
                pass

        time.sleep(60)

if __name__  == '__main__':

    apiKey    = os.getenv("API_KEY")
    secretKey = os.getenv("SECRET_KEY")
    interval_sec = int(os.getenv("INTERVAL_SEC"))

    exchange = ccxt.binance({"apiKey":apiKey, "secret":secretKey, "options": {"defaultType": "future"}, "enableRateLimit": True})
    start(exchange, interval_sec)
