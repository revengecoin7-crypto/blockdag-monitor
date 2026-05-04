"""
BTC/USDT — Geen Stop Loss, onbeperkte trades

Regels:
  1. Nieuw signaal -> scan ALLE open trades
       Positief  -> direct sluiten (winst incasseren)
       Negatief  -> laat staan, hoe lang ook
  2. Open altijd de nieuwe trade
  3. GEEN stop loss, GEEN take profit
     Trade sluit ALLEEN als hij positief is bij een volgend signaal
  4. Onbeperkt aantal gelijktijdige trades
  5. Kapitaal per trade: EUR 10 (10% van EUR 100)

15m candles | 2026-01-01 tot vandaag | BTC/USDT
"""
import ccxt, pandas as pd, numpy as np, time, warnings
warnings.filterwarnings('ignore')

# ── Data ──────────────────────────────────────────────────────────────────────
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

# ── Indicatoren ───────────────────────────────────────────────────────────────
def calc_indicators(df):
    c=df['Close']; h=df['High']; l=df['Low']; v=df['Volume']
    df['ef']  = c.ewm(span=9,  adjust=False).mean()
    df['es']  = c.ewm(span=21, adjust=False).mean()
    df['et']  = c.ewm(span=55, adjust=False).mean()
    d  = c.diff()
    g  = d.clip(lower=0).ewm(com=12, adjust=False).mean()
    lo = (-d.clip(upper=0)).ewm(com=12, adjust=False).mean()
    df['rsi'] = 100 - 100/(1 + g/lo)
    mf=c.ewm(span=12,adjust=False).mean(); ms2=c.ewm(span=26,adjust=False).mean()
    macd=mf-ms2; sig=macd.ewm(span=9,adjust=False).mean()
    df['macd_hist'] = macd - sig
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
    df['swing_lo']=l.rolling(10).min()
    df['swing_hi']=h.rolling(10).max()
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

# ── Backtest ──────────────────────────────────────────────────────────────────
def run(df, start_cap=100, alloc_per_trade=10.0, commission=0.001, min_score=5.0):
    equity      = start_cap
    open_trades = []
    closed      = []
    last_dir    = 0
    max_open    = 0
    rows        = df.reset_index()
    equity_curve = [start_cap]

    for i in range(1, len(rows)):
        row  = rows.iloc[i]
        prev = rows.iloc[i-1]
        cl   = row['Close']

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

            # Scan open trades: positief sluiten, negatief laten
            still_open = []
            for t in open_trades:
                pnl_now = ((cl - t['entry']) / t['entry'] if t['dir'] == 'long'
                           else (t['entry'] - cl) / t['entry'])
                if pnl_now > 0:
                    net = alloc_per_trade * pnl_now - 2 * commission * alloc_per_trade
                    equity += net
                    bars_open = i - t['bar']
                    closed.append({
                        'dir':       t['dir'],
                        'entry':     t['entry'],
                        'exit':      cl,
                        'pnl_pct':   round(pnl_now * 100, 3),
                        'pnl_eur':   round(net, 4),
                        'bars_open': bars_open,
                        'closed_by': 'Winst-sluit',
                        'open_bar':  t['bar'],
                        'close_bar': i
                    })
                else:
                    still_open.append(t)

            open_trades = still_open

            # Open nieuwe trade
            open_trades.append({
                'dir':   new_dir,
                'entry': cl,
                'bar':   i,
                'score': bs if new_dir == 'long' else be
            })
            last_dir = 1 if new_dir == 'long' else -1

            if len(open_trades) > max_open:
                max_open = len(open_trades)

        equity_curve.append(equity)

    # Sluit alle resterende open trades op slotkoers
    cl_final = rows.iloc[-1]['Close']
    for t in open_trades:
        pnl = ((cl_final - t['entry']) / t['entry'] if t['dir'] == 'long'
               else (t['entry'] - cl_final) / t['entry'])
        net = alloc_per_trade * pnl - 2 * commission * alloc_per_trade
        equity += net
        closed.append({
            'dir':       t['dir'],
            'entry':     t['entry'],
            'exit':      cl_final,
            'pnl_pct':   round(pnl * 100, 3),
            'pnl_eur':   round(net, 4),
            'bars_open': len(rows) - 1 - t['bar'],
            'closed_by': 'Einde data',
            'open_bar':  t['bar'],
            'close_bar': len(rows) - 1
        })

    # Nog open posities unrealized P&L
    unrealized = sum(
        alloc_per_trade * ((cl_final - t['entry']) / t['entry'] if t['dir'] == 'long'
                           else (t['entry'] - cl_final) / t['entry'])
        for t in open_trades
    )

    return equity, closed, max_open, equity_curve, len(open_trades), unrealized

# ── Main ──────────────────────────────────────────────────────────────────────
START_DATE     = '2026-01-01'
START_CAP      = 100
ALLOC          = 10.0   # EUR per trade
COMMISSION     = 0.001

print(f"\n{'='*70}")
print(f"  BTC/USDT  |  GEEN Stop Loss  |  Onbeperkte trades")
print(f"  Positieve trades sluiten bij nieuw signaal")
print(f"  Negatieve trades blijven open tot ze positief zijn")
print(f"  EUR {ALLOC:.0f} per trade  |  15m  |  {START_DATE} tot vandaag")
print(f"{'='*70}\n")

df_raw = fetch('BTC/USDT', '15m', START_DATE)
df_ind = calc_indicators(df_raw.copy())
final_eq, closed, max_open, eq_curve, still_open_count, unrealized = run(
    df_ind, start_cap=START_CAP, alloc_per_trade=ALLOC, commission=COMMISSION
)

df_t = pd.DataFrame(closed)

wins  = df_t[df_t['pnl_eur'] > 0]
loss  = df_t[df_t['pnl_eur'] <= 0]
total = len(df_t)

# Trades nog open aan het einde
einde_open = df_t[df_t['closed_by'] == 'Einde data']
winst_sluit = df_t[df_t['closed_by'] == 'Winst-sluit']

# Max drawdown
peak = eq_curve[0]; max_dd = 0
for e in eq_curve:
    if e > peak: peak = e
    dd = (peak - e) / peak * 100
    if dd > max_dd: max_dd = dd

# Langste trade open
if total > 0:
    longest = df_t['bars_open'].max()
    longest_h = round(longest * 15 / 60, 1)
else:
    longest = longest_h = 0

pf = abs(wins['pnl_eur'].sum()/loss['pnl_eur'].sum()) if loss['pnl_eur'].sum() != 0 else 999

# Long vs Short
longs  = len(df_t[df_t['dir']=='long'])
shorts = len(df_t[df_t['dir']=='short'])

print(f"  RESULTAAT:")
print(f"  EUR {START_CAP:.2f}  ->  EUR {round(final_eq,2):.2f}  ({round((final_eq-START_CAP)/START_CAP*100,2):+.2f}%)")
print()
print(f"  Trades (gesloten):     {total}")
print(f"    Gesloten via winst:  {len(winst_sluit)}")
print(f"    Gesloten einde data: {len(einde_open)}")
print(f"    Long:  {longs}  |  Short: {shorts}")
print()
print(f"  Win Rate:              {round(len(wins)/total*100,1) if total else 0}%")
print(f"  Profit Factor:         {round(pf,2)}")
print(f"  Gem win:               EUR {round(wins['pnl_eur'].mean(),3) if len(wins) else 0:.3f}")
print(f"  Gem verlies:           EUR {round(loss['pnl_eur'].mean(),3) if len(loss) else 0:.3f}")
print()
print(f"  Max gelijktijdig open: {max_open}")
print(f"  Langste trade open:    {longest} bars = {longest_h} uur")
print(f"  Max Drawdown:          {round(max_dd,2)}%")
print()

# Trades nog open aan het einde (wachten nog op winst)
waiting = df_t[df_t['closed_by'] == 'Einde data'].copy()
if len(waiting) > 0:
    waiting['pnl_now_pct'] = waiting['pnl_pct']
    print(f"  Trades die nog wachten op positief (open op einddatum):")
    print(f"  {'Richting':<8} {'Entry':>10} {'Huidige P&L':>12} {'Open (uur)':>12}")
    print(f"  {'-'*46}")
    for _, w in waiting.iterrows():
        bars = w['bars_open']
        uren = round(bars * 15 / 60, 1)
        print(f"  {w['dir']:<8} {w['entry']:>10.2f} {w['pnl_pct']:>+11.2f}% {uren:>11.1f}h")

print(f"\n{'='*70}")

# Top 5 langste open trades
print(f"\n  TOP 5 LANGST OPEN TRADES:")
print(f"  {'Richting':<8} {'Entry':>10} {'Exit':>10} {'P&L':>8} {'Open (uur)':>12} {'Gesloten via'}")
print(f"  {'-'*62}")
top5 = df_t.nlargest(5, 'bars_open')
for _, r in top5.iterrows():
    uren = round(r['bars_open'] * 15 / 60, 1)
    print(f"  {r['dir']:<8} {r['entry']:>10.2f} {r['exit']:>10.2f} {r['pnl_pct']:>+7.2f}% {uren:>11.1f}h  {r['closed_by']}")
print(f"{'='*70}\n")
