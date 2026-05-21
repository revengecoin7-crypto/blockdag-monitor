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
2. `tracker.html` — Promise Tracker (68 promises, 60 broken)
3. `timeline.html` — Tijdlijn (incl. May 14–18 events)
4. `evidence.html` — directe quotes (uitgebreid met May 14–18)
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

## Data (data.js) — Huidige staat (May 21, 2026)
- 82 promises tracked (74 broken, ~90.2% failure rate)
- Timeline events bijgewerkt t/m May 21
- Notable quotes bijgewerkt t/m May 21
- 20 bronnen
- Laatste artikelen: article-casino-may19.html (May 20), article-blocked-on-x.html (May 19), article-buyback-cap.html (May 19), is-blockdag-a-scam.html (landing page)

## Telegram analyse
- Geanalyseerd t/m: **21 mei 2026** (export: ChatExport_2026-05-21)
- Periode: 18 februari t/m 21 mei 2026
- Totaal berichten: 365,234 (1,374 nieuw sinds laatste export)
- Gap: 20–30 april ontbreekt nog

## Bekende blockchain data
- BSC presale contract BlockDAG: 0xf0163C18F8D3fC8D5b4cA15e97D0F9f75460335F

## Actuele marktdata (May 21, 2026)
- BDAG prijs: **$0.00007224** (CMC, +5.8% bounce na de 15.64% dump, −99.86% vs $0.05)
- Market cap: $3.97M
- Circulating supply: 54.24B BDAG (36.17% van max 150B)
- BDAG Aftersale prijs **DALEDE** $0.0000003 → **$0.00000025** in 2 dagen (officieel, –99.9995% vs $0.05). Marketing: "350X ROI" (math fout, echte ratio naar $0.001 = 4,000x)
- **BDAG SPARKS GESLOTEN (May 20)** — gelanceerd May 14, dus 6 dagen later dicht. Live Swap ook gesloten.
- **CASINO DEPOSITS WERKEN NIET** — meerdere users melden missing tokens (Santiago: 1,250 BDAG, Analiz Radar: 10,000 BDAG). Community waarschuwing: "Do not send BDAG to the Casino section, it doesn't get credited."
- **Admin admit (May 20, 18:14 UTC):** "There's no information on compression rates" — actief verkopen met onbekend compression rate
- **Admin admit (May 20, 15:08 UTC):** "We are still in listing phase. Next will be price discovery and liquidity."
- **Admin defense narrative (May 21):** "long presale = good" / "transition phase from presale into full ecosystem rollout"
- Casino: vijf "live" claims gemist (May 7, 14, 15, 18, 19). Mei 19 "100M+ BDAG deposited" → 24h later −15.64%.
- Aftersale claims gedeferred naar "the last Batch" — geen datum
- MetaMask warning door admin omschreven als "casual" (May 20) — eigenlijk de Blockaid scam-flag
- Buyback "300X ROI" (nu 350X) — cap van 250,000 BDAG per gebruiker (max $250 recovery)
- Miner verkoop GESTOPT (May 19): "you might be able to purchase them from third party websites later"
- Batch 1 claims INGETROKKEN (May 19)
- Wallet changing feature VERWIJDERD (May 18)
- x10swap: $40 entry fee, ~1 in 10 entries goedgekeurd, geen refund
- $213M Tether freeze op Kiziloz (Brazilië, May 14, gambling tax dispuut 2021–2024)
- BlockDAG heeft @blockdagmonitor geblokkeerd op X (May 19)

## Belangrijke correcties gedaan
- BingX en Gate.io stonden als KEPT maar listings zijn NOOIT gebeurd → gecorrigeerd naar BROKEN (May 4, 2026)

## Volgende deadlines om te monitoren
- Batch 5 claims: **May 21, 2026 (donderdag)** — admin bevestigd via May 18 AMA
- $0.001 buyback start: June 1, 2026 (Promise 67 — 250k cap onthuld, budget/bron nog niet gepubliceerd)
- Casino full launch: geen nieuwe harde datum na vijf misses
- Miners: "June 2026" voor bestaande orders (zoveelste deadline), nieuwe verkoop gestopt
- Brazilië/Kiziloz: appèl tegen $213M freeze loopt
- Staking: **91 dagen** broken sinds Feb 19, 2026
- Mainnet trading: June 30, 2026 (volgens Barry Moore via AMA referentie)
- Admin's "listing phase" → "full TGE" overgang: geen datum gegeven

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


