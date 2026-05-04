# BlockDAG Exposed — Project Status

## Live website
- URL: https://blockdagexposed.com
- GitHub repo: https://github.com/revengecoin7-crypto/blockdag-monitor
- Hosting: GitHub Pages (branch: main, folder: /docs)
- Domain gekocht bij: Namecheap

## Sociale media
- Twitter/X: https://x.com/blockdagmonitor
- Telegram: https://t.me/blockdagexposed

## Mapstructuur
- `blockdag-monitor/website/` — werkversie (hier aanpassingen maken)
- `docs/` — live versie voor GitHub Pages (altijd syncen na aanpassingen)
- Na elke wijziging: `cp blockdag-monitor/website/* docs/` + commit + push

## Pagina's op de website
1. `index.html` — Homepage met hero, metrics, countdown, vergelijkingstabel, recently added, watch list, nieuwsbrief
2. `tracker.html` — Alle promises (55 stuks), zoekbalk, filters, share knop per promise
3. `timeline.html` — Tijdlijn (60 events), nieuwste bovenaan
4. `evidence.html` — 38 directe quotes
5. `categories.html` — Categorieoverzicht met gekleurde kaarten
6. `investigation.html` — DL News onderzoek met verdict strip
7. `indicators.html` — Trust Score pagina (halvemaan gauge, 5/100)
8. `petition.html` — Petitie met Firebase + blockchain TX verificatie
9. `sources.html` — 20 bronnen
10. `about.html` — Over de site + ideeënformulier (Firebase)
11. `admin.html` — Verborgen admin pagina (NIET in nav)

## Admin pagina
- URL: https://blockdagexposed.com/admin.html
- Wachtwoord: Holisan-1983
- Toont: petitie handtekeningen (incl. email + TX verificatie), ideeën van about pagina, link naar Brevo voor nieuwsbrief

## Firebase (Firestore database)
- Project: blockdag-exposed
- Collections:
  - `signatures` — petitie handtekeningen
  - `ideas` — ideeën van about pagina
- Config:
  - apiKey: AIzaSyBkFwzdib2ewXvNf6YmgKvmfhMWt-8k6uw
  - authDomain: blockdag-exposed.firebaseapp.com
  - projectId: blockdag-exposed
  - messagingSenderId: 867203959601
  - appId: 1:867203959601:web:e31c472057f118f9aa3e10

## Nieuwsbrief
- Platform: Brevo (brevo.com)
- Account: Blockdagexposed
- Lijst: Your first list
- Beheer: https://app.brevo.com/contact/list

## Google Analytics
- Tag ID: G-J5YT0HDKHY
- Staat op alle pagina's

## Google Search Console
- Geverifieerd via TXT record
- Sitemap ingediend: https://blockdagexposed.com/sitemap.xml
- Site nog niet geïndexeerd (nieuw domein, duurt 1-4 weken)

## Data (data.js)
- 59 promises (33 broken, 19 misleading, 3 kept, 4 pending)
- 66 timeline events
- 38 notable quotes
- 20 bronnen
- Faalpercentage: 88.1%
- Laatste update: May 4, 2026

## Laatste Dewi Schep update (May 4, 2026)
Nieuwe toevoegingen:
- Promise 57: Binance listing May 7 misleading claim
- Promise 58: May 2026 3-fase roadmap (Batch 5, lending, dApp dashboard) pending
- 2 nieuwe timeline events (May 4): Binance claim headlines, May roadmap aankondiging
- Casino deadline May 7 nog 3 dagen weg
- Eerdere updates (May 1): Live Swap (56), 10 exchanges (55)

## Bekende blockchain data
- BSC presale contract BlockDAG: 0xf0163C18F8D3fC8D5b4cA15e97D0F9f75460335F
- Koper gebruikt BSC (BNB) voor aankoop

## Belangrijke regels bij werken aan dit project
1. Na elke wijziging in `blockdag-monitor/website/` altijd ook `docs/` updaten en pushen
2. Bij nieuwe promises/data altijd hardcoded cijfers bijwerken in index.html en andere pagina's
3. Geen streepjes (— of -) gebruiken in tweets, CMC berichten of andere sociale media teksten
4. Twitter heeft maximaal 280 tekens

## Wat nog gepland staat
- Community claim pagina met Firebase verificatie van walletadressen (gedeeltelijk gebouwd via petitie)
- Video scripts voor YouTube/TikTok

## Hoe verder te gaan op nieuwe computer
1. `git clone https://github.com/revengecoin7-crypto/blockdag-monitor.git`
2. Open de map in VS Code met Claude Code
3. Verwijs Claude naar dit bestand: "Lees PROJECT_STATUS.md voor context"
