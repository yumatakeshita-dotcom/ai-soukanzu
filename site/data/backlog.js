/* 確かめ係(過去の動画・番組の手がかり)の進み具合。scripts/media_backlog.py status が書く。手で直さない */
const BACKLOG_PROG=[{"d":"2026-11-21","todo":405,"done":7,"checked":322,"unverified":0},{"d":"2026-11-22","todo":353,"done":7,"checked":382,"unverified":0}];
function backlogBox(){
  const h=typeof BACKLOG_PROG!=='undefined'?BACKLOG_PROG:[];if(!h.length)return '';
  const e=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const L=h[h.length-1],P=h.length>1?h[h.length-2]:null,tot=L.todo+L.done+L.checked+L.unverified;
  const md=d=>d.slice(5).replace('-','/');
  const dt=P?`${md(P.d)}→${md(L.d)}で確かめ済みが ${(L.done+L.checked+L.unverified)-(P.done+P.checked+P.unverified)} 件増えた(入れた +${L.done-P.done}・入れなかった +${L.checked-P.checked}・確かめられず +${L.unverified-P.unverified})`:'';
  const rows=h.slice(-7).reverse().map(r=>{const t=r.todo+r.done+r.checked+r.unverified;return `<tr><td>${md(r.d)}</td><td style="text-align:right">${r.todo}</td><td style="width:45%"><div style="background:var(--line);border-radius:4px;height:8px"><div style="background:var(--accent,var(--active,#4a5dd0));width:${t?Math.round(100*(t-r.todo)/t):0}%;height:8px;border-radius:4px"></div></div></td><td style="text-align:right">${r.done}</td></tr>`}).join('');
  return `<div style="border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:var(--surface);overflow-wrap:anywhere"><b>確かめ係の進み具合</b>
  <p style="margin:6px 0;font-size:14px">過去の動画・番組の手がかり ${tot}件のうち、まだ確かめていないのは <b>${L.todo}件</b>(${e(md(L.d))} 時点)。毎日10:07に10件ほどずつ確かめています。</p>
  ${dt?`<p style="margin:0 0 8px;font-size:13px;color:var(--muted)">${e(dt)}</p>`:''}
  <div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:13px"><tr style="color:var(--muted)"><th style="text-align:left;font-weight:600">日付</th><th style="text-align:right;font-weight:600">残り</th><th style="font-weight:600">確かめ済みの割合</th><th style="text-align:right;font-weight:600">入れた累計</th></tr>${rows}</table></div>
  <p style="margin:8px 0 0;font-size:12px;color:var(--muted)">「入れなかった」は、確かめて相関図に足さなかったもの(動きではない・すでにある・外れ)です。記録は inbox/backlog/history.json。</p></div>`;
}
