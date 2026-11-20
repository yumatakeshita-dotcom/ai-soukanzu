-- Stripe課金のための追加(足すだけ)。pro_schema.sql を流したあとに1回だけ流す。
ALTER TABLE pro_keys ADD COLUMN stripe_customer TEXT;      -- Stripeの顧客ID(cus_...)。返金・解約のときに行を探すため
ALTER TABLE pro_keys ADD COLUMN stripe_subscription TEXT;  -- Stripeの定期購入ID(sub_...)
CREATE INDEX IF NOT EXISTS pro_keys_cus ON pro_keys(stripe_customer);
CREATE INDEX IF NOT EXISTS pro_keys_sub ON pro_keys(stripe_subscription);
