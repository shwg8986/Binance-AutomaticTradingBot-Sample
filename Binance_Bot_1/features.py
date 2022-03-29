import talib

features = sorted([
    'EMA',
])


def calc_features(df):
    open = df['op']
    high = df['hi']
    low = df['lo']
    close = df['cl']
    volume = df['volume']

    orig_columns = df.columns
    hilo = (df['hi'] + df['lo']) / 2


    df['diff'] = (close - close.shift(1)) / close * 100

    #AVAXUSDT-1用
    # df['ema_diff1'] = talib.EMA(df['diff'], timeperiod=10) #直前の値動きのMA
    # df['sig1'] = df['ema_diff1'] - df['ema_diff1'].shift(18) #直前の値動きのMAと過去の差分

    #AVAXUSDT-2用
    df['ema_diff1'] = talib.EMA(df['diff'], timeperiod=10) #直前の値動きのMA
    df['sig1'] = df['ema_diff1'] - df['ema_diff1'].shift(9) #直前の値動きのMAと過去の差分

    #DOTUSDT用, NEARUSDT用, LUNAUSDT用
    df['ema_diff2'] = talib.EMA(df['diff'], timeperiod=8) #直前の値動きのMA
    df['sig2'] = df['ema_diff2'] - df['ema_diff2'].shift(18) #直前の値動きのMAと過去の差分

    #VETUSDT用, MANAUSDT用, SOLUSDT用, ENJ用
    df['ema_diff3'] = talib.EMA(df['diff'], timeperiod=10) #直前の値動きのMA
    df['sig3'] = df['ema_diff3'] - df['ema_diff3'].shift(16) #直前の値動きのMAと過去の差分

    #ADAUSDT用,
    df['ema_diff4'] = talib.EMA(df['diff'], timeperiod=10) #直前の値動きのMA
    df['sig4'] = df['ema_diff4'] - df['ema_diff4'].shift(18) #直前の値動きのMAと過去の差分











    # df['BBANDS_upperband'], df['BBANDS_middleband'], df['BBANDS_lowerband'] = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    # df['BBANDS_upperband'] -= hilo
    # df['BBANDS_middleband'] -= hilo
    # df['BBANDS_lowerband'] -= hilo

    # df['EMA'] = talib.EMA(close, timeperiod=30) - hilo

    # df['MACD_macd'], df['MACD_macdsignal'], df['MACD_macdhist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    # df['MOM10'] = talib.MOM(close, timeperiod=10)
    # df['MOM14'] = talib.MOM(close, timeperiod=14)
    # df['MOM50'] = talib.MOM(close, timeperiod=50)

    # df['ATR10'] = talib.ATR(high, low, close, timeperiod=10)
    # df['ATR14'] = talib.ATR(high, low, close, timeperiod=14)
    # df['ATR89'] = talib.ATR(high, low, close, timeperiod=89)
    # df['ATR149'] = talib.ATR(high, low, close, timeperiod=149)
    # df['ATR5'] = talib.ATR(high, low, close, timeperiod=5)


    return df
