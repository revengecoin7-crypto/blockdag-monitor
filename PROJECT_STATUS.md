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
2. `tracker.html` — Promise Tracker (95 promises, 87 broken)
3. `timeline.html` — Tijdlijn (incl. May 14–26 events)
4. `evidence.html` — directe quotes (uitgebreid t/m May 26)
5. `categories.html` — Categorieoverzicht
6. `investigation.html` — DL News onderzoek
7. `indicators.html` — Trust Score pagina (gauge, 4/100)
8. `petition.html` — Petitie met Firebase + blockchain TX verificatie
9. `sources.html` — 20 bronnen
10. `about.html` — Over de site + ideeënformulier
11. `admin.html` — Verborgen admin pagina (NIET in nav)

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

## Data (data.js) — Huidige staat (May 28, 2026)
- 99 promises tracked (92 broken/misleading = 67 broken + 25 misleading, 92.9% failure rate)
- LET OP: tracker.html telt nu "broken + misleading" samen als failures (92). Status verdeling: broken 67, misleading 25, kept 2, pending 3, promise 1, promised 1.
- Timeline events bijgewerkt t/m May 28 (TIMELINE_EVENTS = 149 entries)
- Notable quotes bijgewerkt t/m May 28 (isNew op nieuwste May 26-28 quotes) (NOTABLE_QUOTES = 206)
- 20 bronnen
- Laatste artikelen: **article-batch6-lottery.html (May 28)**, article-turbo-presale.html (May 26), article-exchange-suspensions.html (May 25), article-burn-illusion.html (May 22)

## Telegram analyse
- Geanalyseerd t/m: **28 mei 2026** (export: ChatExport_2026-05-28)
- Periode: 18 februari t/m 28 mei 2026
- Totaal berichten: 377,700+ (3,114 nieuw sinds laatste export op 26 mei)
- Gap: 20–30 april ontbreekt nog

## Bekende blockchain data
- BSC presale contract BlockDAG: 0xf0163C18F8D3fC8D5b4cA15e97D0F9f75460335F

## Actuele marktdata (May 26, 2026) — HUIDIGE STAAT
- BDAG prijs CMC: **$0.000069** (−99.86% vs $0.05)
- BDAG Aftersale prijs: **$0.00000019** (–99.99996% vs $0.05). Marketing: "400X ROI" (echte math: 5,263x)

## NIEUW (May 26-28):
- **"FINAL BATCH 6" + $10,000 USDT lottery** (May 26): "BUY BDAG NOW & WIN $10,000 USDT. FIRST 500 HOLDERS." Sweepstakes op een token sale. Batch 6 weerspreekt "presale ended Jan 26".
- **TURBO op de Sparks slot machine binnen 24u** (May 26): "spin to multiply 2X/10X/50X/100X". May 27: "$24,835 from a few spins". 5% referral commissie toegevoegd. De "utility token" heeft 1 gedemonstreerde functie: gokken.
- **Presale coins LOCKED tot June 30** tenzij promo code gebruikt (admin May 26): "If you bought BDAG during the presale but did not use a special code like TRADEMAY30 or FINALTRADE, your coins are locked until this date." Nooit verteld bij aankoop. De Feb "TGE compleet" is ongedaan gemaakt voor de meeste kopers.
- **Stablecoin tegenspraak**: marketing "OFFICIAL BDAG STABLE COIN" vs admin "The team is not creating a new token" / "USDT will be available as pegged token". 6 dagen voor launch onduidelijk of ze een stablecoin maken of USDT bridgen.
- **TURBO whitepaper pas DAG NA launch gepubliceerd** (May 26 20:35): blockdag.network/blockdag-turbo-whitepaper.pdf
- **Barry Moore (mod) openlijk vijandig** tegen community: "I don't argue with reta*ded" (May 27)
- **Super App "coming out soon"** (May 27)
- Staking 98 dagen broken. Support tickets nog steeds down.

## EERDER NIEUW (May 25-26):
- **BlockDAG TURBO PRESALE GELANCEERD** (May 25, 19:51 UTC): 7e distinct sales mechanism sinds 2024. Entry $0.0005, "launch" $0.04, "80X ROI", "ONLY 10 STAGES". Geen tokenomics, supply, vesting, contract, whitepaper of audit gepubliceerd. Community vijandig: T TriumphAnt "F Turbo F FOMO Until our network is working correctly." Edward Hernandez: "TURBO batch 1 phase 1 this one will extend for years enough is enough." Admin verdedigt: "BDAG is not bring abandon. Bdag turbo is a token under bdag ecosystem."
- **Admin geeft toe MEXC was nooit confirmed** (May 25 22:20 UTC): "Tier 1 exchanges is yet to be announced and team are still in discussions with MEXC team regarding listing." Eerste officiële admission dat 3 maanden marketing ("Major Tier 1 USA Exchange Secured" Feb 18) een leugen was.
- **Stablecoin onbevestigd door eigen admin** 6 dagen voor June 1 launch (May 25 19:31 UTC): "Not officially confirmed yet. If it launches as a stablecoin, it will likely be pegged around $1, but final details will be announced by the team."
- **Admin tegenspreekt "listing phase" lijn** (May 25 17:15 UTC): "BDAG is launched and trading on exchanges" — terwijl 5 uur later dezelfde admin handle MEXC nog "in discussions" noemt
- **Miners shipping "next month" = juni** (admin May 26 09:28): 7e datum verschuiving
- **Staking 96 dagen broken** sinds Feb 19, 2026

## Eerdere staat (May 22-25):
- MEXC cancelled scheduled BDAG listing before launch (May 24) — niet "delisted" want het was nooit live
- BTSE suspended actief trading (May 23) — admin "Only the exchange admin can explain"
- Vesting contract toegevoegd NA Batch 5 (admin May 24): nieuwe lock NA aankoop
- $25M Live Liquidity Wallets marketing (May 23): vijf June 1 producten op één datum
- BDAG Sparks REOPENED met chest mechanic (May 23-24) na sluiting May 20
- CMC supply officieel "self reported" (May 25 admin 06:10)
- Support ticket system BROKEN sinds May 17 — "account suspended" errors. 9+ dagen down
- 1B BDAG "BURN" (May 21) naar Ethereum dead address (0x0...0) op non-Ethereum chain. Circulating supply ging OMHOOG +1.54B same week
- Batch 5 compression bevestigd: João Veríssimo paid 368,792,138 BDAG, kreeg 300,000 claimable = 99.92% compression
- x10swap officieel toegegeven door admin als "event-based USDT rewards, not a fixed-price buyback program" (May 21)
- Exchange deposits indefinitely deferred (admin May 21)
- CASINO DEPOSITS WERKEN NIET — multiple users melden missing tokens
- Casino: vijf "live" claims gemist (May 7, 14, 15, 18, 19)
- Buyback "300X ROI" (nu 400X) — cap van 250,000 BDAG per gebruiker (max $250 recovery)
- Miner verkoop GESTOPT (May 19)
- Batch 1 claims INGETROKKEN (May 19)
- Wallet changing feature VERWIJDERD (May 18)
- x10swap: $40 entry fee, ~1 in 10 entries goedgekeurd, geen refund
- $213M Tether freeze op Kiziloz (Brazilië, May 14)
- BlockDAG heeft @blockdagmonitor geblokkeerd op X (May 19)
- Trader (May 24): "This group has already lost over 5,000 members"

## 7 sales mechanisms sinds 2024 (KRITIEKE LIJST)
1. Original presale (Batches 1-5) — March 2024
2. Aftersale — na "no sale after May 7" belofte
3. Live Swap — May 1, 2026 (closed May 20)
4. x10swap — May 6, 2026 (admin: "not a swap")
5. Utility Presale — May 8, 2026
6. BDAG Sparks (incl. chests) — May 14 (closed May 20, reopened May 23)
7. **BlockDAG TURBO** — May 25, 2026 (CURRENTLY LIVE)

## Belangrijke correcties gedaan
- BingX en Gate.io stonden als KEPT maar listings zijn NOOIT gebeurd → gecorrigeerd naar BROKEN (May 4, 2026)
- MEXC was als "in final stages" gemarkeerd, scheduled listing CANCELLED voor launch (May 24). Admin May 25 22:20 UTC bevestigt: "still in discussions" — listing was nooit geconfirmeerd.
- BTSE was als gelist gemarkeerd, nu BROKEN (May 23 suspension)

## Volgende deadlines om te monitoren
- **June 1, 2026**: $0.001 buyback (250k cap, max $250 per user)
- **June 1, 2026**: Stable Coin launch (geen peg/backing/spec gepubliceerd 6 dagen vooraf)
- **June 1, 2026**: $25M Liquidity Wallets deployment
- **June 1, 2026**: Daily Burns programma
- **June 1, 2026**: Liquidity Expansion
- **June 1, 2026**: New Token Launches
- **June 2026**: Miners shipping (7e datum)
- Vesting contract implementatie: na Batch 5 (geen datum)
- Casino full launch: geen nieuwe harde datum na vijf misses
- Brazilië/Kiziloz: appèl tegen $213M freeze loopt
- Staking: **96 dagen** broken sinds Feb 19, 2026
- BlockDAG TURBO: tokenomics/supply/vesting publicatie?

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
10. Cache busting: site.css?v=N, articles.js?v=N, data.js?v=N — bump bij elke update

## Hoe verder te gaan in nieuwe chat
1. Open VS Code in map `c:\Users\yozga\Documents\Hakan\blockdag-exposed`
2. Start nieuwe chat met Claude Code
3. Zeg: "Lees PROJECT_STATUS.md voor context, dan gaan we verder"
4. Claude leest dit bestand en is direct bijgepraat
