// プロ会員の設定。ここを書き換えるだけで、画面の動きが変わる(コードは触らない)。
window.PRO_CONFIG = {
  // false のあいだは、今までどおり誰でも「確かな版」「営業資料」を印刷・保存できる。
  // true にすると、印刷・保存・コピー(確かな版と営業資料)がプロ会員(アクセスキー)だけになる。
  // LP(/pro/)を公開して、決済(または先行案内)の準備ができてから true にする。
  gate: false,
  // Stripe の Payment Link(https://buy.stripe.com/...)。空のあいだは、LPに「先行案内に登録」のフォームが出る。
  checkoutUrl: '',
  // 表示する価格(円・月額)。決める前の仮の値
  priceMonthly: 980,
  priceBusinessMonthly: 9800
};
