"""
Backtest van de populairste TradingView strategieen
- 15m candles, Jan 1 2026 tot vandaag
- Tijdfilter: werkdagen 09:00-21:00, weekend 12:00-21:00 (Amsterdam = UTC+2)
- Long + Short
- Maximale trades
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

# ── Tijdfilter (Amsterdam UTC+2) ──────────────────────────────────────────────
def in_trading_hours(ts):
    local = ts + pd.Timedelta(hours=2)  # UTC -> Amsterdam (CEST)
    h = local.hour + local.minute / 60
    wd = local.weekday()  # 0=ma, 5=za, 6=zo
    if wd < 5:   # werkdag
        return 9.0 <= h < 21.0
    else:        # weekend
        return 12.0 <= h < 21.0

# ── Indicator functies ────────────────────────────────────────────────────────
def ema(a, n):
    return pd.Series(a).ewm(span=n, adjust=False).mean().to_numpy()

def sma(a, n):
    return pd.Series(a).rolling(n).mean().to_numpy()

def rsi(a, n=14):
    s = pd.Series(a)
    d = s.diff()
    g = d.clip(lower=0).ewm(com=n-1, adjust=False).mean()
    l = (-d.clip(upper=0)).ewm(com=n-1, adjust=False).mean()
    return (100 - 100/(1 + g/l)).to_numpy()

def macd_l(a, f=12, s=26):
    a = pd.Series(a)
    return (a.ewm(span=f,adjust=False).mean() - a.ewm(span=s,adjust=False).mean()).to_numpy()

def macd_sig(a, f=12, s=26, sig=9):
    return pd.Series(macd_l(a,f,s)).ewm(span=sig,adjust=False).mean().to_numpy()

def adx_s(hi, lo, cl, n=14):
    hi=pd.Series(hi); lo=pd.Series(lo); cl=pd.Series(cl)
    pc=cl.shift()
    tr=pd.concat([hi-lo,(hi-pc).abs(),(lo-pc).abs()],axis=1).max(axis=1)
    dp=(hi-hi.shift()).clip(lower=0); dm=(lo.shift()-lo).clip(lower=0)
    dp=dp.where(dp>dm,0); dm=dm.where(dm>dp,0)
    atr=tr.ewm(com=n-1,adjust=False).mean()
    dip=100*dp.ewm(com=n-1,adjust=False).mean()/atr
    dim=100*dm.ewm(com=n-1,adjust=False).mean()/atr
    dx=100*(dip-dim).abs()/(dip+dim+1e-9)
    return dx.ewm(com=n-1,adjust=False).mean().to_numpy()

def stoch_rsi(a, rsi_len=14, stoch_len=14, k=3, d=3):
    r = pd.Series(rsi(a, rsi_len))
    lo = r.rolling(stoch_len).min()
    hi = r.rolling(stoch_len).max()
    k_val = 100*(r-lo)/(hi-lo+1e-9)
    k_smooth = k_val.rolling(k).mean()
    d_smooth = k_smooth.rolling(d).mean()
    return k_smooth.to_numpy(), d_smooth.to_numpy()

def stoch_k(a, rsi_len=14, stoch_len=14, k=3, d=3):
    return stoch_rsi(a, rsi_len, stoch_len, k, d)[0]

def stoch_d(a, rsi_len=14, stoch_len=14, k=3, d=3):
    return stoch_rsi(a, rsi_len, stoch_len, k, d)[1]

def hma(a, n):
    s = pd.Series(a)
    half = s.ewm(span=n//2, adjust=False).mean()
    full = s.ewm(span=n,     adjust=False).mean()
    raw  = 2*half - full
    return raw.ewm(span=int(np.sqrt(n)), adjust=False).mean().to_numpy()

def bb_mid(a, n=20):
    return pd.Series(a).rolling(n).mean().to_numpy()

def bb_up(a, n=20, k=2):
    s=pd.Series(a); return (s.rolling(n).mean()+k*s.rolling(n).std()).to_numpy()

def bb_lo(a, n=20, k=2):
    s=pd.Series(a); return (s.rolling(n).mean()-k*s.rolling(n).std()).to_numpy()

def squeeze_mom(hi, lo, cl, bb_len=20, kc_mult=1.5, mom_len=12):
    hi=pd.Series(hi); lo=pd.Series(lo); cl=pd.Series(cl)
    bb_basis = cl.rolling(bb_len).mean()
    bb_dev   = cl.rolling(bb_len).std()
    kc_range = (hi-lo).rolling(bb_len).mean()
    sq_on    = (bb_basis - bb_dev*2 > bb_basis - kc_range*kc_mult) | \
               (bb_basis + bb_dev*2 < bb_basis + kc_range*kc_mult)
    highest = hi.rolling(mom_len).max()
    lowest  = lo.rolling(mom_len).min()
    delta   = cl - (highest+lowest)/2
    mom     = delta.rolling(mom_len).mean()
    return mom.to_numpy(), sq_on.to_numpy()

def sq_mom_val(hi, lo, cl, bb=20, kc=1.5, ml=12):
    return squeeze_mom(hi, lo, cl, bb, kc, ml)[0]

def atr_s(hi, lo, cl, n=14):
    hi=pd.Series(hi); lo=pd.Series(lo); cl=pd.Series(cl)
    tr=pd.concat([hi-lo,(hi-cl.shift()).abs(),(lo-cl.shift()).abs()],axis=1).max(axis=1)
    return tr.ewm(com=n-1,adjust=False).mean().to_numpy()

# ── Mixin voor tijdfilter ─────────────────────────────────────────────────────
SZ = 0.95

class TimedMixin:
    def _ok(self):
        return in_trading_hours(self.data.index[-1])

# ── Strategieen van TradingView ───────────────────────────────────────────────

# 1. EMA Cross (klassiek)
class S_EMA_Cross(TimedMixin, Strategy):
    n1=5; n2=13
    def init(self):
        self.f=self.I(ema,self.data.Close,self.n1)
        self.s=self.I(ema,self.data.Close,self.n2)
    def next(self):
        if not self._ok(): return
        if crossover(self.f,self.s): self.position.close(); self.buy(size=SZ)
        elif crossover(self.s,self.f): self.position.close(); self.sell(size=SZ)

# 2. EMA_ADX (Sovereign Trend / Nifty Alpha stijl)
class S_EMA_ADX(TimedMixin, Strategy):
    n1=9; n2=21; adx_thr=15
    def init(self):
        self.f=self.I(ema,self.data.Close,self.n1)
        self.s=self.I(ema,self.data.Close,self.n2)
        self.adx=self.I(adx_s,self.data.High,self.data.Low,self.data.Close,14)
    def next(self):
        if not self._ok(): return
        if crossover(self.f,self.s) and self.adx[-1]>self.adx_thr:
            self.position.close(); self.buy(size=SZ)
        elif crossover(self.s,self.f) and self.adx[-1]>self.adx_thr:
            self.position.close(); self.sell(size=SZ)

# 3. MACD + EMA200 (ADX/MACD/200 EMA Strawberry Signals stijl)
class S_MACD_EMA200(TimedMixin, Strategy):
    def init(self):
        self.macd=self.I(macd_l,self.data.Close,12,26)
        self.sig =self.I(macd_sig,self.data.Close,12,26,9)
        self.e200=self.I(ema,self.data.Close,200)
    def next(self):
        if not self._ok(): return
        above = self.data.Close[-1] > self.e200[-1]
        if crossover(self.macd,self.sig) and above:
            self.position.close(); self.buy(size=SZ)
        elif crossover(self.sig,self.macd) and not above:
            self.position.close(); self.sell(size=SZ)

# 4. Double MACD (55/89/1 trend + 13/21/1 entry)
class S_Double_MACD(TimedMixin, Strategy):
    def init(self):
        self.m_trend = self.I(macd_l,  self.data.Close,55,89)
        self.m_entry = self.I(macd_l,  self.data.Close,13,21)
        self.s_entry = self.I(macd_sig, self.data.Close,13,21,1)
    def next(self):
        if not self._ok(): return
        bull = self.m_trend[-1] > 0
        if crossover(self.m_entry,self.s_entry) and bull:
            self.position.close(); self.buy(size=SZ)
        elif crossover(self.s_entry,self.m_entry) and not bull:
            self.position.close(); self.sell(size=SZ)

# 5. RSI Midline (50 cross) - maximale frequentie
class S_RSI_50(TimedMixin, Strategy):
    rsi_len=10
    def init(self):
        self.r=self.I(rsi,self.data.Close,self.rsi_len)
    def next(self):
        if not self._ok(): return
        if self.r[-2]<50 and self.r[-1]>=50:
            self.position.close(); self.buy(size=SZ)
        elif self.r[-2]>50 and self.r[-1]<=50:
            self.position.close(); self.sell(size=SZ)

# 6. Tideflow VWAP-RSI stijl
class S_VWAP_RSI(TimedMixin, Strategy):
    def init(self):
        tp = (self.data.High+self.data.Low+self.data.Close)/3
        vwap = np.cumsum(tp*self.data.Volume)/np.cumsum(self.data.Volume)
        self.vwap=self.I(lambda: vwap)
        self.r=self.I(rsi,self.data.Close,14)
    def next(self):
        if not self._ok(): return
        above_vwap = self.data.Close[-1] > self.vwap[-1]
        if self.r[-2]<50 and self.r[-1]>=50 and above_vwap:
            self.position.close(); self.buy(size=SZ)
        elif self.r[-2]>50 and self.r[-1]<=50 and not above_vwap:
            self.position.close(); self.sell(size=SZ)

# 7. Stochastic RSI + EMA (Nifty Alpha Swing Bot stijl)
class S_StochRSI_EMA(TimedMixin, Strategy):
    def init(self):
        self.k=self.I(stoch_k,self.data.Close,14,14,3,3)
        self.d=self.I(stoch_d,self.data.Close,14,14,3,3)
        self.f=self.I(ema,self.data.Close,9)
        self.s=self.I(ema,self.data.Close,21)
    def next(self):
        if not self._ok(): return
        bull_ema = self.f[-1] > self.s[-1]
        if crossover(self.k,self.d) and self.k[-1]<80 and bull_ema:
            self.position.close(); self.buy(size=SZ)
        elif crossover(self.d,self.k) and self.k[-1]>20 and not bull_ema:
            self.position.close(); self.sell(size=SZ)

# 8. Hull MA Cross
class S_HMA_Cross(TimedMixin, Strategy):
    n1=9; n2=16
    def init(self):
        self.f=self.I(hma,self.data.Close,self.n1)
        self.s=self.I(hma,self.data.Close,self.n2)
    def next(self):
        if not self._ok(): return
        if crossover(self.f,self.s): self.position.close(); self.buy(size=SZ)
        elif crossover(self.s,self.f): self.position.close(); self.sell(size=SZ)

# 9. Squeeze Momentum (LazyBear stijl)
class S_Squeeze_Mom(TimedMixin, Strategy):
    def init(self):
        self.mom=self.I(sq_mom_val,self.data.High,self.data.Low,self.data.Close,20,1.5,12)
    def next(self):
        if not self._ok(): return
        if self.mom[-2]<0 and self.mom[-1]>=0:
            self.position.close(); self.buy(size=SZ)
        elif self.mom[-2]>0 and self.mom[-1]<=0:
            self.position.close(); self.sell(size=SZ)

# 10. Bollinger Band mean-reversion
class S_BB_Revert(TimedMixin, Strategy):
    def init(self):
        self.mid=self.I(bb_mid,self.data.Close,20)
        self.up =self.I(bb_up, self.data.Close,20,2)
        self.lo =self.I(bb_lo, self.data.Close,20,2)
        self.r  =self.I(rsi,self.data.Close,14)
    def next(self):
        if not self._ok(): return
        if self.data.Close[-1]<self.lo[-1] and self.r[-1]<40:
            self.position.close(); self.buy(size=SZ)
        elif self.data.Close[-1]>self.up[-1] and self.r[-1]>60:
            self.position.close(); self.sell(size=SZ)

# 11. Triple EMA (5/13/34) - snelle versie
class S_TripleEMA(TimedMixin, Strategy):
    def init(self):
        self.e1=self.I(ema,self.data.Close,5)
        self.e2=self.I(ema,self.data.Close,13)
        self.e3=self.I(ema,self.data.Close,34)
    def next(self):
        if not self._ok(): return
        if self.e1[-1]>self.e2[-1]>self.e3[-1] and crossover(self.e1,self.e2):
            self.position.close(); self.buy(size=SZ)
        elif self.e1[-1]<self.e2[-1]<self.e3[-1] and crossover(self.e2,self.e1):
            self.position.close(); self.sell(size=SZ)

# 12. MACD zero-cross (Adaptive MACD stijl)
class S_MACD_ZeroCross(TimedMixin, Strategy):
    def init(self):
        self.m=self.I(macd_l,self.data.Close,8,21)
    def next(self):
        if not self._ok(): return
        if self.m[-2]<0 and self.m[-1]>=0:
            self.position.close(); self.buy(size=SZ)
        elif self.m[-2]>0 and self.m[-1]<=0:
            self.position.close(); self.sell(size=SZ)

# 13. RSI extremen + EMA trend (Zen Momentum stijl)
class S_RSI_Extreme(TimedMixin, Strategy):
    def init(self):
        self.r=self.I(rsi,self.data.Close,14)
        self.t=self.I(ema,self.data.Close,50)
    def next(self):
        if not self._ok(): return
        bull = self.data.Close[-1] > self.t[-1]
        if self.r[-1]<35 and bull:
            self.position.close(); self.buy(size=SZ)
        elif self.r[-1]>65 and not bull:
            self.position.close(); self.sell(size=SZ)

# ── Runner ────────────────────────────────────────────────────────────────────
STRATEGIES = {
    '01_EMA_Cross':      S_EMA_Cross,
    '02_EMA_ADX':        S_EMA_ADX,
    '03_MACD_EMA200':    S_MACD_EMA200,
    '04_Double_MACD':    S_Double_MACD,
    '05_RSI_50cross':    S_RSI_50,
    '06_VWAP_RSI':       S_VWAP_RSI,
    '07_StochRSI_EMA':   S_StochRSI_EMA,
    '08_HMA_Cross':      S_HMA_Cross,
    '09_SqueezeMom':     S_Squeeze_Mom,
    '10_BB_Revert':      S_BB_Revert,
    '11_TripleEMA':      S_TripleEMA,
    '12_MACD_ZeroCross': S_MACD_ZeroCross,
    '13_RSI_Extreme':    S_RSI_Extreme,
}

START_DATE    = '2026-01-01'
START_CAP     = 100
SIM_CAP       = 10_000
COMMISSION    = 0.001
PAIRS         = ['ETH/USDT', 'SOL/USDT', 'BTC/USDT', 'BNB/USDT']

print(f"\n{'='*75}")
print(f"  13 TradingView Strategieen  |  15m  |  {START_DATE} tot vandaag")
print(f"  Uren: ma-vr 09:00-21:00, za-zo 12:00-21:00  |  EUR {START_CAP} start")
print(f"{'='*75}\n")

all_results = []

for symbol in PAIRS:
    print(f"\n>>> {symbol}")
    try:
        df = fetch_full_history(symbol, '15m', START_DATE)
    except Exception as e:
        print(f"  FETCH FOUT: {e}"); continue

    for name, strat in STRATEGIES.items():
        try:
            bt    = Backtest(df, strat, cash=SIM_CAP, commission=COMMISSION, exclusive_orders=True)
            stats = bt.run()
            ret   = float(stats['Return [%]'])
            wr    = float(stats['Win Rate [%]']) if not pd.isna(stats['Win Rate [%]']) else 0.0
            sh    = float(stats['Sharpe Ratio'])  if not pd.isna(stats['Sharpe Ratio'])  else 0.0
            dd    = float(stats['Max. Drawdown [%]'])
            tr    = int(stats['# Trades'])
            final = round(START_CAP * (1 + ret/100), 2)
            all_results.append({'Symbol':symbol,'Strategy':name,
                                 'EindEUR':final,'Return%':round(ret,2),
                                 'WinRate%':round(wr,1),'Sharpe':round(sh,3),
                                 'MaxDD%':round(dd,2),'Trades':tr})
            tag = 'WINST  ' if final > START_CAP else 'VERLIES'
            print(f"  [{tag}] {name:<22} | EUR {final:6.2f} ({ret:+6.2f}%) | WR={wr:4.1f}% | N={tr:4d}")
        except Exception as e:
            print(f"  [ERROR  ] {name:<22} | {e}")

# ── Samenvatting ──────────────────────────────────────────────────────────────
if all_results:
    df_r = pd.DataFrame(all_results)
    df_r = df_r[df_r['Trades'] >= 10]

    print(f"\n{'='*75}")
    print("  TOP 15  -  Return%  (minimaal 10 trades)")
    print(f"{'='*75}")
    cols=['Symbol','Strategy','EindEUR','Return%','WinRate%','Sharpe','MaxDD%','Trades']
    print(df_r.sort_values('Return%',ascending=False).head(15)[cols].to_string(index=False))

    print(f"\n{'='*75}")
    print("  TOP 15  -  Sharpe Ratio")
    print(f"{'='*75}")
    valid = df_r[df_r['Sharpe'] > 0]
    if not valid.empty:
        print(valid.sort_values('Sharpe',ascending=False).head(15)[cols].to_string(index=False))
    else:
        print("  Geen positieve Sharpe gevonden")

    best_ret    = df_r.sort_values('Return%',ascending=False).iloc[0]
    best_sharpe = (df_r[df_r['Sharpe']>0].sort_values('Sharpe',ascending=False).iloc[0]
                   if not df_r[df_r['Sharpe']>0].empty else best_ret)

    print(f"\n{'='*75}")
    print(f"  BESTE RETURN:  {best_ret['Strategy']}  op  {best_ret['Symbol']}")
    print(f"    EUR {START_CAP:.2f} -> EUR {best_ret['EindEUR']:.2f}  ({best_ret['Return%']:+.2f}%)")
    print(f"    Win Rate: {best_ret['WinRate%']}%  |  Trades: {best_ret['Trades']}  |  Max DD: {best_ret['MaxDD%']}%")
    print(f"\n  BESTE SHARPE:  {best_sharpe['Strategy']}  op  {best_sharpe['Symbol']}")
    print(f"    EUR {START_CAP:.2f} -> EUR {best_sharpe['EindEUR']:.2f}  ({best_sharpe['Return%']:+.2f}%)")
    print(f"    Win Rate: {best_sharpe['WinRate%']}%  |  Sharpe: {best_sharpe['Sharpe']}  |  Trades: {best_sharpe['Trades']}")
    print(f"{'='*75}\n")
