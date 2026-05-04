"""
BTC/USDT — Binance Futures, 5% Stop Loss, meerdere leverage niveaus

Regels:
  - Bij nieuw signaal: positieve trades sluiten, negatieve laten staan
  - Stop Loss op 5% spot beweging tegen je in
  - Liquidatie als vangnet (bij extreme moves)
  - Marge per trade: EUR 10
  - Onbeperkt gelijktijdige trades
  - BTC/USDT | 15m | 2026-01-01 tot vandaag
"""
import ccxt, pandas as pd, numpy as np, time, warnings
warnings.filterwarnings('ignore')

def fetch(symbol, tf, since):
    ex = ccxt.binance({'enableRateLimit': True})
    ms = int(pd.Timestamp(since).timestamp() * 1000)
    out = []
    print(f"  {symbol} {tf}...", end='', flush=True)
    while True:
        b = ex.fetch_ohlcv(symbol, tf, since=ms, limit=1000)
        if not b: break
        out.extend(b)
        last = b[-1][0]
        if last >= int(pd.Timestamp('now', tz='UTC').timestamp() * 1000): break
        ms = last + 1
        time.sleep(0.08)
        print('.', end='', flush=True)
    print(f" {len(out)} candles")
    df = pd.DataFrame(out, columns=['ts','Open','High','Low','Close','Volume'])
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df.set_index('ts', inplace=True)
    return df[~df.index.duplicated()]

def calc_indicators(df):
    c=df['Close']; h=df['High']; l=df['Low']; v=df['Volume']
    df['ef']  = c.ewm(span=9,  adjust=False).mean()
    df['es']  = c.ewm(span=21, adjust=False).mean()
    df['et']  = c.ewm(span=55, adjust=False).mean()
    d=c.diff()
    g=d.clip(lower=0).ewm(com=12,adjust=False).mean()
    lo=(-d.clip(upper=0)).ewm(com=12,adjust=False).mean()
    df['rsi']=100-100/(1+g/lo)
    mf=c.ewm(span=12,adjust=False).mean()
    ms2=c.ewm(span=26,adjust=False).mean()
    macd=mf-ms2
    sig=macd.ewm(span=9,adjust=False).mean()
    df['macd_hist']=macd-sig
    pc=c.shift()
    tr=pd.concat([h-l,(h-pc).abs(),(l-pc).abs()],axis=1).max(axis=1)
    df['atr']=tr.ewm(com=13,adjust=False).mean()
    dp=(h-h.shift()).clip(lower=0); dm=(l.shift()-l).clip(lower=0)
    dp=dp.where(dp>dm,0); dm=dm.where(dm>dp,0)
    atr_s=tr.ewm(com=13,adjust=False).mean()
    dip=100*dp.ewm(com=13,adjust=False).mean()/atr_s
    dim=100*dm.ewm(com=13,adjust=False).mean()/atr_s
    dx=100*(dip-dim).abs()/(dip+dim+1e-9)
    df['adx']=dx.ewm(com=13,adjust=False).mean()
    df['dip']=dip; df['dim']=dim
    tp2=(h+l+c)/3
    df['vwap']=(tp2*v).cumsum()/v.cumsum()
    df['vol_ok']=v>v.rolling(20).mean()*1.2
    return df.dropna()

def get_score(r, direction):
    ef=r['ef']; es=r['es']; et=r['et']; c=r['Close']
    rsi=r['rsi']; mh=r['macd_hist']
    adx=r['adx']; dp=r['dip']; dm=r['dim']
    vwap=r['vwap']; vol=r['vol_ok']
    if direction == 'long':
        return sum([ef>es, c>et, 50<rsi<75, mh>0, c>vwap, bool(vol),
                    adx>20 and dp>dm, 0.5 if c>ef else 0])
    else:
        return sum([ef<es, c<et, 25<rsi<50, mh<0, c<vwap, bool(vol),
                    adx>20 and dm>dp, 0.5 if c<ef else 0])

def run(df, start_cap=100, margin=10.0, leverage=10,
        sl_pct=0.05, commission=0.0004, min_score=5.0):

    equity      = start_cap
    open_trades = []
    closed      = []
    last_dir    = 0
    max_open    = 0
    rows        = df.reset_index()
    liq_pct     = -(1.0 / leverage) * 0.9   # liquidatiedrempel

    for i in range(1, len(rows)):
        row  = rows.iloc[i]
        prev = rows.iloc[i-1]
        hi=row['High']; lo=row['Low']; cl=row['Close']

        # ── Check SL / liquidatie op elke bar ────────────────────────────────
        still_open = []
        for t in open_trades:
            d = t['dir']
            worst = ((lo - t['entry']) / t['entry'] if d == 'long'
                     else (t['entry'] - hi) / t['entry'])

            if sl_pct is not None and worst <= -sl_pct:
                # Stop Loss geraakt
                exit_p  = t['entry'] * (1 - sl_pct if d == 'long' else 1 + sl_pct)
                lev_pnl = -sl_pct * leverage
                net     = margin * lev_pnl - 2 * commission * margin * leverage
                equity += net
                closed.append({'dir':d, 'entry':t['entry'], 'exit':round(exit_p,2),
                                'pnl_pct':round(-sl_pct*100,2),
                                'pnl_lev_pct':round(lev_pnl*100,2),
                                'pnl_eur':round(net,4),
                                'bars_open':i-t['bar'],
                                'closed_by':'Stop Loss',
                                'open_bar':t['bar'],'close_bar':i})
            elif worst <= liq_pct:
                # Liquidatie (vangnet)
                net = -margin
                equity += net
                closed.append({'dir':d, 'entry':t['entry'],
                                'exit':round(t['entry']*(1+liq_pct if d=='long' else 1-liq_pct),2),
                                'pnl_pct':round(liq_pct*100,2),
                                'pnl_lev_pct':round(liq_pct*leverage*100,2),
                                'pnl_eur':round(net,4),
                                'bars_open':i-t['bar'],
                                'closed_by':'LIQUIDATIE',
                                'open_bar':t['bar'],'close_bar':i})
            else:
                still_open.append(t)
        open_trades = still_open

        # ── Signalen ──────────────────────────────────────────────────────────
        ef=row['ef']; es=row['es']
        pef=prev['ef']; pes=prev['es']
        rsi=row['rsi']
        bull_cross = (pef < pes) and (ef >= es)
        bear_cross = (pef > pes) and (ef <= es)
        bull_mom   = cl > ef and cl > es
        bear_mom   = cl < ef and cl < es
        bs = get_score(row, 'long')
        be = get_score(row, 'short')
        raw_buy  = bull_cross and bull_mom and rsi < 75 and bs >= min_score and last_dir != 1
        raw_sell = bear_cross and bear_mom and rsi > 25 and be >= min_score and last_dir != -1

        if raw_buy or raw_sell:
            new_dir = 'long' if raw_buy else 'short'

            # Positieve trades sluiten, negatieve laten staan
            still2 = []
            for t in open_trades:
                d = t['dir']
                pnl = ((cl - t['entry']) / t['entry'] if d == 'long'
                       else (t['entry'] - cl) / t['entry'])
                if pnl > 0:
                    lev_pnl = pnl * leverage
                    net = margin * lev_pnl - 2 * commission * margin * leverage
                    equity += net
                    closed.append({'dir':d, 'entry':t['entry'], 'exit':cl,
                                   'pnl_pct':round(pnl*100,3),
                                   'pnl_lev_pct':round(lev_pnl*100,2),
                                   'pnl_eur':round(net,4),
                                   'bars_open':i-t['bar'],
                                   'closed_by':'Winst-sluit',
                                   'open_bar':t['bar'],'close_bar':i})
                else:
                    still2.append(t)
            open_trades = still2

            # Nieuwe trade openen
            open_trades.append({'dir':new_dir,'entry':cl,'bar':i,
                                 'score':bs if new_dir=='long' else be})
            last_dir = 1 if new_dir == 'long' else -1
            if len(open_trades) > max_open:
                max_open = len(open_trades)

    # Sluit resterende trades op slotkoers
    cl_f = rows.iloc[-1]['Close']
    for t in open_trades:
        d = t['dir']
        pnl = ((cl_f-t['entry'])/t['entry'] if d=='long' else (t['entry']-cl_f)/t['entry'])
        lev_pnl = pnl * leverage
        net = margin * lev_pnl - 2 * commission * margin * leverage
        equity += net
        closed.append({'dir':d,'entry':t['entry'],'exit':cl_f,
                        'pnl_pct':round(pnl*100,3),
                        'pnl_lev_pct':round(lev_pnl*100,2),
                        'pnl_eur':round(net,4),
                        'bars_open':len(rows)-1-t['bar'],
                        'closed_by':'Einde data',
                        'open_bar':t['bar'],'close_bar':len(rows)-1})

    return equity, closed, max_open

# ── Main ──────────────────────────────────────────────────────────────────────
START_DATE = '2026-01-01'
START_CAP  = 100
MARGIN     = 10.0
COMMISSION = 0.0004
SL         = 0.05   # 5% stop loss

print(f"\n{'='*72}")
print(f"  BTC/USDT FUTURES  |  Stop Loss: {SL*100:.0f}%  |  Marge: EUR {MARGIN}")
print(f"  15m  |  {START_DATE} tot vandaag  |  Commissie: {COMMISSION*100}% per kant")
print(f"{'='*72}\n")

df_raw = fetch('BTC/USDT', '15m', START_DATE)
df_ind = calc_indicators(df_raw.copy())

print(f"\n  {'Lev':<6} {'Eindkapitaal':<16} {'Return%':<12} {'WinstTrades EUR':<18} {'SL-hits':<10} {'Liqs':<7} {'WinRate':<10} {'MaxOpen'}")
print(f"  {'-'*85}")

results = {}
for lev in [2, 5, 10, 20]:
    final_eq, closed, max_open = run(df_ind, start_cap=START_CAP,
                                      margin=MARGIN, leverage=lev,
                                      sl_pct=SL, commission=COMMISSION)
    df_t = pd.DataFrame(closed)
    wins   = df_t[df_t['pnl_eur'] > 0]
    liqs   = df_t[df_t['closed_by'] == 'LIQUIDATIE']
    sl_hit = df_t[df_t['closed_by'] == 'Stop Loss']
    wsluit = df_t[df_t['closed_by'] == 'Winst-sluit']
    total  = len(df_t)
    wr     = round(len(wins)/total*100,1) if total else 0
    ret    = round((final_eq-START_CAP)/START_CAP*100,2)
    results[lev] = (final_eq, closed, max_open)

    tag = '+ ' if final_eq > START_CAP else '- '
    print(f"  {lev}x{'':<4} {tag}EUR {final_eq:<10.2f}  {ret:>+8.2f}%   "
          f"EUR {wsluit['pnl_eur'].sum():>+8.2f}{'':<8} {len(sl_hit):<10} {len(liqs):<7} {wr}%{'':<5} {max_open}")

# ── Detail 10x ───────────────────────────────────────────────────────────────
print(f"\n{'='*72}")
print(f"  DETAIL: 10x LEVERAGE  +  5% SL")
print(f"{'='*72}")
final_eq, closed, max_open = results[10]
df_t   = pd.DataFrame(closed)
wins   = df_t[df_t['pnl_eur'] > 0]
loss   = df_t[df_t['pnl_eur'] <= 0]
sl_hit = df_t[df_t['closed_by'] == 'Stop Loss']
liqs   = df_t[df_t['closed_by'] == 'LIQUIDATIE']
wsluit = df_t[df_t['closed_by'] == 'Winst-sluit']
einde  = df_t[df_t['closed_by'] == 'Einde data']

print(f"  Eindkapitaal:      EUR {round(final_eq,2)}")
print(f"  Return:            {round((final_eq-START_CAP)/START_CAP*100,2):+.2f}%")
print()
print(f"  Trades totaal:     {len(df_t)}")
print(f"  Winst-sluit:       {len(wsluit):<5}  EUR {wsluit['pnl_eur'].sum():>+8.2f}  gem: EUR {wsluit['pnl_eur'].mean():.3f}/trade")
print(f"  Stop Loss (5%):    {len(sl_hit):<5}  EUR {sl_hit['pnl_eur'].sum():>+8.2f}  gem: EUR {sl_hit['pnl_eur'].mean():.3f}/trade")
print(f"  Liquidaties:       {len(liqs):<5}  EUR {liqs['pnl_eur'].sum():>+8.2f}")
print(f"  Einde data:        {len(einde):<5}  EUR {einde['pnl_eur'].sum():>+8.2f}")
print()
print(f"  Win Rate:          {round(len(wins)/len(df_t)*100,1)}%")
print(f"  Gem win:           EUR {wins['pnl_eur'].mean():.3f}" if len(wins) else "")
print(f"  Gem verlies (SL):  EUR {sl_hit['pnl_eur'].mean():.3f}" if len(sl_hit) else "")
print(f"  Max gelijktijdig:  {max_open} trades open")
print()
print(f"  Per winning trade (gem BTC +{wsluit['pnl_pct'].mean():.2f}% spot):")
print(f"    Spot move:       +{wsluit['pnl_pct'].mean():.2f}%")
print(f"    Met 10x lever.:  +{wsluit['pnl_lev_pct'].mean():.2f}%")
print(f"    EUR winst:       EUR {wsluit['pnl_eur'].mean():.3f} per trade")
print()
print(f"  Per SL trade:")
print(f"    Spot move:       -5.00%")
print(f"    Met 10x lever.:  -50.00%")
print(f"    EUR verlies:     EUR {sl_hit['pnl_eur'].mean():.3f} per trade")
print(f"{'='*72}\n")
