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
2. `tracker.html` — Promise Tracker (92 promises, 84 broken)
3. `timeline.html` — Tijdlijn (incl. May 14–25 events)
4. `evidence.html` — directe quotes (uitgebreid t/m May 25)
5. `categories.html` — Categorieoverzicht
6. `investigation.html` — DL News onderzoek
7. `indicators.html` — Trust Score pagina (gauge, 4/100)
8. `petition.html` — Petitie met Firebase + blockchain TX verificatie
9. `sources.html` — 20 bronnen
10. `about.html` — Over de site + ideeënformulier
11. `admin.html` — Verborgen admin pagina (NIET in nav)

**Verwijderd:** `blockdag.html` — inhoud verhuisd naar homepage (later weer terug)

## Admin pagina
- URL: https://blockdagexposed.com/admin.html
- Wachtwoord: Holisan-1983
- Tabs: Petitie handtekeningen (incl. email + TX verificatie), Ideeën, Nieuwsbrief (Brevo link)

## Firebase (Firestore database)
- Project: blockdag-exposed
- Collections: `signatures` (petitie), `ideas` (about pagina), `comments` (artikel reacties)
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

## Data (data.js) — Huidige staat (May 25, 2026)
- 92 promises tracked (84 broken, 91.3% failure rate)
- Timeline events bijgewerkt t/m May 25
- Notable quotes bijgewerkt t/m May 25 (isNew op nieuwste May 23-25 quotes)
- 20 bronnen
- Laatste artikelen: **article-exchange-suspensions.html (May 25)**, article-burn-illusion.html (May 22), article-sparks-closed.html (May 21), article-casino-may19.html (May 20), is-blockdag-a-scam.html (landing page)

## Telegram analyse
- Geanalyseerd t/m: **25 mei 2026** (export: ChatExport_2026-05-25)
- Periode: 18 februari t/m 25 mei 2026
- Totaal berichten: 372,300+ (4,990 nieuw sinds laatste export op 22 mei)
- Gap: 20–30 april ontbreekt nog

## Bekende blockchain data
- BSC presale contract BlockDAG: 0xf0163C18F8D3fC8D5b4cA15e97D0F9f75460335F

## Actuele marktdata (May 25, 2026)
- BDAG prijs CMC: **$0.000069** (−99.86% vs $0.05)
- Market cap: $3.82M
- Circulating supply: **55.78B BDAG** (CMC self-reported volgens admin, "subjected to change")
- BDAG Aftersale prijs: **$0.00000019** (officieel, –99.99996% vs $0.05). Marketing: "400X ROI" (echte math: $0.00000019 → $0.001 = 5,263x). Lager dan $0.00000025 op 21 mei.
- **MEXC delisted BDAG** (May 24) — community confirmed, geen officieel statement van BlockDAG
- **BTSE suspended BDAG trading** (May 23) — admin: "Only the exchange admin can explain"
- **Vesting contract** (May 24): "After the previous claim, which was Batch 5, the vesting contract will be implemented" — nieuwe lock NA aankoop
- **Stable Coin launch June 1** — admin May 23, geen peg, geen backing, geen spec
- **$25M Live Liquidity Wallets** marketing (May 23): vijf June 1 producten op één datum (Buybacks, Stable Coin, Daily Burns, Liquidity Expansion, New Token Launches)
- **BDAG Sparks REOPENED met chest mechanic** (May 23-24) na sluiting May 20
- **Admin contradicts "listing phase"** (May 25 01:15): "BDAG is already launched and trading on exchanges" vs May 20: "We are still in listing phase"
- **CMC supply officieel "self reported"** (May 25 admin 06:10): "subjected to change. Check BDAG explorer"
- **Support ticket system BROKEN** sinds May 17 — "account suspended" errors. Admin May 24: "The support link is no longer working"
- 1B BDAG "BURN" (May 21) naar Ethereum dead address (0x0...0) op non-Ethereum chain. Circulating supply ging OMHOOG +1.54B same week.
- Batch 5 compression bevestigd: João Veríssimo paid 368,792,138 BDAG, kreeg 300,000 claimable = 99.92% compression (0.0814% delivery)
- x10swap officieel toegegeven door admin: "event-based USDT rewards after approved entries, not a fixed-price buyback program" (May 21)
- Exchange deposits indefinitely deferred (admin May 21: "once the ecosystem infrastructure is fully prepared")
- BDAG SPARKS GESLOTEN (May 20) → REOPENED (May 23 met chest gambling)
- CASINO DEPOSITS WERKEN NIET — Santiago: 1,250 BDAG, Analiz Radar: 10,000 BDAG missing
- Casino: vijf "live" claims gemist (May 7, 14, 15, 18, 19). Mei 19 "100M+ BDAG deposited" → 24h later −15.64%
- MetaMask warning door admin omschreven als "casual" (May 23-24 nog steeds)
- Buyback "300X ROI" (nu 400X) — cap van 250,000 BDAG per gebruiker (max $250 recovery)
- Miner verkoop GESTOPT (May 19): shipping "next month" (= juni) - admin May 24, 25
- Batch 1 claims INGETROKKEN (May 19)
- Wallet changing feature VERWIJDERD (May 18)
- x10swap: $40 entry fee, ~1 in 10 entries goedgekeurd, geen refund
- $213M Tether freeze op Kiziloz (Brazilië, May 14, gambling tax dispuut 2021–2024)
- BlockDAG heeft @blockdagmonitor geblokkeerd op X (May 19)
- Trader (May 24): "This group has already lost over 5,000 members"

## Belangrijke correcties gedaan
- BingX en Gate.io stonden als KEPT maar listings zijn NOOIT gebeurd → gecorrigeerd naar BROKEN (May 4, 2026)
- MEXC was als "in final stages" gemarkeerd, nu BROKEN (May 24)
- BTSE was als gelist gemarkeerd, nu BROKEN (May 23 suspension)

## Volgende deadlines om te monitoren
- $0.001 buyback start: **June 1, 2026** (250k cap, max $250 per user)
- Stable Coin launch: **June 1, 2026** (geen peg/backing/spec gepubliceerd)
- "$25M Liquidity Wallets" deployment: June 1, 2026
- Daily Burns programma: June 1, 2026
- Liquidity Expansion: June 1, 2026
- New Token Launches: June 1, 2026
- Vesting contract implementatie: na Batch 5 (geen datum)
- Casino full launch: geen nieuwe harde datum na vijf misses
- Miners shipping: "next month" = juni 2026 (zoveelste deadline)
- Brazilië/Kiziloz: appèl tegen $213M freeze loopt
- Staking: **95 dagen** broken sinds Feb 19, 2026
- Mainnet trading: June 30, 2026 (volgens Barry Moore via AMA referentie — quietly disappeared)
- Admin's "listing phase" → "full TGE" overgang: geen datum gegeven

## Vaste regels
1. Na elke wijziging in `blockdag-monitor/website/` altijd ook `docs/` updaten en pushen
2. Bij nieuwe promises/data alle hardcoded cijfers bijwerken in index.html en andere pagina's (tracker.html, trust.html, blockdag.html, is-blockdag-a-scam.html hebben eigen hardcoded tabellen los van data.js)
3. Geen streepjes (— of -) in tweets, CMC berichten of sociale media teksten
4. Twitter maximaal 280 tekens
5. CMC berichten maximaal 2000 tekens, GEEN URLs (laatste waarschuwing van CMC ontvangen)
6. "Dewi Schep" typen = volledige update: bronnen nalopen, nieuwe data toevoegen, cijfers bijwerken, PROJECT_STATUS.md updaten, pushen
7. Bij elke update: verwijder oude isNew vlaggen, zet alleen op nieuwste items
8. Na elke aanpassing PROJECT_STATUS.md bijwerken
9. Long-context replacements only — never pure-numeric bulk (corrupteert font-weight 600→100 etc.)

## Hoe verder te gaan in nieuwe chat
1. Open VS Code in map `c:\Users\yozga\Documents\Hakan\blockdag-exposed`
2. Start nieuwe chat met Claude Code
3. Zeg: "Lees PROJECT_STATUS.md voor context, dan gaan we verder"
4. Claude leest dit bestand en is direct bijgepraat
