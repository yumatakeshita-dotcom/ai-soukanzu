// プロ会員の制限(2026/11/20追加)。index.html に <script src="pro/config.js"> と <script src="pro/gate.js"> を足すだけで動く。
// 「確かな版」「営業資料」の印刷・保存・コピーのボタンを、gate が true のときだけアクセスキーで制限する。
// 既存のコードには触らない: ボタンのクリックを先に受けて(キャプチャ)、会員でなければそこで止める。
(function () {
  'use strict';
  var C = window.PRO_CONFIG || {};
  if (!C.gate) return; // いまは何もしない
  // 制限するボタン: 確かな版(印刷・コピー・保存)と、営業資料(印刷・保存。コピーも)
  var GUARDED = { kkprint: 1, kkcopy: 1, kksave: 1, bfprint: 1, bfsave: 1, bfcopy: 1 };
  var member = null, bypass = false;

  function getKey() { try { return localStorage.getItem('pro_key') || ''; } catch (e) { return ''; } }
  function setKey(k) { try { localStorage.setItem('pro_key', k); } catch (e) {} }

  function verify(key) {
    if (!key) return Promise.resolve(false);
    return fetch('/api/pro/verify', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ key: key }) })
      .then(function (r) { return r.json(); })
      .then(function (j) { return !!(j && j.ok); })
      .catch(function () { return false; }); // つながらないときは会員ではない扱い(ほかの機能は止めない)
  }
  function check() {
    if (member !== null) return Promise.resolve(member);
    return verify(getKey()).then(function (ok) { member = ok; return ok; });
  }
  // 開いた直後に確かめておく(クリックのときに待たせないため)
  if (getKey()) setTimeout(check, 1500);

  function css() {
    if (document.getElementById('pro-gate-css')) return;
    var st = document.createElement('style'); st.id = 'pro-gate-css';
    st.textContent =
      '#pro-gate{position:fixed;inset:0;z-index:200;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;padding:16px}' +
      '#pro-gate .pg{background:var(--surface,#fff);color:var(--fg,#161b22);border:1px solid var(--line,#d5dbe1);border-radius:12px;max-width:420px;width:100%;padding:18px 18px 16px;font-size:14px;line-height:1.7}' +
      '#pro-gate h2{font-size:17px;margin:0 0 6px}#pro-gate p{margin:6px 0}' +
      '#pro-gate input{font:inherit;width:100%;box-sizing:border-box;padding:8px 10px;border-radius:6px;border:1px solid var(--line,#d5dbe1);background:var(--bg,#f2f4f6);color:var(--fg,#161b22)}' +
      '#pro-gate .pg-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}' +
      '#pro-gate button,#pro-gate a.pg-b{font:inherit;font-size:13px;padding:7px 14px;border-radius:6px;border:1px solid var(--line,#d5dbe1);background:var(--surface,#fff);color:var(--fg,#161b22);cursor:pointer;text-decoration:none}' +
      '#pro-gate .pg-main{border-color:var(--active,#0d8a79);color:var(--active,#0d8a79);font-weight:700}' +
      '#pro-gate .pg-msg{font-size:12px;color:var(--conflict,#c93b3b);min-height:1.4em}';
    document.head.appendChild(st);
  }
  function close() { var d = document.getElementById('pro-gate'); if (d) d.remove(); }
  function ask(replay) {
    css(); close();
    var d = document.createElement('div'); d.id = 'pro-gate'; d.setAttribute('role', 'dialog'); d.setAttribute('aria-label', 'プロ会員限定');
    d.innerHTML =
      '<div class="pg"><h2>プロ会員の機能です</h2>' +
      '<p>公式・開示で確かめた資料の印刷・保存・コピーは、プロ会員だけが使えます。画面で読むのは、これまでどおり無料です。</p>' +
      '<input id="pg-key" type="password" autocomplete="off" placeholder="アクセスキー(会員の方)">' +
      '<div class="pg-msg" id="pg-msg"></div>' +
      '<div class="pg-row"><button type="button" class="pg-main" id="pg-ok">キーを確かめる</button>' +
      '<a class="pg-b" href="/pro/" target="_blank" rel="noopener">プランを見る</a>' +
      '<button type="button" id="pg-x">閉じる</button></div></div>';
    document.body.appendChild(d);
    d.addEventListener('click', function (e) { if (e.target === d) close(); });
    document.getElementById('pg-x').addEventListener('click', close);
    document.getElementById('pg-ok').addEventListener('click', function () {
      var k = (document.getElementById('pg-key').value || '').trim(), m = document.getElementById('pg-msg');
      m.textContent = '確かめています…';
      verify(k).then(function (ok) {
        if (!ok) { m.textContent = 'キーが確かめられませんでした。入力を見直してください'; return; }
        setKey(k); member = true; close(); replay();
      });
    });
  }

  document.addEventListener('click', function (ev) {
    if (bypass) return;
    var el = ev.target && ev.target.closest ? ev.target.closest('button,a') : null;
    if (!el || !GUARDED[el.id]) return;
    if (member === true) return; // 会員: そのまま通す
    ev.preventDefault(); ev.stopImmediatePropagation();
    var replay = function () { bypass = true; try { el.click(); } finally { bypass = false; } };
    check().then(function (ok) { if (ok) replay(); else ask(replay); });
  }, true);
})();
