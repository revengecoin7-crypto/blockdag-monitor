"""
Precision Sniper — Multi-trade backtest

Logica:
  - Bij elk nieuw signaal: scan alle open trades
      * Trade is POSITIEF -> sluit hem (winst incasseren)
      * Trade is NEGATIEF -> laat staan (wacht tot hij positief is)
  - Open altijd de nieuwe trade
  - Meerdere trades tegelijk mogelijk

Kapitaal per trade: 20% van startkapitaal (max 5 gelijktijdig = 100%)
Verliezende trades wachten tot ze bij een VOLGENDE trade-opening positief zijn.
Elke trade heeft eigen SL/TP op basis van ATR.
Geen tijdfilter. 15m. 2026-01-01 tot vandaag.
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
    ef2=c.ewm(span=12,adjust=False).mean(); es2=c.ewm(span=26,adjust=False).mean()
    macd=ef2-es2; sig=macd.ewm(span=9,adjust=False).mean()
    df['macd_hist'] = macd - sig
    df['macd_vs']   = macd - sig
    pc  = c.shift()
    tr  = pd.concat([h-l,(h-pc).abs(),(l-pc).abs()],axis=1).max(axis=1)
    df['atr'] = tr.ewm(com=13, adjust=False).mean()
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
    rsi=r['rsi']; mh=r['macd_hist']; mv=r['macd_vs']
    adx=r['adx']; dp=r['dip']; dm=r['dim']
    vwap=r['vwap']; vol=r['vol_ok']
    if direction == 'long':
        s  = sum([ef>es, c>et, 50<rsi<75, mh>0, mv>0, c>vwap, vol,
                  adx>20 and dp>dm, 0.5 if c>ef else 0])
    else:
        s  = sum([ef<es, c<et, 25<rsi<50, mh<0, mv<0, c<vwap, vol,
                  adx>20 and dm>dp, 0.5 if c<ef else 0])
    return s

# ── Backtest met meerdere gelijktijdige trades ────────────────────────────────
def run(df, start_cap=100, alloc_pct=0.20, commission=0.001,
        sl_mult=1.5, tp1_m=1.0, tp2_m=2.0, tp3_m=3.0, min_score=5.0):

    equity      = start_cap
    alloc       = start_cap * alloc_pct   # vaste euro per trade
    open_trades = []                       # alle gelijktijdig open trades
    closed      = []
    last_dir    = 0
    rows        = df.reset_index()

    for i in range(1, len(rows)):
        row  = rows.iloc[i]
        prev = rows.iloc[i-1]
        hi=row['High']; lo=row['Low']; cl=row['Close']; atr=row['atr']

        # ── Beheer alle open trades op elke bar ──────────────────────────────
        still_open = []
        for t in open_trades:
            d = t['dir']
            # Trail update
            if t['tp1_hit'] and not t['tp2_hit']:
                t['trail'] = t['entry']
            if t['tp2_hit'] and not t['tp3_hit']:
                t['trail'] = t['tp1']

            # TP hits
            if d == 'long':
                if hi >= t['tp1'] and not t['tp1_hit']:
                    t['tp1_hit'] = True; t['trail'] = t['entry']
                if hi >= t['tp2'] and not t['tp2_hit']:
                    t['tp2_hit'] = True; t['trail'] = t['tp1']
                if hi >= t['tp3'] and not t['tp3_hit']:
                    t['tp3_hit'] = True
            else:
                if lo <= t['tp1'] and not t['tp1_hit']:
                    t['tp1_hit'] = True; t['trail'] = t['entry']
                if lo <= t['tp2'] and not t['tp2_hit']:
                    t['tp2_hit'] = True; t['trail'] = t['tp1']
                if lo <= t['tp3'] and not t['tp3_hit']:
                    t['tp3_hit'] = True

            # SL / trail hit
            sl_hit = (lo <= t['trail'] if d=='long' else hi >= t['trail'])
            if sl_hit:
                ep = t['trail']
                pnl = ((ep-t['entry'])/t['entry'] if d=='long'
                       else (t['entry']-ep)/t['entry'])
                net_eur = alloc * pnl - 2 * commission * alloc
                equity += net_eur
                closed.append({**t, 'exit':ep,
                                'pnl_eur':round(net_eur,4),
                                'pnl_pct':round(pnl*100,3),
                                'closed_by':'SL/Trail','bar':i})
            else:
                still_open.append(t)

        open_trades = still_open

        # ── Signaal check ────────────────────────────────────────────────────
        ef=row['ef']; es=row['es']
        pef=prev['ef']; pes=prev['es']
        rsi=row['rsi']

        bull_cross = (pef < pes) and (ef >= es)
        bear_cross = (pef > pes) and (ef <= es)
        bull_mom   = cl > ef and cl > es
        bear_mom   = cl < ef and cl < es

        bull_score = get_score(row, 'long')
        bear_score = get_score(row, 'short')

        raw_buy  = bull_cross and bull_mom and rsi < 75 and bull_score >= min_score and last_dir != 1
        raw_sell = bear_cross and bear_mom and rsi > 25 and bear_score >= min_score and last_dir != -1

        if raw_buy or raw_sell:
            new_dir = 'long' if raw_buy else 'short'

            # ── Scan open trades: sluit positieve, laat negatieve staan ──────
            still_open2 = []
            for t in open_trades:
                d = t['dir']
                pnl_now = ((cl-t['entry'])/t['entry'] if d=='long'
                           else (t['entry']-cl)/t['entry'])
                if pnl_now > 0:
                    # Positief -> sluiten
                    net_eur = alloc * pnl_now - 2 * commission * alloc
                    equity += net_eur
                    closed.append({**t, 'exit':cl,
                                   'pnl_eur':round(net_eur,4),
                                   'pnl_pct':round(pnl_now*100,3),
                                   'closed_by':'Winst-sluit','bar':i})
                else:
                    # Negatief -> blijft staan
                    still_open2.append(t)

            open_trades = still_open2

            # ── Open nieuwe trade ────────────────────────────────────────────
            if new_dir == 'long':
                sl = max(row['swing_lo'] - atr*0.2, cl - atr*sl_mult)
                risk = abs(cl - sl)
                t_new = {'dir':'long','entry':cl,'sl':sl,'trail':sl,
                         'tp1':cl+risk*tp1_m,'tp2':cl+risk*tp2_m,'tp3':cl+risk*tp3_m,
                         'risk':risk,'tp1_hit':False,'tp2_hit':False,'tp3_hit':False,
                         'bar':i,'score':bull_score}
                last_dir = 1
            else:
                sl = min(row['swing_hi'] + atr*0.2, cl + atr*sl_mult)
                risk = abs(cl - sl)
                t_new = {'dir':'short','entry':cl,'sl':sl,'trail':sl,
                         'tp1':cl-risk*tp1_m,'tp2':cl-risk*tp2_m,'tp3':cl-risk*tp3_m,
                         'risk':risk,'tp1_hit':False,'tp2_hit':False,'tp3_hit':False,
                         'bar':i,'score':bear_score}
                last_dir = -1

            open_trades.append(t_new)

    # ── Sluit alle nog open trades aan het einde ──────────────────────────────
    cl_final = rows.iloc[-1]['Close']
    for t in open_trades:
        d = t['dir']
        pnl = ((cl_final-t['entry'])/t['entry'] if d=='long'
               else (t['entry']-cl_final)/t['entry'])
        net_eur = alloc * pnl - 2 * commission * alloc
        equity += net_eur
        closed.append({**t,'exit':cl_final,'pnl_eur':round(net_eur,4),
                        'pnl_pct':round(pnl*100,3),'closed_by':'Einde','bar':len(rows)-1})

    return equity, closed

# ── Statistieken ──────────────────────────────────────────────────────────────
def stats(closed, start_cap, final_equity):
    if not closed: return {}
    df_t = pd.DataFrame(closed)
    wins = df_t[df_t['pnl_eur'] > 0]
    loss = df_t[df_t['pnl_eur'] <= 0]
    total = len(df_t)

    # Max gelijktijdige trades
    open_count = {}
    for t in closed:
        for b in range(t['bar'] - (t.get('bar',0) - t.get('bar',0)), t['bar']+1):
            open_count[b] = open_count.get(b, 0) + 1
    max_concurrent = max(open_count.values()) if open_count else 1

    # Max drawdown op equity curve
    eq = [start_cap]
    for _, row in df_t.iterrows():
        eq.append(eq[-1] + row['pnl_eur'])
    peak=eq[0]; max_dd=0
    for e in eq:
        if e>peak: peak=e
        dd=(peak-e)/peak*100
        if dd>max_dd: max_dd=dd

    pf = abs(wins['pnl_eur'].sum()/loss['pnl_eur'].sum()) if loss['pnl_eur'].sum()!=0 else 999

    by_dir   = df_t.groupby('dir').size().to_dict()
    by_close = df_t.groupby('closed_by').size().to_dict()

    return {
        'total': total,
        'wins':  len(wins),
        'losses':len(loss),
        'win_rate': round(len(wins)/total*100,1),
        'avg_win_eur':  round(wins['pnl_eur'].mean(),3)  if len(wins)  else 0,
        'avg_loss_eur': round(loss['pnl_eur'].mean(),3)  if len(loss)  else 0,
        'profit_factor': round(pf,2),
        'max_dd': round(max_dd,2),
        'max_concurrent': max_concurrent,
        'longs':  by_dir.get('long',0),
        'shorts': by_dir.get('short',0),
        'sl_hits':     by_close.get('SL/Trail',0),
        'winst_sluit': by_close.get('Winst-sluit',0),
        'final': round(final_equity,2),
        'return_pct': round((final_equity-start_cap)/start_cap*100,2)
    }

# ── Main ──────────────────────────────────────────────────────────────────────
PAIRS      = ['ETH/USDT','SOL/USDT','BTC/USDT','BNB/USDT']
START_DATE = '2026-01-01'
START_CAP  = 100

print(f"\n{'='*72}")
print(f"  PRECISION SNIPER  —  Multi-trade backtest")
print(f"  POSITIEVE trades sluiten bij nieuw signaal")
print(f"  NEGATIEVE trades blijven open tot ze positief zijn")
print(f"  20% kapitaal per trade | 15m | {START_DATE} | EUR {START_CAP}")
print(f"{'='*72}\n")

all_res = []

for symbol in PAIRS:
    try:
        df_raw = fetch(symbol, '15m', START_DATE)
        df_ind = calc_indicators(df_raw.copy())
        final_eq, closed = run(df_ind, start_cap=START_CAP)
        s = stats(closed, START_CAP, final_eq)
        if not s:
            print(f"  {symbol}: geen trades\n"); continue

        all_res.append({'Symbol':symbol, **s})
        tag = 'WINST  ' if final_eq > START_CAP else 'VERLIES'
        print(f"  {symbol}  [{tag}]")
        print(f"    EUR {START_CAP:.2f}  ->  EUR {s['final']:.2f}  ({s['return_pct']:+.2f}%)")
        print(f"    Trades: {s['total']}  (Long: {s['longs']}  Short: {s['shorts']})")
        print(f"    Win Rate: {s['win_rate']}%  |  Profit Factor: {s['profit_factor']}")
        print(f"    Max gelijktijdig open: {s['max_concurrent']}")
        print(f"    Gesloten via Winst-sluit: {s['winst_sluit']}  |  Via SL: {s['sl_hits']}")
        print(f"    Gem win: EUR {s['avg_win_eur']:.3f}  |  Gem verlies: EUR {s['avg_loss_eur']:.3f}")
        print(f"    Max Drawdown: {s['max_dd']}%")
        print()
    except Exception as e:
        import traceback
        print(f"  {symbol}: FOUT — {e}")
        traceback.print_exc()

if all_res:
    df_r = pd.DataFrame(all_res).sort_values('return_pct', ascending=False)
    print(f"{'='*72}")
    print("  OVERZICHT")
    print(f"{'='*72}")
    cols = ['Symbol','final','return_pct','win_rate','profit_factor','max_dd',
            'total','longs','shorts','max_concurrent','winst_sluit']
    print(df_r[cols].rename(columns={
        'final':'Eind EUR','return_pct':'Return%','win_rate':'WinRate%',
        'profit_factor':'PF','max_dd':'MaxDD%','total':'Trades',
        'longs':'Longs','shorts':'Shorts','max_concurrent':'MaxOpen',
        'winst_sluit':'WinstSluit'
    }).to_string(index=False))
    print(f"{'='*72}\n")
