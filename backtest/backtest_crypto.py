import ccxt
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import warnings
warnings.filterwarnings('ignore')

# ── Data fetcher (multiple pages for more history) ────────────────────────────
def fetch_ohlcv(symbol, timeframe, limit=1000):
    exchange = ccxt.binance({'enableRateLimit': True})
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# ── Indicator helpers ─────────────────────────────────────────────────────────
def ema(arr, n):
    return pd.Series(arr).ewm(span=n, adjust=False).mean().to_numpy()

def rsi(arr, n=14):
    s = pd.Series(arr)
    delta = s.diff()
    gain = delta.clip(lower=0).ewm(com=n-1, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(com=n-1, adjust=False).mean()
    rs = gain / loss
    return (100 - 100 / (1 + rs)).to_numpy()

def macd_line(arr, fast=12, slow=26):
    s = pd.Series(arr)
    return (s.ewm(span=fast, adjust=False).mean() - s.ewm(span=slow, adjust=False).mean()).to_numpy()

def macd_signal(arr, fast=12, slow=26, sig=9):
    ml = pd.Series(macd_line(arr, fast, slow))
    return ml.ewm(span=sig, adjust=False).mean().to_numpy()

def bb_upper(arr, n=20, k=2):
    s = pd.Series(arr)
    return (s.rolling(n).mean() + k * s.rolling(n).std()).to_numpy()

def bb_lower(arr, n=20, k=2):
    s = pd.Series(arr)
    return (s.rolling(n).mean() - k * s.rolling(n).std()).to_numpy()

def donchian_high(arr, n=20):
    return pd.Series(arr).rolling(n).max().to_numpy()

def donchian_low(arr, n=20):
    return pd.Series(arr).rolling(n).min().to_numpy()

def supertrend_dir(high, low, close, period=10, mult=3.0):
    high = pd.Series(high); low = pd.Series(low); close = pd.Series(close)
    hl2 = (high + low) / 2
    prev_close = close.shift()
    tr = pd.concat([high - low,
                    (high - prev_close).abs(),
                    (low  - prev_close).abs()], axis=1).max(axis=1)
    atr = tr.ewm(com=period-1, adjust=False).mean()
    basic_upper = hl2 + mult * atr
    basic_lower = hl2 - mult * atr

    final_upper = basic_upper.copy()
    final_lower = basic_lower.copy()
    direction   = pd.Series(np.nan, index=close.index)

    for i in range(period, len(close)):
        fu = basic_upper.iloc[i]
        fl = basic_lower.iloc[i]
        fu_prev = final_upper.iloc[i-1]
        fl_prev = final_lower.iloc[i-1]
        c_prev  = close.iloc[i-1]
        c_now   = close.iloc[i]

        final_upper.iloc[i] = fu if fu < fu_prev or c_prev > fu_prev else fu_prev
        final_lower.iloc[i] = fl if fl > fl_prev or c_prev < fl_prev else fl_prev

        if c_now > final_upper.iloc[i]:
            direction.iloc[i] = 1.0
        elif c_now < final_lower.iloc[i]:
            direction.iloc[i] = -1.0
        else:
            direction.iloc[i] = direction.iloc[i-1] if not pd.isna(direction.iloc[i-1]) else 0.0

    return direction.fillna(0).to_numpy()

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

# ── Strategies (fractional sizing so BTC works at any price) ─────────────────
SZ = 0.95  # use 95% of equity per trade

class EMA_Cross(Strategy):
    n1=9; n2=21
    def init(self):
        self.fast = self.I(ema, self.data.Close, self.n1)
        self.slow = self.I(ema, self.data.Close, self.n2)
    def next(self):
        if crossover(self.fast, self.slow):
            self.position.close(); self.buy(size=SZ)
        elif crossover(self.slow, self.fast):
            self.position.close(); self.sell(size=SZ)

class RSI_MACD(Strategy):
    def init(self):
        self.rsi  = self.I(rsi, self.data.Close, 14)
        self.macd = self.I(macd_line, self.data.Close)
        self.sig  = self.I(macd_signal, self.data.Close)
    def next(self):
        if self.rsi[-1] < 45 and crossover(self.macd, self.sig):
            self.position.close(); self.buy(size=SZ)
        elif self.rsi[-1] > 55 and crossover(self.sig, self.macd):
            self.position.close(); self.sell(size=SZ)

class BB_RSI(Strategy):
    def init(self):
        self.rsi   = self.I(rsi, self.data.Close, 14)
        self.upper = self.I(bb_upper, self.data.Close, 20, 2)
        self.lower = self.I(bb_lower, self.data.Close, 20, 2)
    def next(self):
        if self.data.Close[-1] < self.lower[-1] and self.rsi[-1] < 35:
            self.position.close(); self.buy(size=SZ)
        elif self.data.Close[-1] > self.upper[-1] and self.rsi[-1] > 65:
            self.position.close(); self.sell(size=SZ)

class Donchian(Strategy):
    n=20
    def init(self):
        self.dhi = self.I(donchian_high, self.data.Close, self.n)
        self.dlo = self.I(donchian_low,  self.data.Close, self.n)
    def next(self):
        if self.data.Close[-1] > self.dhi[-2]:
            self.position.close(); self.buy(size=SZ)
        elif self.data.Close[-1] < self.dlo[-2]:
            self.position.close(); self.sell(size=SZ)

class SuperTrend(Strategy):
    def init(self):
        self.dir = self.I(supertrend_dir, self.data.High, self.data.Low, self.data.Close, 10, 3.0)
    def next(self):
        if self.dir[-1] == 1 and self.dir[-2] != 1 and self.dir[-2] != 0:
            self.position.close(); self.buy(size=SZ)
        elif self.dir[-1] == -1 and self.dir[-2] != -1 and self.dir[-2] != 0:
            self.position.close(); self.sell(size=SZ)

class EMA_ADX(Strategy):
    def init(self):
        self.fast = self.I(ema, self.data.Close, 9)
        self.slow = self.I(ema, self.data.Close, 21)
        self.adx  = self.I(adx_series, self.data.High, self.data.Low, self.data.Close, 14)
    def next(self):
        if crossover(self.fast, self.slow) and self.adx[-1] > 20:
            self.position.close(); self.buy(size=SZ)
        elif crossover(self.slow, self.fast) and self.adx[-1] > 20:
            self.position.close(); self.sell(size=SZ)

class TripleEMA(Strategy):
    def init(self):
        self.e1 = self.I(ema, self.data.Close, 5)
        self.e2 = self.I(ema, self.data.Close, 13)
        self.e3 = self.I(ema, self.data.Close, 34)
    def next(self):
        if self.e1[-1] > self.e2[-1] > self.e3[-1] and crossover(self.e1, self.e2):
            self.position.close(); self.buy(size=SZ)
        elif self.e1[-1] < self.e2[-1] < self.e3[-1] and crossover(self.e2, self.e1):
            self.position.close(); self.sell(size=SZ)

class VWAP_RSI(Strategy):
    def init(self):
        tp = (self.data.High + self.data.Low + self.data.Close) / 3
        cumvol = np.cumsum(self.data.Volume)
        cumvwap = np.cumsum(tp * self.data.Volume)
        vwap_arr = cumvwap / cumvol
        self.vwap = self.I(lambda: vwap_arr)
        self.rsi  = self.I(rsi, self.data.Close, 14)
    def next(self):
        if self.data.Close[-1] > self.vwap[-1] and self.rsi[-1] < 60 and self.rsi[-2] < 40:
            self.position.close(); self.buy(size=SZ)
        elif self.data.Close[-1] < self.vwap[-1] and self.rsi[-1] > 40 and self.rsi[-2] > 60:
            self.position.close(); self.sell(size=SZ)

# ── Runner ────────────────────────────────────────────────────────────────────
STRATEGIES = {
    'EMA_Cross':  EMA_Cross,
    'RSI_MACD':   RSI_MACD,
    'BB_RSI':     BB_RSI,
    'Donchian':   Donchian,
    'SuperTrend': SuperTrend,
    'EMA_ADX':    EMA_ADX,
    'TripleEMA':  TripleEMA,
    'VWAP_RSI':   VWAP_RSI,
}

TIMEFRAMES = ['1m', '3m', '5m', '15m']
SYMBOLS    = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT']

results = []

print(f"\n{'='*80}")
print("  CRYPTO BACKTEST  |  8 Strategies × 4 Timeframes × 4 Symbols  |  Binance live data")
print(f"{'='*80}")

for symbol in SYMBOLS:
    print(f"\n>>> {symbol}")
    for tf in TIMEFRAMES:
        try:
            df = fetch_ohlcv(symbol, tf, limit=1000)
            for name, strat in STRATEGIES.items():
                try:
                    bt    = Backtest(df, strat, cash=100_000, commission=.001, exclusive_orders=True)
                    stats = bt.run()
                    ret   = round(float(stats['Return [%]']), 2)
                    wr    = round(float(stats['Win Rate [%]']), 1) if not pd.isna(stats['Win Rate [%]']) else 0.0
                    sh    = round(float(stats['Sharpe Ratio']),  3) if not pd.isna(stats['Sharpe Ratio'])  else 0.0
                    dd    = round(float(stats['Max. Drawdown [%]']), 2)
                    trades = int(stats['# Trades'])
                    results.append({'Symbol': symbol, 'Timeframe': tf, 'Strategy': name,
                                    'Return%': ret, 'WinRate%': wr, 'Sharpe': sh,
                                    'MaxDD%': dd, 'Trades': trades})
                    print(f"  [{tf:3s}] {name:<12} | Ret={ret:7.2f}% | WR={wr:5.1f}% | Sharpe={sh:7.3f} | DD={dd:7.2f}% | N={trades}")
                except Exception as e:
                    print(f"  [{tf:3s}] {name:<12} | ERROR: {e}")
        except Exception as e:
            print(f"  [{tf:3s}] FETCH ERROR: {e}")

# ── Summary ───────────────────────────────────────────────────────────────────
if results:
    df_r = pd.DataFrame(results)
    # Filter out 0-trade results
    df_r = df_r[df_r['Trades'] >= 5]

    print(f"\n{'='*80}")
    print("  TOP 15  —  Sharpe Ratio  (risk-adjusted, only >= 5 trades)")
    print(f"{'='*80}")
    cols = ['Symbol','Timeframe','Strategy','Return%','WinRate%','Sharpe','MaxDD%','Trades']
    top  = df_r.sort_values('Sharpe', ascending=False).head(15)
    print(top[cols].to_string(index=False))

    print(f"\n{'='*80}")
    print("  TOP 15  —  Return %")
    print(f"{'='*80}")
    top2 = df_r.sort_values('Return%', ascending=False).head(15)
    print(top2[cols].to_string(index=False))

    if not df_r.empty:
        best = df_r.loc[df_r['Sharpe'].idxmax()]
        print(f"\n{'='*80}")
        print(f"  WINNER:   {best['Strategy']}  |  {best['Symbol']}  |  {best['Timeframe']}")
        print(f"  Return:   {best['Return%']}%")
        print(f"  Win Rate: {best['WinRate%']}%")
        print(f"  Sharpe:   {best['Sharpe']}")
        print(f"  Max DD:   {best['MaxDD%']}%")
        print(f"  Trades:   {best['Trades']}")
        print(f"{'='*80}\n")
