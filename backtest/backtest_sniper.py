"""
Precision Sniper [WillyAlgoTrader] — aangepaste backtest
Extra logica: bij nieuw signaal, als huidige trade POSITIEF is -> sluit en open nieuw
              als huidige trade NEGATIEF is -> laat lopen (SL handelt het af), sla nieuw over
Geen tijdfilter. Alle trades 24/7. Periode: 2026-01-01 tot vandaag. 15m candles.
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
        batch = ex.fetch_ohlcv(symbol, tf, since=ms, limit=1000)
        if not batch: break
        out.extend(batch)
        last = batch[-1][0]
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
def calc_indicators(df, ema_fast=9, ema_slow=21, ema_trend=55,
                    rsi_len=13, atr_len=14, macd_f=12, macd_s=26, macd_sig=9):
    c = df['Close']; h = df['High']; l = df['Low']; v = df['Volume']

    df['ema_fast']  = c.ewm(span=ema_fast,  adjust=False).mean()
    df['ema_slow']  = c.ewm(span=ema_slow,  adjust=False).mean()
    df['ema_trend'] = c.ewm(span=ema_trend, adjust=False).mean()

    # RSI
    d = c.diff()
    g = d.clip(lower=0).ewm(com=rsi_len-1, adjust=False).mean()
    los = (-d.clip(upper=0)).ewm(com=rsi_len-1, adjust=False).mean()
    df['rsi'] = 100 - 100/(1 + g/los)

    # MACD
    ema_f = c.ewm(span=macd_f, adjust=False).mean()
    ema_s = c.ewm(span=macd_s, adjust=False).mean()
    macd  = ema_f - ema_s
    sig   = macd.ewm(span=macd_sig, adjust=False).mean()
    df['macd']      = macd
    df['macd_sig']  = sig
    df['macd_hist'] = macd - sig

    # ATR
    pc  = c.shift()
    tr  = pd.concat([h-l, (h-pc).abs(), (l-pc).abs()], axis=1).max(axis=1)
    df['atr'] = tr.ewm(com=atr_len-1, adjust=False).mean()

    # Volume SMA
    df['vol_sma'] = v.rolling(20).mean()
    df['vol_ok']  = v > df['vol_sma'] * 1.2

    # ADX / DI
    dp = (h - h.shift()).clip(lower=0)
    dm = (l.shift() - l).clip(lower=0)
    dp = dp.where(dp > dm, 0); dm = dm.where(dm > dp, 0)
    atr_s = tr.ewm(com=atr_len-1, adjust=False).mean()
    di_p  = 100 * dp.ewm(com=atr_len-1, adjust=False).mean() / atr_s
    di_m  = 100 * dm.ewm(com=atr_len-1, adjust=False).mean() / atr_s
    dx    = 100 * (di_p - di_m).abs() / (di_p + di_m + 1e-9)
    df['adx']    = dx.ewm(com=atr_len-1, adjust=False).mean()
    df['di_p']   = di_p
    df['di_m']   = di_m

    # VWAP (rolling dagelijks reset is complex, gebruik cumulatief)
    tp = (h + l + c) / 3
    df['vwap'] = (tp * v).cumsum() / v.cumsum()

    # Swing high/low (lookback=10)
    df['swing_low']  = l.rolling(10).min()
    df['swing_high'] = h.rolling(10).max()

    return df.dropna()

# ── Confluence score ──────────────────────────────────────────────────────────
def scores(row):
    ef=row['ema_fast']; es=row['ema_slow']; et=row['ema_trend']
    c=row['Close']; r=row['rsi']
    mh=row['macd_hist']; mv=row['macd']; ms=row['macd_sig']
    adx=row['adx']; dp=row['di_p']; dm=row['di_m']
    vwap=row['vwap']; vol=row['vol_ok']

    bull = 0.0
    bull += 1.0 if ef > es else 0
    bull += 1.0 if c  > et else 0
    bull += 1.0 if 50 < r < 75 else 0
    bull += 1.0 if mh > 0 else 0
    bull += 1.0 if mv > ms else 0
    bull += 1.0 if c  > vwap else 0
    bull += 1.0 if vol else 0
    bull += 1.0 if adx > 20 and dp > dm else 0
    bull += 0.5 if c  > ef else 0

    bear = 0.0
    bear += 1.0 if ef < es else 0
    bear += 1.0 if c  < et else 0
    bear += 1.0 if 25 < r < 50 else 0
    bear += 1.0 if mh < 0 else 0
    bear += 1.0 if mv < ms else 0
    bear += 1.0 if c  < vwap else 0
    bear += 1.0 if vol else 0
    bear += 1.0 if adx > 20 and dm > dp else 0
    bear += 0.5 if c  < ef else 0

    return bull, bear

# ── Handmatige backtest met aangepaste trade-logica ──────────────────────────
def run_backtest(df, start_capital=100, commission=0.001,
                 sl_mult=1.5, tp1_mult=1.0, tp2_mult=2.0, tp3_mult=3.0,
                 min_score=5.0):

    equity   = start_capital
    trades   = []

    # Huidige open trade state
    pos = None  # None = geen positie
    # pos = {
    #   'dir': 'long'/'short', 'entry': float, 'sl': float,
    #   'tp1': float, 'tp2': float, 'tp3': float,
    #   'risk': float, 'trail': float,
    #   'tp1_hit': bool, 'tp2_hit': bool, 'tp3_hit': bool,
    #   'entry_equity': float, 'bar': int
    # }

    last_dir = 0  # voorkomt dubbele signalen in dezelfde richting

    rows = df.reset_index()

    for i in range(1, len(rows)):
        row   = rows.iloc[i]
        prev  = rows.iloc[i-1]
        hi    = row['High']; lo = row['Low']; cl = row['Close']
        atr   = row['atr']

        ef  = row['ema_fast']; es = row['ema_slow']
        pef = prev['ema_fast']; pes = prev['ema_slow']
        r   = row['rsi']
        bs, be = scores(row)

        # EMA crossovers
        bull_cross = (pef < pes) and (ef >= es)
        bear_cross = (pef > pes) and (ef <= es)

        bull_mom = cl > ef and cl > es
        bear_mom = cl < ef and cl < es

        raw_buy  = bull_cross and bull_mom and r < 75 and bs >= min_score and last_dir != 1
        raw_sell = bear_cross and bear_mom and r > 25 and be >= min_score and last_dir != -1

        # ── Beheer open positie ──────────────────────────────────────────────
        if pos is not None:
            dir_ = pos['dir']
            profit_now = (cl - pos['entry']) if dir_ == 'long' else (pos['entry'] - cl)
            is_profit = profit_now > 0

            # Trail update
            if pos['tp1_hit'] and not pos['tp2_hit']:
                pos['trail'] = pos['entry']
            if pos['tp2_hit'] and not pos['tp3_hit']:
                pos['trail'] = pos['tp1']

            # TP hits
            if dir_ == 'long':
                if hi >= pos['tp1'] and not pos['tp1_hit']:
                    pos['tp1_hit'] = True; pos['trail'] = pos['entry']
                if hi >= pos['tp2'] and not pos['tp2_hit']:
                    pos['tp2_hit'] = True; pos['trail'] = pos['tp1']
                if hi >= pos['tp3'] and not pos['tp3_hit']:
                    pos['tp3_hit'] = True
            else:
                if lo <= pos['tp1'] and not pos['tp1_hit']:
                    pos['tp1_hit'] = True; pos['trail'] = pos['entry']
                if lo <= pos['tp2'] and not pos['tp2_hit']:
                    pos['tp2_hit'] = True; pos['trail'] = pos['tp1']
                if lo <= pos['tp3'] and not pos['tp3_hit']:
                    pos['tp3_hit'] = True

            # SL/Trail hit
            sl_hit = (lo <= pos['trail'] if dir_ == 'long' else hi >= pos['trail'])

            if sl_hit:
                exit_price = pos['trail']
                pnl_pct = ((exit_price - pos['entry']) / pos['entry']) if dir_ == 'long' \
                          else ((pos['entry'] - exit_price) / pos['entry'])
                net = pnl_pct - 2 * commission
                equity *= (1 + net)
                trades.append({
                    'dir': dir_, 'entry': pos['entry'], 'exit': exit_price,
                    'pnl_pct': round(net * 100, 3),
                    'tp1': pos['tp1_hit'], 'tp2': pos['tp2_hit'], 'tp3': pos['tp3_hit'],
                    'closed_by': 'SL/Trail', 'bar': i
                })
                last_dir = 0  # reset na SL zodat nieuwe signalen mogelijk zijn
                pos = None

            # ── Nieuw signaal terwijl positie open is ────────────────────────
            elif raw_buy or raw_sell:
                new_dir  = 'long' if raw_buy else 'short'
                is_opposite = (dir_ == 'long' and new_dir == 'short') or \
                              (dir_ == 'short' and new_dir == 'long')
                profit_now = (cl - pos['entry']) if dir_ == 'long' else (pos['entry'] - cl)
                in_profit  = profit_now > 0

                # Tegengesteld signaal -> ALTIJD sluiten en omdraaien (ook bij verlies)
                # Zelfde richting -> alleen sluiten als positief (reset TP/SL niveaus)
                should_close = is_opposite or in_profit

                if should_close:
                    exit_price = cl
                    pnl_pct = ((exit_price - pos['entry']) / pos['entry']) if dir_ == 'long' \
                              else ((pos['entry'] - exit_price) / pos['entry'])
                    net = pnl_pct - 2 * commission
                    equity *= (1 + net)
                    reden = 'Omdraaien (signaal)' if is_opposite else 'Nieuw signaal (winst)'
                    trades.append({
                        'dir': dir_, 'entry': pos['entry'], 'exit': exit_price,
                        'pnl_pct': round(net * 100, 3),
                        'tp1': pos['tp1_hit'], 'tp2': pos['tp2_hit'], 'tp3': pos['tp3_hit'],
                        'closed_by': reden, 'bar': i
                    })
                    pos = None
                    # Open nieuwe trade in nieuwe richting
                    if new_dir == 'long':
                        sl = max(row['swing_low'] - atr * 0.2, cl - atr * sl_mult)
                        risk = abs(cl - sl)
                        pos = {'dir':'long','entry':cl,'sl':sl,'trail':sl,
                               'tp1':cl+risk*tp1_mult,'tp2':cl+risk*tp2_mult,'tp3':cl+risk*tp3_mult,
                               'risk':risk,'tp1_hit':False,'tp2_hit':False,'tp3_hit':False,'bar':i}
                        last_dir = 1
                    else:
                        sl = min(row['swing_high'] + atr * 0.2, cl + atr * sl_mult)
                        risk = abs(cl - sl)
                        pos = {'dir':'short','entry':cl,'sl':sl,'trail':sl,
                               'tp1':cl-risk*tp1_mult,'tp2':cl-risk*tp2_mult,'tp3':cl-risk*tp3_mult,
                               'risk':risk,'tp1_hit':False,'tp2_hit':False,'tp3_hit':False,'bar':i}
                        last_dir = -1
                # Zelfde richting + verlies -> overslaan (niet opnieuw instappen in verliezende richting)

        # ── Geen open positie: open nieuwe trade ─────────────────────────────
        else:
            if raw_buy:
                sl   = max(row['swing_low'] - atr * 0.2, cl - atr * sl_mult)
                risk = abs(cl - sl)
                pos  = {'dir':'long','entry':cl,'sl':sl,'trail':sl,
                        'tp1':cl+risk*tp1_mult,'tp2':cl+risk*tp2_mult,'tp3':cl+risk*tp3_mult,
                        'risk':risk,'tp1_hit':False,'tp2_hit':False,'tp3_hit':False,'bar':i}
                last_dir = 1
            elif raw_sell:
                sl   = min(row['swing_high'] + atr * 0.2, cl + atr * sl_mult)
                risk = abs(cl - sl)
                pos  = {'dir':'short','entry':cl,'sl':sl,'trail':sl,
                        'tp1':cl-risk*tp1_mult,'tp2':cl-risk*tp2_mult,'tp3':cl-risk*tp3_mult,
                        'risk':risk,'tp1_hit':False,'tp2_hit':False,'tp3_hit':False,'bar':i}
                last_dir = -1

    # Sluit open positie aan einde
    if pos is not None and len(rows) > 0:
        cl_final = rows.iloc[-1]['Close']
        exit_price = cl_final
        dir_ = pos['dir']
        pnl_pct = ((exit_price - pos['entry']) / pos['entry']) if dir_ == 'long' \
                  else ((pos['entry'] - exit_price) / pos['entry'])
        net = pnl_pct - 2 * commission
        equity *= (1 + net)
        trades.append({
            'dir': dir_, 'entry': pos['entry'], 'exit': exit_price,
            'pnl_pct': round(net * 100, 3),
            'tp1': pos['tp1_hit'], 'tp2': pos['tp2_hit'], 'tp3': pos['tp3_hit'],
            'closed_by': 'Einde data', 'bar': len(rows)-1
        })

    return equity, trades

# ── Statistieken ──────────────────────────────────────────────────────────────
def stats(trades, start_cap, final_equity):
    if not trades:
        return {}
    df_t = pd.DataFrame(trades)
    wins = df_t[df_t['pnl_pct'] > 0]
    loss = df_t[df_t['pnl_pct'] <= 0]
    total = len(df_t)
    win_r = len(wins) / total * 100 if total else 0
    avg_w = wins['pnl_pct'].mean() if len(wins) else 0
    avg_l = loss['pnl_pct'].mean() if len(loss) else 0
    pf    = abs(wins['pnl_pct'].sum() / loss['pnl_pct'].sum()) if loss['pnl_pct'].sum() != 0 else 999
    tp1_r = df_t['tp1'].sum() / total * 100 if total else 0
    tp2_r = df_t['tp2'].sum() / total * 100 if total else 0
    tp3_r = df_t['tp3'].sum() / total * 100 if total else 0

    # Max drawdown
    eq_curve = [start_cap]
    for t in trades:
        eq_curve.append(eq_curve[-1] * (1 + t['pnl_pct']/100))
    peak = eq_curve[0]; max_dd = 0
    for e in eq_curve:
        if e > peak: peak = e
        dd = (peak - e) / peak * 100
        if dd > max_dd: max_dd = dd

    # Trades gesloten door "Nieuw signaal (winst)"
    by_signal  = df_t[df_t['closed_by'] == 'Nieuw signaal (winst)']
    by_flip    = df_t[df_t['closed_by'] == 'Omdraaien (signaal)']

    return {
        'trades': total, 'wins': len(wins), 'losses': len(loss),
        'win_rate': round(win_r, 1),
        'avg_win': round(avg_w, 3), 'avg_loss': round(avg_l, 3),
        'profit_factor': round(pf, 2),
        'max_dd': round(max_dd, 2),
        'tp1_rate': round(tp1_r, 1), 'tp2_rate': round(tp2_r, 1), 'tp3_rate': round(tp3_r, 1),
        'by_signal': len(by_signal), 'by_flip': len(by_flip),
        'final': round(final_equity, 2),
        'return_pct': round((final_equity - start_cap) / start_cap * 100, 2)
    }

# ── Main ──────────────────────────────────────────────────────────────────────
PAIRS      = ['ETH/USDT', 'SOL/USDT', 'BTC/USDT', 'BNB/USDT']
START_DATE = '2026-01-01'
START_CAP  = 100

print(f"\n{'='*72}")
print(f"  PRECISION SNIPER — Aangepaste backtest")
print(f"  Logica: sluit winnende trade bij nieuw signaal, laat verliezers lopen")
print(f"  Geen tijdfilter | 15m | {START_DATE} tot vandaag | EUR {START_CAP}")
print(f"{'='*72}\n")

all_results = []

for symbol in PAIRS:
    try:
        df_raw = fetch(symbol, '15m', START_DATE)
        df_ind = calc_indicators(df_raw.copy())
        final_eq, tr = run_backtest(df_ind, start_capital=START_CAP)
        s = stats(tr, START_CAP, final_eq)
        if not s:
            print(f"  {symbol}: geen trades")
            continue
        all_results.append({'Symbol': symbol, **s})
        tag = 'WINST  ' if final_eq > START_CAP else 'VERLIES'
        print(f"  {symbol} [{tag}]")
        print(f"    EUR {START_CAP:.2f} -> EUR {s['final']:.2f}  ({s['return_pct']:+.2f}%)")
        print(f"    Trades: {s['trades']}  |  Win Rate: {s['win_rate']}%  |  Profit Factor: {s['profit_factor']}")
        print(f"    Omgedraaid (tegengesteld signaal): {s['by_flip']} trades  |  Winst-sluit: {s['by_signal']} trades")
        print(f"    TP1: {s['tp1_rate']}%  TP2: {s['tp2_rate']}%  TP3: {s['tp3_rate']}%")
        print(f"    Gem win: +{s['avg_win']}%  |  Gem verlies: {s['avg_loss']}%  |  Max DD: {s['max_dd']}%")
        print()
    except Exception as e:
        print(f"  {symbol}: FOUT — {e}")
        import traceback; traceback.print_exc()

# ── Vergelijking ──────────────────────────────────────────────────────────────
if all_results:
    df_r = pd.DataFrame(all_results).sort_values('return_pct', ascending=False)
    print(f"{'='*72}")
    print("  OVERZICHT  —  gesorteerd op rendement")
    print(f"{'='*72}")
    cols = ['Symbol','final','return_pct','win_rate','profit_factor','max_dd','trades','by_signal']
    print(df_r[cols].rename(columns={
        'final':'Eind EUR','return_pct':'Return%','win_rate':'WinRate%',
        'profit_factor':'PF','max_dd':'MaxDD%','trades':'Trades',
        'by_signal':'WinSluit'
    }).to_string(index=False))

    best = df_r.iloc[0]
    print(f"\n  Beste pair: {best['Symbol']}")
    print(f"  EUR {START_CAP:.2f} -> EUR {best['final']:.2f}  ({best['return_pct']:+.2f}%)")
    print(f"{'='*72}\n")
