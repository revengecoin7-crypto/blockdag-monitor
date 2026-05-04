"""
Break-Even Lock strategie backtest
- Entry: MACD zero cross (winnaar vorige backtest)
- Wanneer trade +5 pips in winst gaat: SL naar entry + 2 pips (gegarandeerd +2)
- TP varianten: 10 / 20 / 30 / 50 / 100 pips
- 1 pip = $1 voor ETH/USDT (bij ~$2000 prijs = 0.05%)
- Tijdfilter: ma-vr 09:00-21:00, za-zo 12:00-21:00 Amsterdam
- Periode: 2026-01-01 tot vandaag, 15m candles
"""
import ccxt
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import time
import warnings
warnings.filterwarnings('ignore')

# ── Data ──────────────────────────────────────────────────────────────────────
def fetch_full_history(symbol, timeframe, since_dt):
    exchange = ccxt.binance({'enableRateLimit': True})
    since_ms  = int(pd.Timestamp(since_dt).timestamp() * 1000)
    all_ohlcv = []
    print(f"  {symbol} {timeframe}...", end='', flush=True)
    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since_ms, limit=1000)
        if not ohlcv:
            break
        all_ohlcv.extend(ohlcv)
        last_ts = ohlcv[-1][0]
        if last_ts >= int(pd.Timestamp('now', tz='UTC').timestamp() * 1000):
            break
        since_ms = last_ts + 1
        print('.', end='', flush=True)
        time.sleep(0.08)
    print(f" {len(all_ohlcv)} candles")
    df = pd.DataFrame(all_ohlcv, columns=['timestamp','Open','High','Low','Close','Volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df[~df.index.duplicated()]

# ── Tijdfilter ────────────────────────────────────────────────────────────────
def in_trading_hours(ts):
    local = ts + pd.Timedelta(hours=2)
    h  = local.hour + local.minute / 60
    wd = local.weekday()
    return (9.0 <= h < 21.0) if wd < 5 else (12.0 <= h < 21.0)

# ── Indicatoren ───────────────────────────────────────────────────────────────
def macd_line(arr, fast=8, slow=21):
    s = pd.Series(arr)
    return (s.ewm(span=fast, adjust=False).mean() -
            s.ewm(span=slow, adjust=False).mean()).to_numpy()

# ── Break-Even Lock Strategy ─────────────────────────────────────────────────
class BreakEvenStrategy(Strategy):
    pip_size     = 1.0   # $1 per pip (ETH/USDT)
    trigger_pips = 5     # na hoeveel pips winst SL naar lock-in
    lock_pips    = 2     # SL komt op entry + 2 pips
    tp_pips      = 20    # take profit in pips (wordt aangepast per test)
    initial_sl   = 10    # initieel stop loss in pips

    def init(self):
        self.macd = self.I(macd_line, self.data.Close, 8, 21)
        # State per trade
        self._entry     = None
        self._sl        = None
        self._tp        = None
        self._locked    = False
        self._direction = None  # 'long' of 'short'

    def _open_long(self):
        ep = self.data.Close[-1]
        self._entry     = ep
        self._sl        = ep - self.initial_sl * self.pip_size
        self._tp        = ep + self.tp_pips    * self.pip_size
        self._locked    = False
        self._direction = 'long'
        self.buy(size=0.95)

    def _open_short(self):
        ep = self.data.Close[-1]
        self._entry     = ep
        self._sl        = ep + self.initial_sl * self.pip_size
        self._tp        = ep - self.tp_pips    * self.pip_size
        self._locked    = False
        self._direction = 'short'
        self.sell(size=0.95)

    def next(self):
        hi = self.data.High[-1]
        lo = self.data.Low[-1]

        # Beheer open positie
        if self.position:
            if self._direction == 'long':
                # Break-even lock: als high >= entry + trigger -> SL naar entry + lock
                if not self._locked and hi >= self._entry + self.trigger_pips * self.pip_size:
                    self._sl     = self._entry + self.lock_pips * self.pip_size
                    self._locked = True
                # Check SL hit (via low)
                if lo <= self._sl:
                    self.position.close()
                    self._direction = None
                    return
                # Check TP hit (via high)
                if hi >= self._tp:
                    self.position.close()
                    self._direction = None
                    return

            elif self._direction == 'short':
                # Break-even lock
                if not self._locked and lo <= self._entry - self.trigger_pips * self.pip_size:
                    self._sl     = self._entry - self.lock_pips * self.pip_size
                    self._locked = True
                # Check SL hit (via high)
                if hi >= self._sl:
                    self.position.close()
                    self._direction = None
                    return
                # Check TP hit (via low)
                if lo <= self._tp:
                    self.position.close()
                    self._direction = None
                    return
            return  # geen nieuwe entry als al in positie

        # Nieuwe entry: MACD zero cross + tijdfilter
        if not in_trading_hours(self.data.index[-1]):
            return

        if self.macd[-2] < 0 and self.macd[-1] >= 0:
            self._open_long()
        elif self.macd[-2] > 0 and self.macd[-1] <= 0:
            self._open_short()

# ── Runner ────────────────────────────────────────────────────────────────────
START_DATE   = '2026-01-01'
START_CAP    = 100
SIM_CAP      = 10_000
COMMISSION   = 0.001
SYMBOL       = 'ETH/USDT'
TP_LEVELS    = [10, 20, 30, 50, 100]

print(f"\n{'='*70}")
print(f"  BREAK-EVEN LOCK BACKTEST  |  {SYMBOL} 15m  |  EUR {START_CAP}")
print(f"  Trigger: +5 pips -> SL naar entry+2 pips  |  Initieel SL: 10 pips")
print(f"  1 pip = $1  |  Tijdfilter: ma-vr 09-21, za-zo 12-21 Amsterdam")
print(f"{'='*70}\n")

print(f"  Downloaden data...")
df = fetch_full_history(SYMBOL, '15m', START_DATE)

results = []

for tp in TP_LEVELS:
    BreakEvenStrategy.tp_pips = tp
    bt    = Backtest(df, BreakEvenStrategy, cash=SIM_CAP,
                     commission=COMMISSION, exclusive_orders=True)
    stats = bt.run()

    ret    = float(stats['Return [%]'])
    wr     = float(stats['Win Rate [%]'])    if not pd.isna(stats['Win Rate [%]'])    else 0.0
    sh     = float(stats['Sharpe Ratio'])    if not pd.isna(stats['Sharpe Ratio'])    else 0.0
    dd     = float(stats['Max. Drawdown [%]'])
    trades = int(stats['# Trades'])
    best   = float(stats['Best Trade [%]'])  if not pd.isna(stats['Best Trade [%]'])  else 0.0
    worst  = float(stats['Worst Trade [%]']) if not pd.isna(stats['Worst Trade [%]']) else 0.0
    avg    = float(stats['Avg. Trade [%]'])  if not pd.isna(stats['Avg. Trade [%]'])  else 0.0

    final     = round(START_CAP * (1 + ret / 100), 2)
    daily_ret = round(ret / 120, 3)  # 120 handelsdagen in 4 maanden

    results.append({
        'TP (pips)':      tp,
        'TP ($)':         f"${tp:.0f}",
        'Eind EUR':       final,
        'Return%':        round(ret, 2),
        'Dagelijks%':     daily_ret,
        'WinRate%':       round(wr, 1),
        'Sharpe':         round(sh, 3),
        'MaxDD%':         round(dd, 2),
        'Trades':         trades,
        'Beste trade%':   round(best, 2),
        'Slechtste%':     round(worst, 2),
        'Gem trade%':     round(avg, 3),
    })

    tag = "WINST  " if final > START_CAP else "VERLIES"
    print(f"  TP={tp:3d} pips (${tp:3d})  [{tag}]  EUR {final:7.2f}  ({ret:+7.2f}%)  "
          f"WR={wr:5.1f}%  Trades={trades:4d}  DD={dd:.1f}%  Gem={avg:+.3f}%/trade")

# ── Samenvatting ──────────────────────────────────────────────────────────────
df_r = pd.DataFrame(results)
print(f"\n{'='*70}")
print("  VOLLEDIGE VERGELIJKING")
print(f"{'='*70}")
print(df_r.to_string(index=False))

best_row = df_r.loc[df_r['Return%'].idxmax()]
print(f"\n  BESTE TP: {best_row['TP (pips)']} pips (${best_row['TP (pips)']})")
print(f"    EUR {START_CAP:.2f} -> EUR {best_row['Eind EUR']:.2f}  ({best_row['Return%']:+.2f}%)")
print(f"    Gemiddeld per dag: {best_row['Dagelijks%']:+.3f}%")
print(f"    Win Rate: {best_row['WinRate%']}%  |  Trades: {best_row['Trades']}  |  Max DD: {best_row['MaxDD%']}%")

# Langetermijn projectie op basis van beste TP
print(f"\n{'='*70}")
print(f"  LANGETERMIJN PROJECTIE met TP={best_row['TP (pips)']} pips")
print(f"  Gebaseerd op gemiddeld {best_row['Dagelijks%']:+.3f}% per dag")
print(f"{'='*70}")
dr = best_row['Return%'] / 120 / 100
for days in [30, 60, 90, 180, 365]:
    val = round(START_CAP * (1 + dr) ** days, 2)
    print(f"  Na {days:3d} dagen:  EUR {val:>10.2f}")

print(f"{'='*70}\n")
