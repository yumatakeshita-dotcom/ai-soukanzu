# Cloudflare をクラウドから動かす道具

PCがなくても、クラウドの定期タスクから D1(kigyo-asiapac・kigyo-relmap のデータ)に
**足すだけ** でデータを入れられるようにするための道具です。

## 守っていること
- `d1_add.py` は SELECT / PRAGMA / INSERT OR IGNORE しか送りません。DELETE・UPDATE・DROP・REPLACE は送る前に止めます
- 入れる前と後で行数を数え、減っていたら止めます(以前の同期で人物が消えたため)
- 鍵(トークン)はリポジトリに書きません。クラウド環境の設定に入れます

## Cloudflare の鍵の作り方(持ち主がやること・5分)
1. https://dash.cloudflare.com/profile/api-tokens を開き「トークンを作成する」
2. 「カスタムトークンを作成する」の「開始する」
3. 名前: `claude-cloud`
4. 権限(「さらに追加」で3行にする)
   - アカウント / **D1** / 編集
   - アカウント / **Workers スクリプト** / 編集
   - アカウント / **アカウント設定** / 読み取り
5. アカウントリソース: 自分のアカウントを選ぶ
6. 「概要に進む」→「トークンを作成する」。出てきた文字列をコピー(チャットには貼らない)
7. このプロジェクトの「プロジェクト設定」→「Cloud environment」→ 使っている環境(Default)の歯車 →
   **Network secrets**(古い画面では API credentials)に追加
   - ホスト: `api.cloudflare.com`
   - ヘッダー: `Authorization`
   - 値: `Bearer ` + コピーした文字列(Bearer のあとに半角スペース)
   - Network secrets が無い画面のときは、環境変数 `CLOUDFLARE_API_TOKEN` にコピーした文字列だけを入れる
8. 新しく始まるクラウドの作業から使えます

## 使い方
```
python3 tools/cloudflare/d1_add.py whoami                # つながるか確かめる
python3 tools/cloudflare/d1_add.py tables <DB名>         # 表と行数
python3 tools/cloudflare/d1_add.py add <DB名> <表名> data.csv --dry-run   # 試し
python3 tools/cloudflare/d1_add.py add <DB名> <表名> data.csv             # 本番(足すだけ)
```

## PCにある道具
`pc/` に、PCの relationship-map-src から移した道具を置きます(`docs/pc_tools_prompt.md` の文をPCの Claude Code に貼ると移ります)。
PCの道具の中の削除・置き換えをする部分は、クラウドの定期タスクでは使いません。
