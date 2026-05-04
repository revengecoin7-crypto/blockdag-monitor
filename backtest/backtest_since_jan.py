import ccxt
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import time
import warnings
warnings.filterwarnings('ignore')

# ── Fetch full history from a start date ─────────────────────────────────────
def fetch_full_history(symbol, timeframe, since_dt):
    exchange = ccxt.binance({'enableRateLimit': True})
    since_ms  = int(pd.Timestamp(since_dt).timestamp() * 1000)
    all_ohlcv = []
    print(f"  Downloading {symbol} {timeframe} vanaf {since_dt}...", end='', flush=True)
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
        time.sleep(0.1)
    print(f" {len(all_ohlcv)} candles")
    df = pd.DataFrame(all_ohlcv, columns=['timestamp','Open','High','Low','Close','Volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df[~df.index.duplicated()]
    return df

# ── Indicators ────────────────────────────────────────────────────────────────
def ema(arr, n):
    return pd.Series(arr).ewm(span=n, adjust=False).mean().to_numpy()

def adx_series(high, low, close, n=14):
    high = pd.Series(high); low = pd.Series(low); close = pd.Series(close)
    prev_close = close.shift()
    tr = pd.concat([high - low,
                    (high - prev_close).abs(),
                    (low  - prev_close).abs()], axis=1).max(axis=1)
    dm_plus  = (high - high.shift()).clip(lower=0)
    dm_minus = (low.shift() - low).clip(lower=0)
    dm_plus  = dm_plus.where(dm_plus > dm_minus, 0)
    dm_minus = dm_minus.where(dm_minus > dm_plus, 0)
    atr   = tr.ewm(com=n-1, adjust=False).mean()
    dip   = 100 * dm_plus.ewm(com=n-1, adjust=False).mean() / atr
    dim   = 100 * dm_minus.ewm(com=n-1, adjust=False).mean() / atr
    dx    = 100 * (dip - dim).abs() / (dip + dim + 1e-9)
    return dx.ewm(com=n-1, adjust=False).mean().to_numpy()

# ── EMA_ADX Strategy ──────────────────────────────────────────────────────────
class EMA_ADX(Strategy):
    n_fast = 9
    n_slow = 21
    adx_threshold = 20

    def init(self):
        self.fast = self.I(ema, self.data.Close, self.n_fast)
        self.slow = self.I(ema, self.data.Close, self.n_slow)
        self.adx  = self.I(adx_series, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if crossover(self.fast, self.slow) and self.adx[-1] > self.adx_threshold:
            self.position.close()
            self.buy(size=0.95)
        elif crossover(self.slow, self.fast) and self.adx[-1] > self.adx_threshold:
            self.position.close()
            self.sell(size=0.95)

# ── Config ────────────────────────────────────────────────────────────────────
START_DATE     = '2026-01-01'
START_CAPITAL  = 100      # EUR (wat de gebruiker inlegt)
SIM_CAPITAL    = 10_000   # grotere sim zodat fractional units werken voor hoge-prijs coins
COMMISSION     = 0.001    # 0.1% per trade

PAIRS = ['ETH/USDT', 'SOL/USDT', 'BTC/USDT', 'BNB/USDT']

print(f"\n{'='*65}")
print(f"  EMA_ADX BACKTEST  |  {START_DATE} tot vandaag  |  start: EUR {START_CAPITAL}")
print(f"  Timeframe: 5m  |  Commissie: {COMMISSION*100}% per trade")
print(f"{'='*65}\n")

results = []

for symbol in PAIRS:
    try:
        df = fetch_full_history(symbol, '5m', START_DATE)
        bt    = Backtest(df, EMA_ADX, cash=SIM_CAPITAL, commission=COMMISSION, exclusive_orders=True)
        stats = bt.run()

        ret_pct_raw = float(stats['Return [%]'])
        final_eq    = round(START_CAPITAL * (1 + ret_pct_raw / 100), 2)
        ret_pct     = round(ret_pct_raw, 2)
        wr          = round(float(stats['Win Rate [%]']), 1) if not pd.isna(stats['Win Rate [%]']) else 0.0
        sharpe      = round(float(stats['Sharpe Ratio']),  3) if not pd.isna(stats['Sharpe Ratio'])  else 0.0
        dd          = round(float(stats['Max. Drawdown [%]']), 2)
        trades      = int(stats['# Trades'])
        best_t      = round(float(stats['Best Trade [%]']), 2) if not pd.isna(stats['Best Trade [%]']) else 0.0
        worst_t     = round(float(stats['Worst Trade [%]']), 2) if not pd.isna(stats['Worst Trade [%]']) else 0.0
        avg_t       = round(float(stats['Avg. Trade [%]']), 2) if not pd.isna(stats['Avg. Trade [%]']) else 0.0

        results.append({
            'Symbol': symbol,
            'Eind EUR': final_eq,
            'Return%': ret_pct,
            'WinRate%': wr,
            'Sharpe': sharpe,
            'MaxDD%': dd,
            'Trades': trades
        })

        winloss = 'WINST' if final_eq > START_CAPITAL else 'VERLIES'
        print(f"\n  {symbol}  [{winloss}]")
        print(f"    Start:        EUR {START_CAPITAL:.2f}")
        print(f"    Eind:         EUR {final_eq:.2f}  ({ret_pct:+.2f}%)")
        print(f"    Win Rate:     {wr}%")
        print(f"    Sharpe:       {sharpe}")
        print(f"    Max Drawdown: {dd}%")
        print(f"    Trades:       {trades}")
        if trades > 0:
            print(f"    Beste trade:  {best_t:+.2f}%  |  Slechtste: {worst_t:+.2f}%  |  Gem: {avg_t:+.2f}%")

    except Exception as e:
        print(f"\n  {symbol}: FOUT - {e}")

# ── Overzicht ─────────────────────────────────────────────────────────────────
if results:
    df_r = pd.DataFrame(results).sort_values('Return%', ascending=False)
    print(f"\n{'='*65}")
    print("  OVERZICHT  -  gesorteerd op rendement")
    print(f"{'='*65}")
    print(df_r[['Symbol','Eind EUR','Return%','WinRate%','Sharpe','MaxDD%','Trades']].to_string(index=False))

    best = df_r.iloc[0]
    print(f"\n  Beste pair:  {best['Symbol']}")
    print(f"  EUR {START_CAPITAL:.2f}  ->  EUR {best['Eind EUR']:.2f}  ({best['Return%']:+.2f}%)")
    print(f"{'='*65}\n")
