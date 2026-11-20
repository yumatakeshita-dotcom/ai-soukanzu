-- プロ会員用の D1(データベース名: kigyo-pro)。公開Worker(kigyo-relmap)の束ね名 DB でつなぐ。
-- 作るのは1回だけ(持ち主の確認をとってから)。中身は「足すだけ」で運用する。
CREATE TABLE IF NOT EXISTS pro_waitlist (
  email      TEXT PRIMARY KEY,           -- 先行案内の申し込み(小文字にそろえて保存)
  plan       TEXT NOT NULL DEFAULT 'personal',   -- personal / business
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pro_keys (
  key_hash   TEXT PRIMARY KEY,           -- アクセスキーの SHA-256。キーそのものは保存しない
  plan       TEXT NOT NULL,              -- personal / business
  status     TEXT NOT NULL DEFAULT 'active',    -- active のものだけ有効
  expires_at TEXT,                       -- 空なら期限なし(ISO日時)
  note       TEXT,                       -- 会員の目印(会社名・Stripeの顧客IDなど。メールは書かない)
  created_at TEXT NOT NULL
);
