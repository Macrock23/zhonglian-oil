# -*- coding: utf-8 -*-
import json
data=open('dashboard_data.json',encoding='utf-8').read()
def _r(p):
    return open(p,encoding='utf-8').read()
_LIBS=[('__LEAFLET_CSS__','libs/leaflet.min.css'),('__MCD_CSS__','libs/MarkerCluster.Default.min.css'),('__MC_CSS__','libs/MarkerCluster.min.css'),('__LEAFLET_JS__','libs/leaflet.min.js'),('__MC_JS__','libs/leaflet.markercluster.min.js')]
import os, urllib.request
_LIB_URLS={
 'libs/leaflet.min.css':'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css',
 'libs/leaflet.min.js':'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js',
 'libs/MarkerCluster.min.css':'https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.min.css',
 'libs/MarkerCluster.Default.min.css':'https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.Default.min.css',
 'libs/leaflet.markercluster.min.js':'https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/leaflet.markercluster.min.js',
}
def _ensure_libs():
    os.makedirs('libs', exist_ok=True)
    for _p,_u in _LIB_URLS.items():
        if not os.path.exists(_p):
            print('downloading', _p); urllib.request.urlretrieve(_u,_p)
_ensure_libs()

TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="color-scheme" content="light dark"/>
<title>中聯油脂問題油品 · 互動查詢儀表板</title>
<meta name="description" content="依食藥署「中聯油脂案專區」公開公告整理的互動查詢工具：查你買的商品是否列入下架清單、瀏覽 360 家下游業者地圖。第三方整理、非官方判定，一切以官方最新公告為準。"/>
<link rel="canonical" href="https://macrock23.github.io/zhonglian-oil/"/>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 rx=%2212%22 fill=%22%234F6BED%22/%3E%3Ccircle cx=%2227%22 cy=%2227%22 r=%2213%22 fill=%22none%22 stroke=%22white%22 stroke-width=%225%22/%3E%3Cline x1=%2237%22 y1=%2237%22 x2=%2250%22 y2=%2250%22 stroke=%22white%22 stroke-width=%226%22 stroke-linecap=%22round%22/%3E%3C/svg%3E"/>
<meta name="theme-color" content="#4F6BED"/>
<meta property="og:image" content="https://macrock23.github.io/zhonglian-oil/og.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:image" content="https://macrock23.github.io/zhonglian-oil/og.png"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="中聯油脂問題油品 · 互動查詢儀表板"/>
<meta property="og:title" content="中聯油脂問題油品 · 互動查詢儀表板"/>
<meta property="og:description" content="查你買的商品是否列入下架清單、瀏覽 360 家下游業者地圖。資料以食藥署官方公告為準；第三方整理、非官方判定。"/>
<meta property="og:url" content="https://macrock23.github.io/zhonglian-oil/"/>
<meta property="og:locale" content="zh_TW"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="中聯油脂問題油品 · 互動查詢儀表板"/>
<meta name="twitter:description" content="查你買的商品是否列入下架清單、瀏覽 360 家下游業者地圖。資料以食藥署官方公告為準；第三方整理、非官方判定。"/>
<style>__LEAFLET_CSS__</style>
<style>__MC_CSS__
__MCD_CSS__</style>
<style>
:root{color-scheme:light;
 --page:#EEF1F5;--surf:#FFFFFF;--surf2:#F4F6FA;--surf3:#E9EDF3;
 --bd:#E1E6EE;--ink:#1B2330;--ink2:#5A667B;--ink3:#8B96A8;
 --ts:#4F6BED;--ts-h:#3F5AD8;--on-pri:#FFFFFF;--sel:#EAEEFD;
 --fs:#3FA45B;--fm:#3E8BE0;--zl:#C79A2E;
 --danger:#C7362B;--warn-ink:#8A5A16;--warn-soft:#FBEFD9;--warn-bd:#EAD6AE;
 --ok-ink:#256B45;--ok-soft:#E7F4EC;--ok-bd:#C4E3CF;
 --hl:#FFE39B;--hl-ink:#4A3B00;--shadow:0 1px 2px rgba(20,30,50,.06),0 2px 8px rgba(20,30,50,.05);--bg:var(--surf2)}
[data-theme="dark"]{color-scheme:dark;
 --page:#0E141B;--surf:#161D27;--surf2:#1E2632;--surf3:#28313F;
 --bd:#2B3644;--ink:#E8EEF6;--ink2:#A5B0C0;--ink3:#6E7A8D;
 --ts:#6182F5;--ts-h:#7A96F7;--on-pri:#FFFFFF;--sel:#25314F;
 --fs:#54B570;--fm:#5B9EE8;--zl:#D8B04E;
 --danger:#F07067;--warn-ink:#E0A64A;--warn-soft:#332918;--warn-bd:#4A3D22;
 --ok-ink:#69C48F;--ok-soft:#16301F;--ok-bd:#284A34;
 --hl:#4A3F1A;--hl-ink:#F3E6B0;--shadow:0 2px 10px rgba(0,0,0,.5);--bg:var(--surf2)}
*{box-sizing:border-box}
html,body{margin:0;height:100%;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;color:var(--ink);background:var(--page)}
.tab,.chipbtn,.catbtn,.ctab,.btn,.item,.lrow,.resizer,.tbtn,input,select{transition:background .13s,color .13s,border-color .13s}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,.tab:focus-visible,.chipbtn:focus-visible,.catbtn:focus-visible,.ctab:focus-visible,.item:focus-visible,.lrow:focus-visible,summary:focus-visible{outline:2px solid var(--ts);outline-offset:2px}
header{height:60px;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 16px;background:var(--surf);border-bottom:1px solid var(--bd)}
.hbrand{display:flex;align-items:center;gap:10px;min-width:0}
header h1{margin:0;font-size:21px;font-weight:700;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
header .sub{font-size:12px;color:var(--ink2);white-space:nowrap}.hmark{flex:none;width:34px;height:34px;border-radius:9px;background:var(--ts);display:flex;align-items:center;justify-content:center}.hmark svg{width:20px;height:20px}.htxt{min-width:0}.hright{display:flex;align-items:center;gap:14px;flex:none}.freshness{display:flex;flex-direction:column;align-items:flex-end;gap:2px;line-height:1.25}.fresh-badge{font-size:12px;font-weight:600;color:var(--warn-ink);background:var(--warn-soft);border:1px solid var(--warn-bd);border-radius:999px;padding:2px 10px;white-space:nowrap}.fresh-note{font-size:11px;color:var(--ink2);text-decoration:none;white-space:nowrap}.fresh-note:hover{color:var(--ts);text-decoration:underline}
.tbtn{border:1px solid var(--bd);background:var(--surf2);color:var(--ink);border-radius:20px;padding:5px 13px;font-size:12px;cursor:pointer;flex:none}
.tbtn:hover{background:var(--surf3)}
.tabbar{display:flex;gap:2px;padding:0 14px;background:var(--surf);border-bottom:1px solid var(--bd);overflow-x:auto;scrollbar-width:thin}
.tab{padding:12px 16px;border:none;background:transparent;cursor:pointer;font-size:14px;color:var(--ink2);border-bottom:2px solid transparent;margin-bottom:-1px;font-family:inherit;flex:none;white-space:nowrap}
.tab:hover{color:var(--ink)}
.tab.active{font-weight:600;color:var(--ts);border-bottom-color:var(--ts)}.tshort{display:none}
.pages{height:calc(100vh - 60px - 46px - 36px)}
.page{display:flex;height:100%}
.side{width:300px;min-width:280px;background:var(--surf);border-right:1px solid var(--bd);overflow:auto;padding:16px}
.content{flex:1;min-width:0;overflow:auto}
#page-map .content,#map{height:100%}
#page-map .content{overflow:hidden}
.cpad{padding:16px 20px 40px}
.chead{font-size:18px;font-weight:600;margin:0 0 2px}
.csub{font-size:12px;color:var(--ink2);margin:0 0 12px}
input[type=text],select{width:100%;padding:8px 9px;border:1px solid var(--bd);border-radius:8px;font-size:13px;background:var(--surf);color:var(--ink)}
#cq{font-size:14px;padding:10px 12px}
.slab,.fg h3{font-size:12px;color:var(--ink3);font-weight:600;letter-spacing:.02em;margin:14px 0 7px}
.fg h3{margin:0 0 6px}
#cnote{font-size:11px;color:var(--ink2);margin-top:16px;line-height:1.6;border-top:1px solid var(--bd);padding-top:10px}
#cnote a,.crumb .x,.footer a,.footer .lk,.lk,.infopad a{color:var(--ts);text-decoration:none;cursor:pointer}
.chiprow{display:flex;flex-wrap:wrap;gap:6px}
.chipbtn{border:1px solid var(--bd);background:var(--surf);color:var(--ink);border-radius:20px;padding:4px 11px;font-size:12px;cursor:pointer}
.chipbtn:hover{background:var(--surf2)}
.chipbtn.on{background:var(--ts);color:var(--on-pri);border-color:var(--ts)}
#qbrands .chipbtn .cnt{color:var(--ink3);font-size:10px}
.cnt{color:var(--ink2);font-weight:400;font-size:11px}
.crumb{font-size:13px;color:var(--ink2);margin:0 0 14px;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.crumb b{color:var(--ink)}
.rsum{font-size:13px;color:var(--ink2);margin:0 2px 10px}
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.card{background:var(--surf);border:1px solid var(--bd);border-radius:12px;padding:13px 15px;border-left:4px solid var(--ts);display:flex;flex-direction:column;box-shadow:var(--shadow)}
.card.oil{border-left-color:var(--zl)}
.card.biz{border-left-color:var(--ink3)}
.card .cn{font-size:15px;font-weight:600;line-height:1.4}
.card .cm{font-size:12px;color:var(--ink2);margin-top:6px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.cstat{font-size:12px;color:var(--ink2);margin-top:5px}
.act,.dact,.cx{color:var(--danger)}
.act{font-size:12px;margin-top:6px}
.chip{font-size:11px;padding:1px 8px;border-radius:20px;background:var(--surf3);color:var(--ink2);border:1px solid var(--bd)}
.chip.cat{background:var(--warn-soft);color:var(--warn-ink);border-color:var(--warn-bd)}
.chip.src{background:var(--ok-soft);color:var(--ok-ink);border-color:var(--ok-bd)}
.chip.biz{background:var(--surf3);color:var(--ink2);border-color:var(--bd)}
mark{background:var(--hl);color:var(--hl-ink);padding:0 1px;border-radius:2px}
.ok{background:var(--ok-soft);border:1px solid var(--ok-bd);border-radius:12px;padding:18px;color:var(--ok-ink);font-size:14px}
.ok b{color:var(--ok-ink)}
.hint,.dhint{color:var(--ink2);font-size:14px;line-height:1.9;background:var(--surf2);border:1px dashed var(--bd);border-radius:12px;padding:22px}
.dhint{font-size:13px;line-height:1.8;padding:18px}
.fg{margin-bottom:13px}
.chk{display:flex;align-items:center;gap:6px;font-size:13px;padding:3px 0;cursor:pointer;color:var(--ink)}
.sw{width:11px;height:11px;border-radius:50%;display:inline-block;flex:none}
.scroll{max-height:150px;overflow:auto;border:1px solid var(--bd);border-radius:8px;padding:6px 8px}
.btn{width:100%;padding:7px;border:1px solid var(--bd);border-radius:8px;background:var(--surf2);color:var(--ink);cursor:pointer;font-size:13px}
.btn:hover{background:var(--surf3)}
.side .btn{margin-top:4px}
.statsbox{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.stat{background:var(--surf2);border:1px solid var(--bd);border-radius:8px;padding:4px 9px;font-size:12px;color:var(--ink2)}
.stat b{font-size:14px;font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums}
.item{padding:8px 10px;border-bottom:1px solid var(--bd);cursor:pointer;border-left:3px solid transparent}
.item:hover{background:var(--surf2)}
.item.sel{background:var(--sel);border-left-color:var(--ts)}
.item .nm{font-size:13px;font-weight:600}
.item .mt{font-size:11px;color:var(--ink2);margin-top:2px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.pill{font-size:10px;padding:1px 6px;border-radius:20px;color:#fff}
.badge{font-size:10px;padding:1px 6px;border-radius:6px;background:var(--surf3);color:var(--ink2)}
.badge.approx{background:var(--warn-soft);color:var(--warn-ink)}
.note{font-size:10px;color:var(--warn-ink);background:var(--warn-soft);border-radius:6px;padding:1px 5px}
.legendbar{font-size:12px;color:var(--ink2)}
table{border-collapse:collapse;width:100%;font-size:12px}
th,td{border-bottom:1px solid var(--bd);padding:6px 9px;text-align:left;vertical-align:top}
th{background:var(--surf);position:sticky;top:0;font-size:11px;color:var(--ink3)}
.leaflet-popup-content{font-size:12px;line-height:1.5}
[data-theme="dark"] .leaflet-popup-content-wrapper,[data-theme="dark"] .leaflet-popup-tip{background:var(--surf);color:var(--ink)}
[data-theme="dark"] .leaflet-popup-content a{color:var(--ts)}
.hidden{display:none!important}
.detail{width:332px;min-width:300px;border-left:1px solid var(--bd);background:var(--surf);overflow:hidden;padding:16px;display:flex;flex-direction:column}
#cdetail{flex:1;overflow:auto}
#mycart{flex:none;border-top:1px solid var(--bd);margin-top:12px;padding-top:10px;max-height:44%;overflow:auto}
.carthd{font-size:13px;font-weight:600;margin-bottom:6px;display:flex;gap:12px;align-items:center}
.carthint{font-size:12px;color:var(--ink2);line-height:1.6}
.cartrow{display:flex;justify-content:space-between;gap:8px;font-size:12px;padding:5px 0;border-bottom:1px dashed var(--bd)}
.cx{cursor:pointer;flex:none}
.lk{font-size:12px;font-weight:400}
.grp{margin-bottom:16px}
.grphd{font-size:13px;font-weight:600;color:var(--ts);border-bottom:1px solid var(--bd);padding-bottom:5px;margin-bottom:6px;display:flex;justify-content:space-between}
.grphd .cnt{color:var(--ink2);font-weight:400}
.lrow{display:flex;align-items:center;gap:8px;padding:8px 10px;border:1px solid transparent;border-radius:8px;cursor:pointer}
.lrow:hover{background:var(--surf2)}
.lrow.sel{background:var(--sel);border-color:var(--ts)}
.lrow .ln{font-size:14px;font-weight:600;line-height:1.4}
.lchk{flex:none;width:15px;height:15px;cursor:pointer}
.dhdr{font-size:13px;font-weight:600;color:var(--ink);border-bottom:1px solid var(--bd);padding-bottom:7px;margin-bottom:8px}
.dname{font-size:17px;font-weight:600;line-height:1.4;margin-bottom:12px}
.drow{display:flex;gap:10px;font-size:13px;padding:6px 0;border-bottom:1px dashed var(--bd)}
.dk{color:var(--ink2);min-width:92px}
.dv{flex:1;word-break:break-all}
.dact{font-size:13px;margin-top:12px;line-height:1.6}
#disc-modal{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px}
.disc-box{background:var(--surf);color:var(--ink);max-width:580px;max-height:88vh;overflow:auto;border-radius:14px;padding:22px 24px;border:1px solid var(--bd)}
.disc-box h2{margin:0 0 6px;font-size:18px;color:var(--danger)}
.disc-sub{font-size:12px;color:var(--ink2);margin:0 0 12px}
.disc-body{font-size:13px;line-height:1.75;color:var(--ink);margin:0;padding-left:18px}
.disc-body li{margin-bottom:8px}
.disc-ok{margin-top:16px;width:100%;padding:12px;border:none;border-radius:10px;background:var(--ts);color:var(--on-pri);font-size:15px;font-weight:600;cursor:pointer}
.disc-ok:hover{background:var(--ts-h)}
.footer{height:36px;display:flex;flex-wrap:wrap;gap:4px 14px;align-items:center;padding:0 16px;background:var(--surf);border-top:1px solid var(--bd);font-size:12px;color:var(--ink2);overflow:hidden}
#ctabs{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px;position:sticky;top:0;background:var(--surf);padding:4px 0;z-index:3}
.ctab{padding:6px 13px;border:1px solid var(--bd);border-radius:20px;background:var(--surf);color:var(--ink);font-size:13px;cursor:pointer;white-space:nowrap}
.ctab:hover{background:var(--surf2)}
.ctab.on{background:var(--ts);color:var(--on-pri);border-color:var(--ts)}
.ctab .cnt{opacity:.75;font-size:11px;margin-left:2px}
.catbtn{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:left;border:1px solid var(--bd);background:var(--surf);color:var(--ink);border-radius:8px;padding:8px 11px;font-size:13px;cursor:pointer;margin-bottom:5px}
.catbtn:hover{background:var(--surf2)}
.catbtn.on{background:var(--ts);color:var(--on-pri);border-color:var(--ts)}
.catbtn .cnt{opacity:.7;font-size:11px}
.resizer{flex:0 0 6px;cursor:col-resize;background:var(--bd);opacity:.6;transition:opacity .15s,background .15s}
.resizer:hover,.resizer.drag{opacity:1;background:var(--ts)}
#page-info .content{overflow:auto}
.infopad{max-width:760px;margin:0 auto;padding:22px 24px 48px;line-height:1.85;font-size:14px}
.infopad h2{font-size:20px;margin:0 0 4px}
.infopad h3{font-size:16px;margin:22px 0 6px;color:var(--ts)}
.infopad .src{font-size:12px;color:var(--ink2)}
.infopad ul{padding-left:20px;margin:6px 0}
.infopad li{margin-bottom:6px}
.infobox{background:var(--surf2);border:1px solid var(--bd);border-radius:10px;padding:12px 14px;margin:12px 0;font-size:13px;line-height:1.7}
@media(max-width:900px){.pages{height:auto}.page{flex-direction:column;height:auto}.side{width:100%;border-right:none;border-bottom:1px solid var(--bd)}#page-map .content{height:66vh}.content{overflow:visible}.detail{width:100%;border-left:none;border-top:1px solid var(--bd)}.resizer{display:none}.footer{height:auto;padding:6px 16px}}@media(max-width:560px){header{height:auto;flex-wrap:wrap;gap:6px 10px;padding:8px 12px}header h1{font-size:17px}header .sub{display:none}.hmark{width:28px;height:28px}.hright{gap:8px}.freshness{flex-direction:row;align-items:center;gap:8px}.fresh-note{display:none}.tab{padding:10px 10px;font-size:13px}.tfull{display:none}.tshort{display:inline}.tbtn{padding:9px 13px}.hbtns{gap:6px}}@media print{:root{--page:#fff;--surf:#fff;--surf2:#fff;--surf3:#fff;--ink:#000;--ink2:#222;--ink3:#555;--bd:#bbb}*{-webkit-print-color-adjust:exact !important;print-color-adjust:exact !important}#themeBtn,.resizer,.tbtn,#disc-modal{display:none !important}.pages,.page,.content,.detail,.side{height:auto !important;max-height:none !important;overflow:visible !important}#page-map{display:none !important}.footer{position:static}}.hbtns{display:flex;gap:8px;flex:none}#page-term th{cursor:pointer;user-select:none}#page-term th:hover{color:var(--ts)}[data-fontscale="lg"] .item,[data-fontscale="lg"] .lrow,[data-fontscale="lg"] #tbody td,[data-fontscale="lg"] .infopad,[data-fontscale="lg"] .infopad li,[data-fontscale="lg"] .infobox,[data-fontscale="lg"] .disc-body li,[data-fontscale="lg"] .csub,[data-fontscale="lg"] #cnote,[data-fontscale="lg"] .footer,[data-fontscale="lg"] header .sub,[data-fontscale="lg"] .chipbtn,[data-fontscale="lg"] .catbtn,[data-fontscale="lg"] .nm,[data-fontscale="lg"] .mt{font-size:15px !important;line-height:1.7 !important}#histbox{margin-top:6px}.histrow{display:flex;align-items:center;gap:6px;padding:5px 6px;border-radius:6px;cursor:pointer;font-size:12px}.histrow:hover{background:var(--surf2)}.htag{flex:none;font-size:10px;color:var(--ts);border:1px solid var(--bd);border-radius:4px;padding:1px 5px}.hl{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.hts{flex:none;color:var(--ink3);font-size:11px}[data-fontscale="lg"] .histrow{font-size:14px}#page-term table{table-layout:fixed;width:100%;max-width:920px;min-width:800px}#page-term td,#page-term th{padding:6px 9px}#page-term th:nth-child(1){width:64px}#page-term th:nth-child(2){width:84px}#page-term th:nth-child(3){width:300px}#page-term th:nth-child(4){width:300px}#page-term th:nth-child(5){width:150px}#page-term td:nth-child(1){text-align:center;white-space:nowrap}#page-term td:nth-child(2){white-space:nowrap}#page-term td,#page-term th{overflow-wrap:anywhere;word-break:break-word;vertical-align:top}#page-term .exp summary{cursor:pointer;color:var(--ts);list-style:none}#page-term .exp summary::-webkit-details-marker{display:none}#page-term .exp summary::before{content:"▸ "}#page-term .exp[open] summary::before{content:"▾ "}#page-term .expfull{margin-top:4px;font-size:12px;color:var(--ink2);line-height:1.7}
</style>
<script>(function(){var t;try{t=localStorage.getItem('zl_theme');}catch(e){}if(!t)t=(window.matchMedia&&matchMedia('(prefers-color-scheme:dark)').matches)?'dark':'light';document.documentElement.setAttribute('data-theme',t);})();</script>
</head>
<body>
<div id="disc-modal" style="display:flex">
  <div class="disc-box">
    <h2>使用前請詳閱 · 免責聲明</h2>
    <p class="disc-sub">本工具為第三方整理，非官方網站、非官方判定。</p>
    <ul class="disc-body">
      <li>資料整理自衛福部食品藥物管理署「中聯油脂案專區」<b>公開公告</b>，為 <b>115/7/8 之快照</b>；官方名單持續更新與更正。</li>
      <li>一切<b>以食藥署最新公告，及商品外包裝實際批號/有效日期為準</b>；本工具可能有誤或已過時。</li>
      <li>商家或品牌被列入官方名單，<b>僅代表其位於問題油品「流向鏈」，不代表該商家知情，亦不代表其現售商品有害</b>。</li>
      <li>本工具於消費者查詢頁<b>已排除</b>官方註記「應刪除／重複／非供食用（飼料‧工業用）」之項目；完整名單及官方註記請見「業者地圖」。</li>
      <li>如發現錯誤或需更正，請以官方公告為準並洽原業者；食安專線 <b>1919</b>。</li>
      <li>本工具不構成法律、醫療或投資建議。點選下方按鈕即表示您已瞭解並同意上述聲明。</li>
    </ul>
    <button class="disc-ok" onclick="document.getElementById('disc-modal').style.display='none'">我已瞭解並同意</button>
  </div>
</div>
<header><div class="hbrand"><span class="hmark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><circle cx="10" cy="10" r="6" stroke="#fff" stroke-width="2.2"/><line x1="14.6" y1="14.6" x2="20" y2="20" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg></span><div class="htxt"><h1>中聯油脂問題油品 · 互動查詢儀表板</h1><span class="sub">依食藥署官方公告整理 · 第三方非官方判定</span></div></div><div class="hright"><div class="freshness"><span class="fresh-badge">資料快照 115/7/8</span><a class="fresh-note" href="https://www.fda.gov.tw/tc/site.aspx?sid=13702" target="_blank" rel="noopener">官方每日更新 · 以食藥署為準 ↗</a></div><div class="hbtns"><button id="fontBtn" class="tbtn" type="button" onclick="toggleFont()" aria-pressed="false" aria-label="放大字級">字級 標準</button><button id="themeBtn" class="tbtn" type="button" onclick="toggleTheme()" aria-label="切換明暗模式">☾ 暗色</button></div></div></header>
<nav aria-label="主要功能分頁"><div class="tabbar" role="tablist" aria-label="主要功能分頁">
  <button class="tab active" id="tab-check" type="button" role="tab" aria-selected="true" aria-controls="page-check" tabindex="0" data-tab="check" onclick="switchTab('check')"><span class="tfull">我買的商品中了嗎？</span><span class="tshort">查商品</span></button>
  <button class="tab" id="tab-map" type="button" role="tab" aria-selected="false" aria-controls="page-map" tabindex="-1" data-tab="map" onclick="switchTab('map')"><span class="tfull">業者地圖</span><span class="tshort">地圖</span></button>
  <button class="tab" id="tab-term" type="button" role="tab" aria-selected="false" aria-controls="page-term" tabindex="-1" data-tab="term" onclick="switchTab('term')"><span class="tfull">終端下架完整清單</span><span class="tshort">完整清單</span></button>
  <button class="tab" id="tab-info" type="button" role="tab" aria-selected="false" aria-controls="page-info" tabindex="-1" data-tab="info" onclick="switchTab('info')"><span class="tfull">官方資訊／健康須知</span><span class="tshort">官方資訊</span></button>
</div></nav>
<main class="pages">

  <section id="page-check" class="page" role="tabpanel" aria-labelledby="tab-check" tabindex="-1">
    <div class="side">
      <div class="slab" style="margin-top:0">搜尋商品</div>
      <input id="cq" type="text" aria-label="搜尋商品名稱" placeholder="輸入商品名稱，如：鮪魚、金酥…"/>
      <div class="slab">知名品牌／通路（點一下查詢）</div>
      <div id="qbrands" class="chiprow"></div>
      <div class="slab">依類別瀏覽（點選在中間顯示）</div>
      <div id="cattree"></div>
      <div id="histbox"></div>
      <div id="cnote">品名比對僅供快速參考，非官方判定。請核對外包裝<b>批號與有效日期</b>，並以<a href="https://www.fda.gov.tw/tc/site.aspx?sid=13702" target="_blank">食藥署專區</a>最新公告為準。</div>
    </div>
    <div class="resizer" data-target="side"></div>
    <div class="content"><div class="cpad">
      <h2 class="chead">我買的商品，在下架名單裡嗎？</h2>
      <p class="csub">左側搜尋／品牌／類別 → 中間依品項分類列出商品 → 點商品看右側詳情。涵蓋 401 項終端商品＋受影響油品。</p>
      <div id="crumb"></div>
      <div id="dimtoggle" class="seg" style="margin:0 0 10px;display:none"><button data-d="cat" class="on" onclick="setDim('cat')">依品項類別</button><button data-d="src" onclick="setDim('src')">依來源業者</button></div>
      <div id="ctabs"></div>
      <div id="clist"></div>
    </div></div>
    <div class="resizer" data-target="detail"></div>
    <aside class="detail"><div class="dhdr">商品詳情</div><div id="cdetail"></div><div id="mycart"></div></aside>
  </section>

  <section id="page-map" class="page hidden" role="tabpanel" aria-labelledby="tab-map" tabindex="-1">
    <div class="side">
      <div id="stats" class="statsbox"></div>
      <div id="panel">
        <div class="fg"><h3>搜尋業者／地址</h3><input id="q" type="text" aria-label="搜尋業者名稱或地址" placeholder="業者名稱或地址"/></div>
        <div class="fg"><h3>來源製造商</h3><div id="fmaker"></div></div>
        <div class="fg"><h3>定位狀態</h3>
          <label class="chk"><input type="checkbox" class="fstatus" value="located" checked/> 已精確定位</label>
          <label class="chk"><input type="checkbox" class="fstatus" value="approx" checked/> 縣市概略位置</label>
          <label class="chk"><input type="checkbox" class="fnote" value="note"/> 只看有官方備註者</label>
        </div>
        <div class="fg"><h3>縣市（可複選）</h3><div id="fcounty" class="chiprow" style="max-height:160px;overflow:auto"></div></div>
        <button class="btn" onclick="resetF()">重置篩選</button>
      </div>
    </div>
    <div class="resizer" data-target="side"></div>
    <div class="content"><div id="map"></div></div>
    <div class="resizer" data-target="detail"></div>
    <aside class="detail">
      <div class="dhdr">品項篩選</div>
      <select id="fprod" aria-label="品項篩選" style="margin-bottom:14px"><option value="">全部品項</option></select>
      <div class="dhdr">符合業者</div>
      <div id="listcount" class="legendbar" style="margin:0 0 8px"></div>
      <div id="list" style="flex:1;overflow:auto"></div>
    </aside>
  </section>

  <section id="page-term" class="page hidden" role="tabpanel" aria-labelledby="tab-term" tabindex="-1">
    <div class="side">
      <div class="slab" style="margin-top:0">篩選終端商品</div>
      <div class="fg"><input id="tq" type="text" aria-label="搜尋業者或產品名稱" placeholder="搜尋業者 / 產品名"/></div>
      <div class="fg"><select id="tcounty" aria-label="縣市篩選"><option value="">全部縣市</option></select></div>
      <div id="tcount" class="legendbar"></div>
    </div>
    <div class="resizer" data-target="side"></div>
    <div class="content"><div style="height:100%;overflow:auto"><table><thead><tr><th onclick="sortTable(this)" title="來源製造商在官方名單中的序號">來源序號</th><th onclick="sortTable(this)">縣市</th><th onclick="sortTable(this)">業者</th><th onclick="sortTable(this)">終端產品名稱</th><th onclick="sortTable(this)">有效日期/狀態</th></tr></thead><tbody id="tbody"></tbody></table></div></div>
  </section>

  <section id="page-info" class="page hidden" role="tabpanel" aria-labelledby="tab-info" tabindex="-1"><div class="content"><div class="infopad">
    <h2>官方資訊／健康須知</h2>
    <p class="src">整理自衛福部食品藥物管理署公告與記者會（快照 115/7/8）。本頁為資訊整理，非官方網站、非醫療建議；一切以官方最新公告為準。</p>
    <div class="infobox"><b>買到問題商品怎麼辦？</b><br>① 核對外包裝<b>批號與有效日期</b> → ② 若在官方名單內，<b>停止食用</b>、向<b>原購買通路退貨</b> → ③ 有疑問撥食安專線 <b>1919</b> 或洽當地衛生局；退貨遭拒可向消保官反映。</div>
    <h3>事件概要</h3>
    <ul>
      <li>中聯油脂供應之部分大豆沙拉油，檢出一級致癌物<b>苯（a）駢芘（BaP）</b>不符規定；自檢 8.1 μg/kg，為限量標準 2.0 μg/kg 的<b>逾 4 倍</b>。</li>
      <li>約 <b>1,300 公噸</b>流向泰山、福壽、福懋，製成受影響產品，流入 <b>360 家</b>下游業者；預防性下架終端商品自 7/7 的 232 項增至 <b>7/8 共 401 項</b>。</li>
      <li>中聯 6/11 得知檢驗超標卻未即時通報；6/15 品保會議三家股東（泰山、福壽、福懋）均已得知仍延遲，看似於 6/30 才自主通報。食藥署認定涉<b>隱匿事實、延遲通報、虛報產量</b>。</li>
    </ul>
    <h3>官方處置</h3>
    <ul>
      <li>要求相關產品<b>下架回收與預防性下架</b>（本工具清單即為預防性下架名單）。</li>
      <li>依食品安全衛生管理法<b>合計裁罰 1 億 6,520 萬元</b>（違反§15 食品衛生標準 1.152 億＋違反§7 通報義務 5,000 萬），創國內食安案件最高。</li>
      <li>要求 4 大國產食用油脂精煉廠（大統益、中聯、台糖、長輝）對黃豆原料<b>逐船或逐批檢驗 BaP</b>。</li>
    </ul>
    <h3>苯駢芘（BaP）是什麼？</h3>
    <ul>
      <li>屬多環芳香烴，世界衛生組織 IARC 列為<b>第一級致癌物</b>（確認對人類致癌）。</li>
      <li>常見於高溫加工、油脂精煉不當或環境污染；長期、過量暴露才是主要風險考量。</li>
    </ul>
    <h3>健康須知（引述專家）</h3>
    <ul>
      <li>台北醫學大學李青澔教授於食藥署記者會提醒：<b>勿過度恐慌</b>，並<b>不要購買來源不明、宣稱有「排毒」功效的產品</b>，以免帶來無法掌控的健康風險。</li>
      <li>一般民眾維持<b>均衡飲食、多蔬果、多喝水</b>即可；如食用後身體不適，請就醫並說明情形。</li>
    </ul>
    <p class="src">※ 本頁為資訊整理，<b>非醫療建議</b>；個別健康狀況請諮詢醫療專業人員。</p>
    <p class="src">主要資料來源：食藥署新聞「五項強化措施‧公布更新360家業者及產品資訊」（2026-07-06，本署新聞 t634424）、食藥署「中聯油脂案專區」、中央社（2026-07-06）。以官方最新公告為準。</p>
    <h3>官方連結與管道</h3>
    <ul>
      <li>食藥署「中聯油脂案專區」（以官方最新公告為準）：<a href="https://www.fda.gov.tw/tc/site.aspx?sid=13702" target="_blank">開啟官方專區</a></li>
      <li>食安服務專線 <b>1919</b>；退換貨遭拒可向所在地消保官反映。</li>
    </ul>
  </div></div></section>

</main>

<footer class="footer">
  <span>⚠ 非官方整理，僅供參考</span>
  <span>資料時間：115/7/8 快照</span>
  <a href="https://www.fda.gov.tw/tc/site.aspx?sid=13702" target="_blank">食藥署官方專區（以此為準）</a>
  <span>更正／申訴請洽原業者或食安專線 1919</span>
  <span class="lk" onclick="document.getElementById('disc-modal').style.display='flex'">重看免責聲明</span>
</footer>
<script>__LEAFLET_JS__</script>
<script>__MC_JS__</script>
<script>window.DATA = __DATA__;</script>
<script>
function switchTab(t){
  ['check','map','term','info'].forEach(function(x){document.getElementById('page-'+x).classList.toggle('hidden',x!==t);});
  document.querySelectorAll('.tab').forEach(function(e){var on=e.dataset.tab===t;e.classList.toggle('active',on);e.setAttribute('aria-selected',on?'true':'false');e.setAttribute('tabindex',on?'0':'-1');});
  if(t==='map'){setTimeout(function(){map.invalidateSize();},60);}
  else if(t==='term'){renderT();}
  else if(t==='check'){renderCheck();}
}
var C={'泰山':'#D85A30','福壽':'#639922','福懋':'#378ADD','中聯油脂(源頭)':'#BA7517','其他':'#888'};
var B=DATA.businesses;
function esc(s){return (s==null?'':(''+s)).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
var map=L.map('map',{preferCanvas:true}).setView([23.7,120.9],7);
var lightTiles=L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap'});
var darkTiles=L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{maxZoom:19,subdomains:'abcd',attribution:'&copy; OpenStreetMap, &copy; CARTO'});
var curTiles=null;
function setTiles(t){var w=(t==='dark')?darkTiles:lightTiles;if(curTiles===w)return;if(curTiles)map.removeLayer(curTiles);w.addTo(map);curTiles=w;}
function applyTheme(t){document.documentElement.setAttribute('data-theme',t);try{localStorage.setItem('zl_theme',t);}catch(e){}var b=document.getElementById('themeBtn');if(b)b.textContent=(t==='dark'?'\u2600 亮色':'\u263e 暗色');setTiles(t);setTimeout(function(){map.invalidateSize();},60);}
function toggleTheme(){applyTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark');}
setTiles(document.documentElement.getAttribute('data-theme')||'light');
(function(){var b=document.getElementById('themeBtn');if(b)b.textContent=(document.documentElement.getAttribute('data-theme')==='dark'?'\u2600 亮色':'\u263e 暗色');})();
var cluster=L.markerClusterGroup({maxClusterRadius:45,spiderfyOnMaxZoom:true});map.addLayer(cluster);
var markers={};
function popupHtml(b){
  var rows=b.products.map(function(p,i){return esc(p)+' <span style="color:var(--ink3)">'+esc(b.batches[i]||'')+' '+esc(b.expiries[i]||'')+'</span>';}).join('<br>');
  var mk=b.makers.map(function(m){return '<span class="pill" style="background:'+(C[m]||'#888')+'">'+esc(m)+'</span>';}).join(' ');
  return '<b>'+esc(b.name)+'</b>　<span style="color:var(--ink3)">#'+b.seq+'</span><br><div style="margin:3px 0">'+esc(b.county)+(b.located?'':' · <span style="color:var(--warn-ink)">縣市概略位置</span>')+'</div>'+(b.addr?'<div style="color:var(--ink2)">'+esc(b.addr)+'</div>':'')+'<div style="margin:4px 0">'+mk+'</div><div>'+rows+'</div>'+(b.note?'<div class="note" style="margin-top:4px">官方備註：'+esc(b.note)+'</div>':'');
}
B.forEach(function(b){var m=L.circleMarker([b.lat,b.lng],{radius:6,color:'#fff',weight:1,fillColor:C[b.maker]||'#888',fillOpacity:b.located?0.95:0.5,dashArray:b.located?null:'2,2'});m.bindPopup(function(){return popupHtml(b);},{maxWidth:280});m._b=b;markers[b.seq]=m;});
var makers=['泰山','福壽','福懋','中聯油脂(源頭)'];
document.getElementById('fmaker').innerHTML=makers.map(function(m){return '<label class="chk"><input type="checkbox" class="fmk" value="'+m+'" checked/><span class="sw" style="background:'+C[m]+'"></span>'+m+'</label>';}).join('');
var counties=Array.from(new Set(B.map(function(b){return b.county;}).filter(Boolean))).sort();
var countySel=new Set();
function renderCounties(){var el=document.getElementById('fcounty');el.innerHTML='<button class="chipbtn'+(countySel.size===0?' on':'')+'" data-county="__all__" onclick="toggleCounty(\''+'__all__'+'\')">全部</button>'+counties.map(function(c){return '<button class="chipbtn'+(countySel.has(c)?' on':'')+'" data-county="'+esc(c)+'" onclick="toggleCounty(this.getAttribute(\'data-county\'))">'+esc(c)+'</button>';}).join('');}
function toggleCounty(c){if(c==='__all__'){countySel.clear();}else{if(countySel.has(c))countySel.delete(c);else countySel.add(c);}renderCounties();render();}
renderCounties();
var psel=document.getElementById('fprod');DATA.products.forEach(function(p){var o=document.createElement('option');o.value=p;o.textContent=p;psel.appendChild(o);});
function getChecked(cls){return Array.from(document.querySelectorAll('.'+cls+':checked')).map(function(e){return e.value;});}
function filtered(){
  var q=document.getElementById('q').value.trim().toLowerCase();var mks=getChecked('fmk'),sts=getChecked('fstatus');
  var onlyNote=document.querySelector('.fnote').checked;var prod=document.getElementById('fprod').value;
  return B.filter(function(b){
    if(q && (b.name.toLowerCase().indexOf(q)<0 && (b.addr||'').toLowerCase().indexOf(q)<0)) return false;
    if(mks.indexOf(b.maker)<0) return false;
    if(sts.indexOf(b.located?'located':'approx')<0) return false;
    if(countySel.size>0 && !countySel.has(b.county)) return false;
    if(onlyNote && !b.note) return false;
    if(prod && b.products.indexOf(prod)<0) return false;
    return true;});
}
function render(){
  var fb=filtered();cluster.clearLayers();cluster.addLayers(fb.map(function(b){return markers[b.seq];}));
  document.getElementById('listcount').innerHTML='符合 <b style="color:var(--ink)">'+fb.length+'</b> / '+B.length+' 家（'+fb.filter(function(b){return !b.located;}).length+' 家概略）';
  document.getElementById('list').innerHTML=fb.map(function(b){return '<div class="item" data-seq="'+b.seq+'" onclick="focusB('+b.seq+')"><div class="nm">'+esc(b.name)+' <span style="color:var(--ink3);font-weight:400">#'+b.seq+'</span></div><div class="mt"><span class="pill" style="background:'+(C[b.maker]||'#888')+'">'+esc(b.maker)+'</span>'+esc(b.county)+(b.located?'':' <span class="badge approx">概略</span>')+(b.note?' <span class="note">備註</span>':'')+'</div><div class="mt">'+esc(b.products.join('、'))+'</div></div>';}).join('')||'<div style="padding:16px;color:var(--ink3)">無符合結果</div>';
  document.getElementById('stats').innerHTML='<div class="stat"><b>'+fb.length+'</b> 家</div><div class="stat">泰山 <b>'+fb.filter(function(b){return b.maker=="泰山";}).length+'</b></div><div class="stat">福壽 <b>'+fb.filter(function(b){return b.maker=="福壽";}).length+'</b></div><div class="stat">福懋 <b>'+fb.filter(function(b){return b.maker=="福懋";}).length+'</b></div><div class="stat">中聯 <b>'+fb.filter(function(b){return b.maker.indexOf("中聯")==0;}).length+'</b></div><div class="stat">精確 <b>'+fb.filter(function(b){return b.located;}).length+'</b>·概略 <b>'+fb.filter(function(b){return !b.located;}).length+'</b></div>';
}
function focusB(seq){document.querySelectorAll('#list .item').forEach(function(el){el.classList.toggle('sel',(+el.getAttribute('data-seq'))===seq);});var m=markers[seq];var b=m._b;map.setView([b.lat,b.lng],b.located?16:12);cluster.zoomToShowLayer(m,function(){m.openPopup();});}
function resetF(){document.getElementById('q').value='';document.querySelectorAll('.fmk,.fstatus').forEach(function(e){e.checked=true;});document.querySelector('.fnote').checked=false;countySel.clear();renderCounties();document.getElementById('fprod').value='';render();}
document.getElementById('panel').addEventListener('input',render);document.getElementById('panel').addEventListener('change',render);document.getElementById('fprod').addEventListener('change',render);render();
window.addEventListener('load',function(){setTimeout(function(){map.invalidateSize();},300);});

var T=DATA.terminal;
var tcs=Array.from(new Set(T.map(function(t){return t.county;}).filter(Boolean))).sort();
var tsel=document.getElementById('tcounty');tcs.forEach(function(c){var o=document.createElement('option');o.value=c;o.textContent=c;tsel.appendChild(o);});
function expiryCell(e){e=(e==null?'':(''+e)).trim();var parts=e.split(/[、\s]+/).map(function(s){return s.trim();}).filter(Boolean);var dl=parts.filter(function(p){return /^\d{3,4}[.\/][\d.\/~-]*$/.test(p);});if(parts.length>=2&&dl.length===parts.length){return '<details class="exp"><summary>'+esc(parts[0])+' 等 '+parts.length+' 個日期</summary><div class="expfull">'+esc(parts.join('、'))+'</div></details>';}return esc(e);}
function renderT(){
  var q=document.getElementById('tq').value.trim().toLowerCase();var c=document.getElementById('tcounty').value;
  var ft=T.filter(function(t){if(c && t.county!=c) return false;if(q && (t.vendor.toLowerCase().indexOf(q)<0 && (t.name||'').toLowerCase().indexOf(q)<0)) return false;return true;});
  document.getElementById('tcount').innerHTML='符合 <b>'+ft.length+'</b> / '+T.length+' 項<br>'+esc(DATA.terminalUpdated);
  document.getElementById('tbody').innerHTML=ft.map(function(t){return '<tr><td>'+t.seq+'</td><td>'+esc(t.county)+'</td><td>'+esc(t.vendor)+'</td><td>'+esc(t.name)+'</td><td>'+expiryCell(t.expiry)+'</td></tr>';}).join('');
}
document.getElementById('tq').addEventListener('input',renderT);document.getElementById('tcounty').addEventListener('change',renderT);

function classify(n){
  if(/(沙拉油|調合油|調和油|耐炸油|黃豆油|蔬菜油|香油|大豆油|原油|烹調油|花生油|果實精華調)/.test(n)) return '油品';
  if(/飯糰/.test(n)) return '飯糰';
  if(/(麵包|吐司|貝果|可頌|餐包|蛋糕|泡芙|甜甜圈|丹麥|布丁|銅鑼)/.test(n)) return '烘焙/麵包';
  if(/(便當|餐盒|飯盒|燴飯|炒飯|焗飯|咖哩飯|雞腿飯|排骨飯)/.test(n)) return '便當/餐盒';
  if(/(拉麵|烏龍|義大利麵|米粉|冬粉|粄條|炒麵|湯麵|涼麵|米線)/.test(n)) return '麵食';
  if(/(醬|美乃滋|沙茶|蛋黃|抹醬)/.test(n)) return '醬料/抹醬';
  if(/(丸|餃|包子|燒賣|火鍋|關東煮|香腸|肉鬆|滷|雞塊|酥|排|餅|捲|串|漢堡|三明治|春捲|水餃)/.test(n)) return '調理/加工食品';
  return '其他';
}
var IDX=[];
(function(){var byName={};
  DATA.upstream.forEach(function(o){if(!byName[o.name]) byName[o.name]={name:o.name,source:o.maker+'（品牌）',county:'',batches:[],cat:'油品',kind:'oil'};byName[o.name].batches.push(o.batch);});
  Object.keys(byName).forEach(function(k){var o=byName[k];o.status='批號 '+o.batches.join('、');IDX.push(o);});
  DATA.terminal.forEach(function(t){IDX.push({name:t.name,source:t.vendor,county:t.county,status:t.expiry||'',cat:classify(t.name),kind:'term'});});
})();
function norm(s){return (s||'').normalize('NFKC').replace(/台/g,'臺').toLowerCase();}
function hl(name,kws){var h=esc(name);kws.forEach(function(k){if(!k)return;var re=new RegExp('('+k.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi');h=h.replace(re,'<mark>$1</mark>');});return h;}
function actText(it){if(it.kind=='biz') return '此店家列入官方問題油品流向名單；不代表其現售商品有害或商家知情。建議留意官方更新，如有疑慮可洽該店家或撥食安專線 1919。';if(it.kind=='oil') return '若買到此油品，請停止使用並向原購買通路退貨。';if(/已逾|過期/.test(it.status)) return '此品項多已過有效日期；如仍留存請勿食用。';return '建議停止食用，並向原購買通路辦理退貨。';}
function card(it,kws){var meta;if(it.kind=='biz'){var mk=(it.makers||[]).map(function(m){return '<span class="chip src">'+esc(m)+'</span>';}).join('');meta='<span class="chip biz">受影響店家/通路</span>'+(it.county?'<span class="chip">'+esc(it.county)+'</span>':'')+mk;}else{meta='<span class="chip cat">'+esc(it.cat)+'</span><span class="chip src">'+esc(it.source)+'</span>'+(it.county?'<span class="chip">'+esc(it.county)+'</span>':'');}return '<div class="card'+(it.kind=='oil'?' oil':(it.kind=='biz'?' biz':''))+'"><div class="cn">'+hl(it.name,kws)+'</div><div class="cm">'+meta+'</div>'+(it.status?'<div class="cstat">'+esc(it.status)+'</div>':'')+'<div class="act">'+esc(actText(it))+'</div></div>';}
var activeCat='',activeItem='';
var CRES=[],CKWS=[],selIdx=-1,GROUPS={},GORDER=[],activeTab='__all__',browseTarget=null,tabDim='cat',activeBrand='';
function detailEmpty(){return '<div class="dhint">點中間的商品，這裡會顯示它的詳細資訊（類別、來源業者/品牌、縣市、批號/有效日期、建議動作）。</div>';}
function detailHtml(it){
  var color=it.kind=='biz'?'#888':(it.kind=='oil'?'#BA7517':'#D85A30');
  function r(k,v){return v?'<div class="drow"><span class="dk">'+esc(k)+'</span><span class="dv">'+esc(v)+'</span></div>':'';}
  var rows;
  if(it.kind=='biz'){ rows=r('類型','受影響店家/通路（列入官方流向名單）')+r('縣市',it.county)+r('進貨油品來源',(it.makers||[]).join('、'))+r('狀態',it.status); }
  else{ rows=r('類別',it.cat)+r('來源業者/品牌',it.source)+r('縣市',it.county)+r(it.kind=='oil'?'受影響批號':'官方標示效期/狀態',it.status); }
  return '<div class="dname" style="border-top:4px solid '+color+';padding-top:10px">'+esc(it.name)+'</div>'+rows+'<div class="dact">'+esc(actText(it))+'</div>'+(it.kind=='biz'?'<button class="btn" style="margin-top:12px" onclick="switchTab(\'map\')">在業者地圖查看位置 →</button>':'');
}
function selectItem(i){selIdx=i;var it=CRES[i];document.querySelectorAll('#clist .lrow').forEach(function(e){e.classList.toggle('sel',(+e.getAttribute('data-i'))===i);});document.getElementById('cdetail').innerHTML=it?detailHtml(it):detailEmpty();if(it)addHist('商品',it.name,it.source);}
function lrow(it){var k=itemKey(it);return '<div class="lrow" data-i="'+it.__i+'" onclick="selectItem('+it.__i+')"><input type="checkbox" class="lchk" '+(CART[k]?'checked':'')+' onclick="event.stopPropagation()" onchange="toggleCart('+it.__i+')"><span class="ln">'+hl(it.name,CKWS)+'</span></div>';}
function renderCheck(){
  var raw=(document.getElementById('cq').value||'').trim();
  CKWS=raw.split(/\s+/).filter(Boolean);var kws=norm(raw).split(/\s+/).filter(Boolean);
  var box=document.getElementById('clist'),crumb=document.getElementById('crumb'),det=document.getElementById('cdetail');
  updateBrandChips();
  var hasFilter=kws.length>0||activeCat||activeItem||browseTarget;
  var cp=['<span class="x" onclick="clearCheck()">全部</span>'];
  if(activeItem) cp.push('▸ <b>'+esc(activeItem)+'</b>');
  if(raw) cp.push('· 關鍵字「'+esc(raw)+'」');
  crumb.innerHTML=cp.join(' ')+(hasFilter?'　<span class="x" onclick="clearCheck()">✕ 清除</span>':'');
  if(!hasFilter){document.getElementById('ctabs').innerHTML='';document.getElementById('dimtoggle').style.display='none';updateTree();box.innerHTML='<div class="hint">用左側「搜尋」輸入商品名、點「知名品牌」，或點「類別」；中間上方有<b>分類標籤</b>（可切換「依品項類別／依來源業者」），下方列出品名，點名稱即在右側看完整資訊。店家完整名單請見「業者地圖」。</div>';det.innerHTML=detailEmpty();CRES=[];return;}
  var browsing=browseTarget && kws.length===0 && !activeCat && !activeItem;
  CRES=browsing?IDX.filter(function(it){return it.kind!=='biz';}):IDX.filter(function(it){if(activeCat && it.cat!==activeCat) return false;if(activeItem && it.name!==activeItem) return false;var hay=norm(it.name+' '+it.source);return kws.every(function(k){return hay.indexOf(k)>=0;});});
  if(CRES.length===0){document.getElementById('ctabs').innerHTML='';document.getElementById('dimtoggle').style.display='none';box.innerHTML='<div class="ok">找不到符合的品項——目前<b>不在</b>本頁公告的下架/受影響清單中。<br><span style="font-size:12px">提醒：名單持續更新、比對僅依品名；請仍以商品外包裝批號與有效日期、及官方最新公告為準。</span></div>';det.innerHTML=detailEmpty();return;}
  CRES.forEach(function(it,i){it.__i=i;});
  activeTab=browsing?browseTarget:'__all__';
  groupAndRender();
}
function groupAndRender(){
  GROUPS={};
  var keyf=(tabDim==='src')?function(it){return it.source;}:function(it){return it.cat;};
  CRES.forEach(function(it){var k=keyf(it);(GROUPS[k]=GROUPS[k]||[]).push(it);});
  GORDER=Object.keys(GROUPS).filter(function(c){return c!=='受影響店家/通路';}).sort(function(a,b){return GROUPS[b].length-GROUPS[a].length;});
  if(!(activeTab==='__all__'||GROUPS[activeTab])) activeTab='__all__';
  var dt=document.getElementById('dimtoggle');if(dt)dt.style.display='';
  renderTabs();renderList();updateDimToggle();
}
function setDim(d){tabDim=d;activeTab='__all__';groupAndRender();}
function updateDimToggle(){document.querySelectorAll('#dimtoggle button').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-d')===tabDim);});}
function renderTabs(){
  function mk(t,label,n){return '<button class="ctab'+(t===activeTab?' on':'')+'" data-t="'+esc(t)+'" onclick="setTab(this.getAttribute(\'data-t\'))">'+esc(label)+' <span class="cnt">'+n+'</span></button>';}
  var h=[mk('__all__','全部',CRES.length)];
  GORDER.forEach(function(cat){h.push(mk(cat,cat,GROUPS[cat].length));});
  document.getElementById('ctabs').innerHTML=h.join('');
}
function setTab(t){activeTab=t;document.querySelectorAll('#ctabs .ctab').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-t')===t);});renderList();}
function renderList(){
  var items=(activeTab==='__all__')?CRES:(GROUPS[activeTab]||[]);
  document.getElementById('clist').innerHTML=items.map(function(it){return lrow(it);}).join('');
  if(items.length) selectItem(items[0].__i);
  updateTree();
}
function buildBrands(){
  var LIST=[['路易莎咖啡','路易莎'],['卜蜂','卜蜂'],['聯華食品(御飯糰/零食)','聯華食品'],['有明(關東煮/火鍋料)','有明'],['味全','味全'],['明德(豆瓣醬)','明德'],['味王','味王'],['南僑','南僑'],['金色三麥','金色三麥'],['廣達香','廣達香'],['聯合利華','聯合利華'],['維義','維義'],['老協珍','老協珍'],['桂冠','桂冠'],['巧福(牛肉麵)','巧福'],['貴族世家(牛排)','貴族世家'],['布列德(麵包)','布列德'],['爭鮮','爭鮮'],['晶華','晶華'],['大買家','大買家'],['家福(家樂福)','家福'],['大全聯','大全聯'],['頂好(惠康)','惠康'],['泰山','泰山'],['福壽','福壽'],['益康','益康']];
  var rows=LIST.map(function(p){var kw=norm(p[1]);var c=IDX.filter(function(it){return norm(it.name+' '+it.source).indexOf(kw)>=0;}).length;return {label:p[0],kw:p[1],c:c};}).filter(function(r){return r.c>0;});
  rows.sort(function(a,b){return b.c-a.c;});
  document.getElementById('qbrands').innerHTML=rows.map(function(r){return '<button class="chipbtn" data-brand="'+esc(r.kw)+'" onclick="pickBrand(this.getAttribute(\'data-brand\'))">'+esc(r.label)+' <span class="cnt">'+r.c+'</span></button>';}).join('');
}
function pickBrand(t){document.getElementById('cq').value=t;activeCat='';activeItem='';browseTarget=null;activeBrand=t;renderCheck();scrollToResults();addHist('品牌',t);}
function buildTree(){
  var all={};IDX.filter(function(it){return it.kind!=='biz';}).forEach(function(it){(all[it.cat]=all[it.cat]||[]).push(it);});
  var cats=Object.keys(all).sort(function(a,b){if(a==='受影響店家/通路')return 1;if(b==='受影響店家/通路')return -1;return all[b].length-all[a].length;});
  document.getElementById('cattree').innerHTML=cats.map(function(cat){return '<button class="catbtn" data-cat="'+esc(cat)+'" onclick="browseCat(this.getAttribute(\'data-cat\'))"><span>'+esc(cat)+'</span><span class="cnt">'+all[cat].length+'</span></button>';}).join('');
}
function updateTree(){document.querySelectorAll('#cattree .catbtn').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-cat')===activeTab);});}
function updateBrandChips(){document.querySelectorAll('#qbrands .chipbtn').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-brand')===activeBrand);});}
function browseCat(cat){document.getElementById('cq').value='';activeCat='';activeItem='';activeBrand='';tabDim='cat';browseTarget=cat;renderCheck();scrollToResults();addHist('類別',cat);}
function clearCheck(){document.getElementById('cq').value='';activeCat='';activeItem='';browseTarget=null;activeBrand='';renderCheck();}
var CART={};
function itemKey(it){return it.name+'||'+it.source;}
function saveCart(){try{localStorage.setItem('zl_cart',JSON.stringify(CART));}catch(e){}}
function loadCart(){try{CART=JSON.parse(localStorage.getItem('zl_cart')||'{}')||{};}catch(e){CART={};}}
function toggleCart(i){var it=CRES[i];if(!it)return;var k=itemKey(it);if(CART[k])delete CART[k];else CART[k]={name:it.name,source:it.source,cat:it.cat,status:it.status};saveCart();renderCart();}
function removeCartAt(idx){var k=Object.keys(CART)[idx];if(k){delete CART[k];saveCart();renderCart();refreshRowChecks();}}
function clearCart(){CART={};saveCart();renderCart();refreshRowChecks();}
function refreshRowChecks(){document.querySelectorAll('#clist .lrow').forEach(function(row){var it=CRES[+row.getAttribute('data-i')];var chk=row.querySelector('.lchk');if(it&&chk)chk.checked=!!CART[itemKey(it)];});}
function copyCart(){var t=Object.keys(CART).map(function(k){return CART[k].name+'（'+CART[k].source+'）';}).join('\n');if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t);}var el=document.getElementById('cartcopy');if(el){el.textContent='已複製';setTimeout(function(){el.textContent='複製';},1500);}}
function renderCart(){var keys=Object.keys(CART);var el=document.getElementById('mycart');if(!el)return;if(keys.length===0){el.innerHTML='<div class="carthd">我的清單（0）</div><div class="carthint">勾選你買過的商品（中間清單每列前方的方框），會列在這裡，方便帶去退貨核對。</div>';return;}el.innerHTML='<div class="carthd">我的清單（'+keys.length+'）<span class="lk" onclick="clearCart()">清空</span><span class="lk" id="cartcopy" onclick="copyCart()">複製</span><span class="lk" onclick="downloadCart()">下載</span></div>'+keys.map(function(k,idx){var it=CART[k];return '<div class="cartrow"><span>'+esc(it.name)+' <span style="color:var(--ink3)">· '+esc(it.source)+'</span></span><span class="cx" onclick="removeCartAt('+idx+')">✕</span></div>';}).join('');}

var HIST=[];
function loadHist(){try{HIST=JSON.parse(localStorage.getItem('zl_history')||'[]')||[];}catch(e){HIST=[];}}
function saveHist(){try{localStorage.setItem('zl_history',JSON.stringify(HIST.slice(0,25)));}catch(e){}}
function addHist(type,label,source){if(!label)return;var key=type+'|'+label+'|'+(source||'');HIST=HIST.filter(function(h){return (h.t+'|'+h.l+'|'+(h.s||''))!==key;});HIST.unshift({t:type,l:label,s:source||'',ts:Date.now()});if(HIST.length>25)HIST=HIST.slice(0,25);saveHist();renderHist();}
function fmtHt(ts){try{var d=new Date(ts),p=function(n){return (n<10?'0':'')+n;};return (d.getMonth()+1)+'/'+d.getDate()+' '+p(d.getHours())+':'+p(d.getMinutes());}catch(e){return '';}}
function runHist(idx){var h=HIST[idx];if(!h)return;if(h.t==='品牌'){pickBrand(h.l);}else if(h.t==='類別'){browseCat(h.l);}else{document.getElementById('cq').value=h.l;activeCat='';activeItem='';browseTarget=null;activeBrand='';renderCheck();scrollToResults();}}
function clearHist(){HIST=[];saveHist();renderHist();}
function renderHist(){var el=document.getElementById('histbox');if(!el)return;if(!HIST.length){el.innerHTML='';return;}el.innerHTML='<div class="slab">最近查詢<span class="lk" onclick="clearHist()" style="float:right;font-weight:400">清除</span></div>'+HIST.slice(0,12).map(function(h,i){return '<div class="histrow" onclick="runHist('+i+')" title="點一下重新查詢"><span class="htag">'+esc(h.t)+'</span><span class="hl">'+esc(h.l)+(h.s?' <span style="color:var(--ink3)">·'+esc(h.s)+'</span>':'')+'</span><span class="hts">'+fmtHt(h.ts)+'</span></div>';}).join('');}
function downloadCart(){var keys=Object.keys(CART);if(!keys.length)return;var L=[];L.push('中聯油脂問題油品 · 我的退貨核對清單');L.push('產生時間：'+new Date().toLocaleString('zh-TW'));L.push('資料以食藥署官方公告為準；第三方整理、非官方判定。');L.push('');keys.forEach(function(k,i){var it=CART[k];L.push((i+1)+'. '+it.name+'（'+it.source+'）');});L.push('');L.push('查詢工具：https://macrock23.github.io/zhonglian-oil/　食安專線 1919');var blob=new Blob([L.join('\r\n')],{type:'text/plain;charset=utf-8'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='退貨核對清單.txt';document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},120);}
loadCart();loadHist();buildBrands();buildTree();renderCheck();renderCart();renderHist();
document.getElementById('cq').addEventListener('input',function(){activeCat='';activeItem='';browseTarget=null;activeBrand='';renderCheck();});
function initResizers(){
  document.querySelectorAll('.resizer').forEach(function(rz){
    rz.addEventListener('mousedown',function(e){
      e.preventDefault();
      var side=rz.getAttribute('data-target');
      var target=(side==='detail')?rz.nextElementSibling:rz.previousElementSibling;
      var startX=e.clientX, startW=target.getBoundingClientRect().width;
      rz.classList.add('drag');document.body.style.cursor='col-resize';document.body.style.userSelect='none';
      function mm(ev){var dx=ev.clientX-startX;var w=(side==='detail')?(startW-dx):(startW+dx);w=Math.max(180,Math.min(680,w));target.style.width=w+'px';target.style.minWidth=w+'px';target.style.flex='0 0 '+w+'px';}
      function mu(){document.removeEventListener('mousemove',mm);document.removeEventListener('mouseup',mu);rz.classList.remove('drag');document.body.style.cursor='';document.body.style.userSelect='';if(window.map&&map.invalidateSize)setTimeout(function(){map.invalidateSize();},0);}
      document.addEventListener('mousemove',mm);document.addEventListener('mouseup',mu);
    });
  });
}
initResizers();
</script>
<script>
function sortTable(th){try{var table=th.closest('table');var idx=[].indexOf.call(th.parentNode.children,th);var tb=table.tBodies[0];if(!tb)return;var rows=[].slice.call(tb.rows);th._asc=!th._asc;var asc=th._asc;rows.sort(function(a,b){var x=((a.cells[idx]||{}).textContent||'').trim();var y=((b.cells[idx]||{}).textContent||'').trim();var nx=parseFloat(x),ny=parseFloat(y);if(!isNaN(nx)&&!isNaN(ny)&&/^[0-9]/.test(x)&&/^[0-9]/.test(y))return asc?nx-ny:ny-nx;return asc?x.localeCompare(y,'zh-Hant'):y.localeCompare(x,'zh-Hant');});rows.forEach(function(r){tb.appendChild(r);});}catch(e){}}
function applyFont(f){document.documentElement.setAttribute('data-fontscale',f||'');try{localStorage.setItem('zl_font',f||'');}catch(e){}var b=document.getElementById('fontBtn');if(b){b.setAttribute('aria-pressed',f==='lg'?'true':'false');b.textContent=(f==='lg'?'字級 大':'字級 標準');}}
function toggleFont(){applyFont(document.documentElement.getAttribute('data-fontscale')==='lg'?'':'lg');}
(function(){var f;try{f=localStorage.getItem('zl_font');}catch(e){}applyFont(f==='lg'?'lg':'');})();
function scrollToResults(){if(window.innerWidth<=900){var el=document.querySelector('#page-check .content');if(el&&el.scrollIntoView)el.scrollIntoView({behavior:'smooth',block:'start'});}}
(function(){var tl=document.querySelector('.tabbar');if(!tl)return;var order=['check','map','term','info'];tl.addEventListener('keydown',function(e){if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft'&&e.key!=='Home'&&e.key!=='End')return;e.preventDefault();var cur=document.querySelector('.tab.active');var i=order.indexOf(cur?cur.dataset.tab:'check');if(e.key==='ArrowRight')i=(i+1)%order.length;else if(e.key==='ArrowLeft')i=(i-1+order.length)%order.length;else if(e.key==='Home')i=0;else i=order.length-1;switchTab(order[i]);var nb=document.getElementById('tab-'+order[i]);if(nb)nb.focus();});})();
</script>
</body>
</html>'''
html=TEMPLATE
for _ph,_p in _LIBS:
    html=html.replace(_ph,_r(_p))
html=html.replace('__DATA__', data)
open('index.html','w',encoding='utf-8').write(html)
open('中聯油脂_下游業者互動地圖.html','w',encoding='utf-8').write(html)
print('WROTE index.html + map html', len(html))
