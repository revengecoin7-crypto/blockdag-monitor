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

## Alle pagina's
1. `index.html` — Homepage (incl. About BlockDAG sectie met oprichters, presale, sponsorships)
2. `tracker.html` — Promise Tracker (59 promises)
3. `timeline.html` — Tijdlijn (66 events)
4. `evidence.html` — 38 directe quotes
5. `categories.html` — Categorieoverzicht
6. `investigation.html` — DL News onderzoek
7. `indicators.html` — Trust Score pagina (gauge, 5/100)
8. `petition.html` — Petitie met Firebase + blockchain TX verificatie
9. `sources.html` — 20 bronnen
10. `about.html` — Over de site + ideeënformulier
11. `admin.html` — Verborgen admin pagina (NIET in nav)

**Verwijderd:** `blockdag.html` — inhoud verhuisd naar homepage

## Admin pagina
- URL: https://blockdagexposed.com/admin.html
- Wachtwoord: Holisan-1983
- Tabs: Petitie handtekeningen (incl. email + TX verificatie), Ideeën, Nieuwsbrief (Brevo link)

## Firebase (Firestore database)
- Project: blockdag-exposed
- Collections: `signatures` (petitie), `ideas` (about pagina)
- apiKey: AIzaSyBkFwzdib2ewXvNf6YmgKvmfhMWt-8k6uw
- authDomain: blockdag-exposed.firebaseapp.com
- projectId: blockdag-exposed
- messagingSenderId: 867203959601
- appId: 1:867203959601:web:e31c472057f118f9aa3e10

## Nieuwsbrief
- Platform: Brevo (brevo.com), account: Blockdagexposed
- Beheer: https://app.brevo.com/contact/list

## Google Analytics
- Tag ID: G-J5YT0HDKHY (op alle pagina's)

## Google Search Console
- Geverifieerd via TXT record bij Namecheap
- Sitemap ingediend: https://blockdagexposed.com/sitemap.xml
- Site nog niet geïndexeerd (nieuw domein)
- Handmatig indexering aanvragen via URL-inspectie voor blockdag.html, petition.html, indicators.html

## Data (data.js) — Huidige staat
- 59 promises (34 broken, 19 misleading, 2 kept, 4 pending)
- 66 timeline events
- 38 notable quotes
- 20 bronnen
- Faalpercentage: 89.8%
- Laatste update: May 4, 2026

## Bekende blockchain data
- BSC presale contract BlockDAG: 0xf0163C18F8D3fC8D5b4cA15e97D0F9f75460335F

## Belangrijke correcties gedaan
- BingX en Gate.io stonden als KEPT maar listings zijn NOOIT gebeurd → gecorrigeerd naar BROKEN (May 4, 2026)

## Volgende deadlines om te monitoren
- Casino launch: May 7, 2026 (3 dagen weg op May 4)
- Batch 5 claims: mid-May 2026 (beloofd)
- Lending/borrowing: mid-May 2026 (beloofd)
- dApp dashboard: late May 2026 (beloofd)
- Miners: June-July 2026 (vijfde deadline)

## Vaste regels
1. Na elke wijziging in `blockdag-monitor/website/` altijd ook `docs/` updaten en pushen
2. Bij nieuwe promises/data alle hardcoded cijfers bijwerken in index.html en andere pagina's
3. Geen streepjes (— of -) in tweets, CMC berichten of sociale media teksten
4. Twitter maximaal 280 tekens
5. "Dewi Schep" typen = volledige update: bronnen nalopen, nieuwe data toevoegen, cijfers bijwerken, PROJECT_STATUS.md updaten, pushen
6. Bij elke update: verwijder oude isNew vlaggen, zet alleen op nieuwste items
7. Na elke aanpassing PROJECT_STATUS.md bijwerken

## Hoe verder te gaan in nieuwe chat
1. Open VS Code in map `c:\Users\yozga\Documents\Hakan\blockdag-exposed`
2. Start nieuwe chat met Claude Code
3. Zeg: "Lees PROJECT_STATUS.md voor context, dan gaan we verder"
4. Claude leest dit bestand en is direct bijgepraat
