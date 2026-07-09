# -*- coding: utf-8 -*-
import json, re, math

pts = json.load(open('points.json'))
prods = json.load(open('products.json'))['products']
term = json.load(open('terminal_products.json'))

located = pts['features']
unloc = pts.get('unlocated', [])

# ---- maker attribution ----
def norm(s): return re.sub(r'\s+', '', s or '').replace('　','')
alias2maker={}
for p in prods:
    comp=p['company']
    mk='泰山' if '泰山' in comp else '福壽' if '福壽' in comp else '福懋' if '福懋' in comp else comp
    for k in [p['name']]+p.get('aliases',[]): alias2maker[norm(k)]=mk
def maker_for(prod,batch):
    n=norm(prod)
    if n in alias2maker: return alias2maker[n]
    if '益康' in (prod or ''): return '福懋'
    if '泰山' in (prod or ''): return '泰山'
    if '健味香油' in (prod or ''): return '福壽'
    b=(batch or '')
    if b.startswith('315-1150404'): return '中聯油脂(源頭)'
    if prod in ('原油','大豆沙拉油'): return '中聯油脂(源頭)'
    if prod=='一級黃豆油': return '中聯油脂(源頭)' if b.startswith('315') else '福懋'
    if b[:2] in ('C1','C2') or b.startswith('BL'): return '福壽'
    if re.fullmatch(r'2026\d{8}',b) or re.fullmatch(r'2027\d{8,}',b): return '福懋'
    if re.fullmatch(r'2027\d{6}',b): return '泰山'
    return '其他'

notes={}
for s in (98,331): notes[s]='同序號96「建樹企業有限公司」（重複）'
for s in (104,243,298,345): notes[s]='經衛生局回復應刪除（第二批名單已更新）'
for s in (240,266,267,301,322): notes[s]='飼料用（非供食品烹製）'
notes[274]='工業用：作環氧大豆油增塑劑/安定劑，非供食品烹製'
notes[360]='單據誤植「誠一」，實際應為「和香行」'

# ---- county centroids (approx) ----
CENT={
 '基隆市':[25.128,121.741],'臺北市':[25.037,121.565],'新北市':[25.011,121.445],
 '桃園市':[24.993,121.301],'新竹市':[24.803,120.968],'新竹縣':[24.703,121.125],
 '苗栗縣':[24.560,120.821],'臺中市':[24.147,120.673],'彰化縣':[24.051,120.516],
 '南投縣':[23.902,120.685],'雲林縣':[23.709,120.431],'嘉義市':[23.480,120.449],
 '嘉義縣':[23.452,120.255],'臺南市':[23.000,120.227],'高雄市':[22.627,120.301],
 '屏東縣':[22.552,120.549],'宜蘭縣':[24.702,121.738],'花蓮縣':[23.987,121.601],
 '臺東縣':[22.758,121.144],'澎湖縣':[23.571,119.579],'金門縣':[24.436,118.317],
 '連江縣':[26.160,119.951],
}

def maker_list(pl,bs):
    mks=[]
    for i,pr in enumerate(pl):
        bt=bs[i] if i<len(bs) else ''
        mks.append(maker_for(pr,bt))
    return list(dict.fromkeys([m for m in mks if m]))

businesses=[]
# located
for f in located:
    p=f['properties']; co=f['geometry']['coordinates']
    pl=p.get('products',[]); bs=p.get('batches',[]); ex=p.get('expiries',[])
    mks=maker_list(pl,bs)
    businesses.append({
      'seq':p['seq'],'name':p['name'],'county':(p.get('counties') or [''])[0],
      'addr':p.get('address',''),'products':pl,'batches':bs,'expiries':ex,
      'makers':mks,'maker':mks[0] if mks else '其他','note':notes.get(p['seq'],''),
      'lat':co[1],'lng':co[0],'located':True
    })
# unlocated -> county centroid with deterministic spiral jitter
county_idx={}
for u in unloc:
    p=u['properties'] if 'properties' in u else u
    cty=(p.get('counties') or [''])[0]
    pl=p.get('products',[]); bs=p.get('batches',[]); ex=p.get('expiries',[])
    mks=maker_list(pl,bs)
    base=CENT.get(cty,[23.8,120.9])
    k=county_idx.get(cty,0); county_idx[cty]=k+1
    ang=k*2.399963; rad=0.012*math.sqrt(k+1)
    lat=base[0]+rad*math.cos(ang); lng=base[1]+rad*math.sin(ang)
    businesses.append({
      'seq':p['seq'],'name':p['name'],'county':cty,'addr':'',
      'products':pl,'batches':bs,'expiries':ex,'makers':mks,
      'maker':mks[0] if mks else '其他','note':notes.get(p['seq'],''),
      'lat':round(lat,6),'lng':round(lng,6),'located':False
    })
businesses.sort(key=lambda b:b['seq'])

# upstream products with official 泰山 batch fix
TSFIX={'20270408':'2027040801','20270409':'2027040901','20270725d':'2027072506','20270413E':'2027041301','20271013':'2027101301','20270725f':'2027072504','20271009':'2027100901'}
upstream=[]
for p in prods:
    comp=p['company']; mk='泰山' if '泰山' in comp else '福壽' if '福壽' in comp else '福懋' if '福懋' in comp else comp
    for b in p['batches']:
        upstream.append({'maker':mk,'name':p['name'],'batch':TSFIX.get(b['code'],b['code']),'expiry':b['expiry']})
upstream.append({'maker':'中聯油脂(源頭)','name':'大豆沙拉油／原油／一級黃豆油','batch':'315-1150404','expiry':'115.9.30'})

# terminal
terminal=[]
for v in term['vendors']:
    for pr in v['products']:
        terminal.append({'seq':v['seq'],'county':v.get('county',''),'vendor':v['name'],'pseq':pr.get('seq',''),'name':pr['name'],'expiry':pr.get('expiry','')})

# distinct products list for filter
allprods=sorted({pr for b in businesses for pr in b['products']})

DATA={'businesses':businesses,'upstream':upstream,'terminal':terminal,
      'terminalUpdated':term.get('updated',''),'products':allprods,
      'centroids':CENT,
      'stats':{'total':len(businesses),'located':sum(1 for b in businesses if b['located']),
               'unlocated':sum(1 for b in businesses if not b['located']),
               'counties':len(sorted({b['county'] for b in businesses if b['county']}))}}

open('dashboard_data.json','w',encoding='utf-8').write(json.dumps(DATA,ensure_ascii=False))
print('businesses',len(businesses),'located',DATA['stats']['located'],'unlocated',DATA['stats']['unlocated'],'counties',DATA['stats']['counties'])
print('upstream rows',len(upstream),'terminal rows',len(terminal),'distinct products',len(allprods))
from collections import Counter
print('maker',Counter(b['maker'] for b in businesses))
print('unloc counties',Counter(b['county'] for b in businesses if not b['located']))
