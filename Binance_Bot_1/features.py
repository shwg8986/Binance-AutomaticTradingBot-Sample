import talib

#テクニカル指標の計算を行う。機械学習を用いる場合はこれが特徴量となる。

def calc_features(df):
    open = df['op']
    high = df['hi']
    low = df['lo']
    close = df['cl']
    volume = df['volume']

    orig_columns = df.columns
    hilo = (df['hi'] + df['lo']) / 2

    
    
    
    
    #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    #                                 
    #
    #
    #                                               略
    #
    #   
    #
    #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
 





    return df
