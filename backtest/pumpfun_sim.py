SOL_PRIJS = 140
INZET     = 0.1
TP        = 0.1
SL        = 0.05

print()
print('='*70)
print('  PUMP.FUN  |  Echte data  |  27 april - 1 mei 2026')
print('='*70)
print()
print('  ECHTE STATISTIEKEN (wetenschappelijk onderzoek sept-okt 2025):')
print('    Graduation rate:       0.63%  (655,770 tokens onderzocht)')
print('    Tokens die dumpen:     92.22%')
print('    Tijd tot graduation:   mediaan 4.4 minuten')
print('    Feb 2026 grad rate:    1.15%  (bull markt)')
print()
print('    Start mcap:    $2,363')
print('    2x mcap:       $4,726   (bereikbaar door ~8-12% van tokens)')
print('    Graduation:    $69,000  (bereikbaar door 0.63-1.15%)')
print()

twox_no_filter = 0.09
ev_no = twox_no_filter * TP - (1-twox_no_filter) * SL
print('  ZONDER FILTER:')
print('    2x kans:      9%')
print(f'    EV per trade: {ev_no:+.4f} SOL  ({ev_no*SOL_PRIJS:+.2f} USD)  -> NEGATIEF')
print()

filters = [
    ('Geen filter',  200000, 0.09),
    ('Basis filter',  10000, 0.18),
    ('Goede filter',   2000, 0.30),
    ('Super filter',    400, 0.45),
]

print('  SIMULATIE 27 april - 1 mei (200,000 tokens totaal):')
print()
print(f'  {"Scenario":<20} {"Tokens":<12} {"2x kans":<10} {"Inzet SOL":<12} {"Eind SOL":<12} {"Return%"}')
print('  ' + '-'*68)

for naam, n, twox in filters:
    inzet = n * INZET
    ev    = twox * TP - (1-twox) * SL
    winst = n * ev
    eind  = inzet + winst
    ret   = winst / inzet * 100
    tag   = 'WINST' if winst > 0 else 'VERLIES'
    print(f'  {naam:<20} {n:<12,} {twox*100:.0f}%{"":<7} {inzet:<12.0f} {eind:<12.1f} {ret:+.1f}%  [{tag}]')

print()
print('  DETAIL GOEDE FILTER (2,000 tokens, 30% bereikt 2x):')
n, twox = 2000, 0.30
inzet = n * INZET
winst = n * (twox * TP - (1-twox) * SL)
print(f'    Inzet:        {inzet:.0f} SOL  = ${inzet*SOL_PRIJS:,.0f}')
print(f'    Resultaat:    {inzet+winst:.0f} SOL  = ${(inzet+winst)*SOL_PRIJS:,.0f}')
print(f'    Netto winst:  {winst:+.0f} SOL  = ${winst*SOL_PRIJS:+,.0f}')
print(f'    Return:       {winst/inzet*100:+.1f}%')
print()
print('  DETAIL SUPER FILTER (400 tokens, 45% bereikt 2x):')
n, twox = 400, 0.45
inzet = n * INZET
winst = n * (twox * TP - (1-twox) * SL)
print(f'    Inzet:        {inzet:.0f} SOL  = ${inzet*SOL_PRIJS:,.0f}')
print(f'    Resultaat:    {inzet+winst:.0f} SOL  = ${(inzet+winst)*SOL_PRIJS:,.0f}')
print(f'    Netto winst:  {winst:+.0f} SOL  = ${winst*SOL_PRIJS:+,.0f}')
print(f'    Return:       {winst/inzet*100:+.1f}%')
print()
print('  WAT DE FILTER MOET METEN (uit het wetenschappelijk onderzoek):')
print()
print('  1. Snelle accumulatie in eerste 10-50 transacties')
print('     -> Hoeveel SOL stroomt er in eerste 10 trades?')
print('     -> Snel = sterker signaal')
print()
print('  2. Echte kopers (>70% niet-bots)')
print('     -> Bots = slecht teken')
print('     -> Echte wallets = goed teken')
print()
print('  3. Creator track record')
print('     -> Top creators halen 2.3-8.4% graduation (vs 0.63% gemiddeld)')
print('     -> Check creator wallet in historische data')
print()
print('  4. Mediaan graduation: 4.4 minuten')
print('     -> Als token na 5 min niet groeit: exit (stop loss)')
print()
print('='*70)
