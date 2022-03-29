### BybitでAPIキーとシークレットキーを取得

APIについては以下を参照  
<!-- https://help.bybit.com/hc/ja/articles/360039749613-API%E7%AE%A1%E7%90%86 -->

### 以下の形式で本フォルダ直下に.envファイルを作成

```
API_KEY={Bybitで取得したAPIキー}
SECRET_KEY={Bybitで取得したシークレットキー}
LOT=0.01 //発注ロット
MAX_LOT=0.03 //最大ロット
INTERVAL=30(売買間隔)
```

### dockerビルド
```bash
docker build . -t paibot-binance
```

### dockerコンテナ起動
```bash
docker run -d -it --env-file=.env --name=paibot-binance paibot-binance
```

### 起動状況確認
```bash
docker container logs -t paibot-binance
```

### dockerコンテナの停止・削除
```bash
docker stop paibot-binance
docker container prune
```
