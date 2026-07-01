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
2. `tracker.html` — Promise Tracker (130 promises, 123 broken)
3. `timeline.html` — Tijdlijn (incl. May 14–26 events)
4. `evidence.html` — directe quotes (uitgebreid t/m May 26)
5. `categories.html` — Categorieoverzicht
6. `investigation.html` — DL News onderzoek
7. `indicators.html` — Trust Score pagina (gauge, 4/100)
8. `petition.html` — Petitie met Firebase + blockchain TX verificatie
9. `sources.html` — 20 bronnen
10. `about.html` — Over de site + ideeënformulier
11. `admin.html` — Verborgen admin pagina (NIET in nav)
12. `social-cards.html` — Generator: download elke artikel-hero als PNG/SVG (NIET in nav, noindex)

## Social Cards Generator (social-cards.html)
- URL: https://blockdagexposed.com/social-cards.html (noindex, niet in nav)
- Toont alle artikelen uit articles.js als kaartjes met knoppen "Download PNG" en "Download SVG"
- PNG = 1600x1000, met watermerk blockdagexposed.com rechtsonder, kant en klaar voor X/Telegram/CMC
- Lost het fonts-probleem op: bij download worden Google Fonts vervangen door web-veilige tegenhangers (Newsreader→Georgia, DM Sans→Segoe UI, JetBrains Mono→Consolas) zodat SVG→PNG rasterisatie correct rendert
- Werkt lokaal (file://) en live, geen server-tools nodig (canvas toBlob in de browser)
- X accepteert geen SVG → gebruik daar de PNG. Per CMC-post beeld roteren tegen spam-detectie

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

## Data (data.js) — Huidige staat (June 16, 2026)
- 124 promises tracked (117 broken/misleading, 94.4% failure rate)
- Canonieke cijfers overal: 124 tracked, 117 broken, 94.4%, staking 117 dagen, 410,000+ berichten
- Aftersale price: **$0.00000012**. Legacy Sale price: **$0.00000044**, sell-tier **$0.05**
- Timeline events bijgewerkt t/m June 16 (188 events)
- Notable quotes bijgewerkt t/m June 16 (isNew op nieuwste June 13-16 quotes; oude isNew weggehaald)
- 20 bronnen
- Laatste artikelen: **article-network-down.html (June 16)**, article-presale-phish-flag.html (June 12), article-buyback-math.html (June 10, UPD June 11), article-claim-failed.html (June 9)

## Telegram analyse
- Geanalyseerd t/m: **16 juni 2026 10:26 UTC** (export: ChatExport_2026-06-16)
- Periode: 18 februari t/m 16 juni 2026
- Totaal berichten: 410,000+ (~5.400 nieuw op 13-16 juni)
- Gap: 20–30 april ontbreekt nog

## NIEUW (July 1): "BDAG AI IS NOW LIVE" + zelfverzonnen "+$500M valuation", terwijl 12 min later "AI is almost here" en de AI zelf BDAG een risico-microcap noemt (GEVERIFIEERD)
- Officieel kanaal 00:13: "🚀 BDAG AI Launched, valuation just jumped $500M USD! ... 1) BDAG AI IS NOW LIVE ... 2) 7,000 TPS upgrades ... 3) FINAL 24 HOURS $0.05 Buyback ends tomorrow ... 4) Coming in 2 weeks: BlockDAG Futures & Spot Exchange."
- **Directe tegenspraak**: 00:25 (12 min later) postte hetzelfde kanaal weer "BLOCKDAG AI LLM MODEL IS ALMOST HERE... final stage of preparation". Live én almost-here tegelijk.
- **De "AI" = chatbot op bdagai.io** ("Deep Think"). Gevraagd naar BDAG geeft hij een WAARSCHUWING: "micro-cap token with extreme price volatility, an uncapped supply structure, and limited liquidity", "not listed on major Tier-1", "a massive spread". Waarschijnlijk generieke LLM-wrapper. Foto: photo_41170@00-49.
- **$500M valuation is self-proclaimed**, niets erachter; markt daalde juist (CMC 24u en 1 week omlaag). William Griggs: "if valuation truly +$500M the price would be ~$0.005 not $0.00004, you overstate and under deliver." Paul: "self acclaimed valuation, nothing to back it up." Kevin K/Himayoon/Salty vroegen om bewijs, kregen niets.
- **TPS opgeblazen** 5.000 → 7.000. **Buyback nu "FINAL 24 HOURS ends tomorrow"** = zevende framing in 2 weken. **Eigen Futures + Spot Exchange "in 2 weken"** (STANS: "11 days") na de mislukte 30-juni listing.
- **RPC/staking "for weeks" plat**: nog steeds niet claimen/verkopen (Raja Dundi: Batch 5 claim RPC error). Jorge: "if you're not fixing RPC there's no way to close the buyback."
- **Nieuwe promise #130** (misleading). Telling nu **130/123 = 94,6%** (was 129/122). Nieuw artikel **article-ai-live-500m.html** + **social-ai-live-500m.svg** (og:image), eerste+isNew in articles.js. #128 reality aangevuld met July 1-twist. 4 nieuwe quotes, 1 timeline-event. Staking 132 dagen. Timeline 60 events/23 escalations.

## NIEUW (June 30): "$0.05 closes FOREVER Monday" werd OPNIEUW met 48u verlengd + dode LLM herrezen + beloofde 30-juni listing kwam niet (GEVERIFIEERD)
- Maandag (30 juni) was de "$0.05 closes FOREVER"-deadline. Sloot niets. Officieel kanaal postte om 01:37 (herhaald 06:50, 06:59, 09:56) "🚨 BlockDAG LLM MODEL LAUNCHING & 48H $0.05 BUYBACK EXTENSION ALERT" → zelfde buyback weer in een nieuwe 48u-countdown. **Zesde framing van één offer in twee weken** ($0.10 → $0.0005 → $0.02 → $0.01 → $0.05 "forever" → $0.05 "+48H").
- **Dode LLM herrezen**: de 25-juni "48u" ChatGPT/Claude-concurrent die nooit kwam staat nu als "BLOCKDAG AI LLM MODEL IS ALMOST HERE... final stage of preparation". Zelfde product, nieuwe "almost". #128 reality aangevuld met June 30-update.
- **30 juni was de beloofde listing/TGE datum** ($0.05). Geen listing, geen TGE, geen exchange-deposits (Paul: "The TGE is not happening today"). Op P2B "withdrawals still suspended after a week". Yuva vroeg expliciet naar de belofte, kreeg geen antwoord.
- **Direct Swap CLOSED** aangekondigd, terwijl de buyback-ad "BUY BDAG NOW" pusht ($0.00000044, "45X ROI").
- **RPC/staking 72u+ plat**: balances op nul in Trust Wallet/MetaMask, coins verdwenen. Officiële regel onveranderd.
- **Nieuwe promise #129** (broken). Telling nu **129/122 = 94,6%** (was 128/121/94,5%). Nieuw artikel **article-forever-extended.html** + **social-forever-extended.svg** (og:image), eerste+isNew in articles.js. 4 nieuwe quotes, 1 timeline-event (30 juni). Staking 131 dagen.

## NIEUW (June 27-29): sell-prijs loopt rond naar "$0.05 closes FOREVER" + RPC weer plat (GEVERIFIEERD)
- Inhaalslag (27, 28, 29 juni). **NIEUW BELEID: elke Dewi Schep krijgt voortaan een eigen los artikel** (zie [[feedback_daily_article]]). Vandaag: nieuw artikel **article-price-loop.html** (eigen hero-SVG + social-price-loop.svg + og:image) PLUS een gedateerd UPDATE-blok op article-price-chaos.html. **Geen nieuwe promise** ("$0.05 ends forever"-deadline is 30 juni, nog niet verstreken; rest is herhaling). Telling blijft 128/121 = 94.5%.
- **Volledige prijs-loop**: na $0.10 → $0.0005 → $0.02 → $0.01 nu terug op **$0.05**, geframed als "LESS THAN 72H: $0.05 BUYBACKS & SWAP END FOREVER on Monday" (30 juni). "24 HOUR COUNTDOWN" op 28 juni was op 29 juni nog steeds "24 HOUR COUNTDOWN".
- **RPC weer dagen plat** tijdens de sluitende deadline (net als 13-15 juni): admin "RPC is down, the team is working on updates". Houders konden niet claimen/verkopen; coins verdwijnen (Jordan: "Only blockdag miraculously vanished"). Cini18: "50Mio for $0.05 → only $458" (~0,018%).
- **LLM 48u (25 juni) BEVESTIGD GEBROKEN**: na 27 juni nooit meer genoemd, geen launch. #128 reality aangevuld.
- Staking 130 dagen, 452.000+ berichten. 4 nieuwe quotes, 1 timeline-event (27-29 juni).

## NIEUW (June 26): geen LLM, miners van "factory photos" naar "customs clearance" (GEVERIFIEERD)
- Voortzettingsdag → **gedateerd UPDATE-blok** op article-llm-48h.html, **geen nieuwe promise** (telling blijft 128/121 = 94.5%).
- **LLM**: de "48H"-aankondiging werd op 25 juni alleen maar herhaald; op 26 juni nog steeds geen LLM.
- **Miners schuiven weer**: 25 juni "official factory assembly photos" → 26 juni (08:46) "Miners are on the way. They're currently in customs clearance." Verzending nog steeds zonder datum; houders gepromised sinds okt 2025.
- **Buyback herverpakt**: "BATCH 7 CLOSING IN 24H + PRICE INCREASING" + dezelfde World Cup Bonus ($0.00000044 / $0.01 / 45X).
- Community (Vikram): "Miners are in hands of delivery boys... and then there's one more promo begins, and this happens again and again." Tap Miner-punten nog steeds niet geconverteerd (klachten N, Ibra).
- Staking 127 dagen, 443.000+ berichten. 3 nieuwe quotes, 1 timeline-event (26 juni).

## NIEUW (June 25): BlockDAG claimt ChatGPT/Claude-concurrent LLM binnen 48 uur te lanceren (GEVERIFIEERD)
- Distinct nieuw event → **nieuw artikel (article-llm-48h.html) + promise #128** (misleading). Telling nu **128 tracked, 121 broken = 94.5%** (percentage ongewijzigd).
- **Aankondiging (02:26)**: "BlockDAG Launching ChatGPT & Claude Competitor LLM Mode in 48H... a Large Language Model designed to compete with the biggest names in AI." Van een project dat nog geen miner, werkende explorer, staking-withdrawal of buyback-uitbetaling heeft geleverd.
- **Admin draait terug (08:11)**: "doesn't mean BlockDAG is suddenly trying to replace ChatGPT or Claude overnight... maybe simply another ecosystem feature."
- **5 updates totaal**: (1) LLM 48u, (2) World Cup Bonus "EXTENDED" (was "24H ONLY"), (3) miner "factory photos" (community: nep/komt niet overeen met sample X10), (4) Batch 7 "tomorrow" (alweer), (5) MiCA clarification.
- **Verificatie-discipline**: NIET geclaimd dat de factory-foto's nep zijn (kan niet bewijzen); gemeld dat community + admin ze niet onderschrijven, en "assembly ≠ shipping". Harde thesis = de LLM-48u claim zelf.
- Foto bruikbaar: photo_40644 ("MINER SHIPMENTS ARE STARTING · factory photos"). Nieuwe social card: social-llm-48h.svg + og:image.
- Staking 126 dagen, 440.000+ berichten. 3 nieuwe quotes, 1 timeline-event (25 juni).

## NIEUW (June 24): buyback wordt "World Cup Bonus" gimmick + nog steeds geen buyback-cijfers (GEVERIFIEERD)
- Voortzetting van de price-chaos story, dus **gedateerd UPDATE-blok** op article-price-chaos.html, **geen nieuwe promise** (telling blijft 127/120 = 94.5%).
- **Nieuwe promo (01:27)**: "24H ONLY WORLD CUP BONUS LIVE: 50% EXTRA BDAG + 45X ROI, BUY AT $0.00000044, SELL FOR $0.01." Landcode invoeren = bonus coins + dashboard-thema. Zelfde gecomprimeerde buyback, meer uitgifte + groter ROI-getal (45X). Officiële foto: photo_40605 (World Cup trophy graphic).
- **Nog steeds geen buyback-cijfers (02:53)**: admin "compiling and reviewing the relevant data... amounts completed and remaining will be provided shortly." Na weken nog geen bedrag.
- **Batch 7 claims "start tomorrow"** (alweer verschoven); miners weer "within the next 20 days".
- Community-feed vol bijna-identieke "World Cup hype" berichten (mogelijk astroturfing). Echte reactie (Mm): "change $0.00000044 to $0.00000022 and then discount football 50%."
- Staking 125 dagen, 436.000+ berichten. 3 nieuwe quotes, 1 timeline-event (24 juni).

## NIEUW (June 23): admin geeft toe dashboard-berekeningen "niet te kunnen verifieren of garanderen" (GEVERIFIEERD)
- Voortzetting van de price-chaos story, dus verwerkt als **gedateerd UPDATE-blok** op article-price-chaos.html, **geen nieuwe promise** (telling blijft 127/120 = 94.5%).
- **Admin-citaat (23 juni 05:38)**: "For Direct Buyback purchases, the team has emphasized a simpler structure with no compression. However, we are not in a position to independently verify or guarantee individual dashboard calculations." Dus de pagina die ze "the official source of record" noemen, staan ze zelf niet achter.
- **$0.05 prijs**: admin (06:17): "no specific dates have been confirmed." Batch 6 claims nog steeds "not confirmed".
- **Variabele tarief-nuance toegevoegd** aan het artikel + dashboard-bewijsbox: effectieve prijs verschilt per houder ($0.00025, $0.00005, $0.0000092 per coin), allemaal onder de geadverteerde prijs. (Belangrijk voor accuratesse: niet één vast "echte prijs" claimen.)
- Staking 124 dagen, 433.000+ berichten. 2 nieuwe quotes, 1 timeline-event (23 juni).

## NIEUW (June 20-22): drie verschillende sell-prijzen in 72 uur + "total invested" van dashboard verwijderd (GEVERIFIEERD)
- **Prijs-chaos**: officieel kanaal adverteerde in 72 uur minstens drie tegenstrijdige buyback sell-prijzen, soms dezelfde dag: "SELL AT $0.02" (buy $0.00000021), "SELL $0.01 / 30X ROI" (buy $0.00000044), én "SELL AT $0.0005" (buy $0.000024). Houders wisten niet welke gold.
- **Echte uitbetaling blijft fractie**: Ghost Buster verkocht 100M BDAG "voor 0.01" → dashboard $1.320 (~0,13%). Homer Sm: "the buyback price isn't 0.02, it's 0.000009."
- **"Total invested" van dashboard verwijderd** (admin-bevestigd, 20 juni): "the removal of certain dashboard information... the visibility of the total sales amount in the dashboard have been noted." Houders (valus, Yeshiwas) zagen transacties/miner-aankopen verdwijnen. İbrahim: "deliberate tactic... buy back at the lowest possible price."
- **Plus**: TPS-claim naar "5,500 TPS LIVE", "Regulated Exchange next month", "Batch 7 claims 23rd", Super App "August 20" alweer "postponed", Oct 1 payout via Super App (withdrawable onduidelijk).
- Promise #127 toegevoegd (misleading). Nieuw artikel: article-price-chaos.html. Telling nu **127 tracked, 120 broken = 94.5%** (rate van 94.4% naar 94.5%). Staking 123 dagen, 430.000+ berichten. (Inhaalslag: dekte 20, 21 én 22 juni; 19 juni was al gedaan.)

## NIEUW (June 19): de "$0.10 FINAL" sell verdween vóór de eigen deadline, vervangen door "Ultimate Sale" sell $0.0005 (GEVERIFIEERD)
- **Bait-and-switch**: de dagenlang gepushte "SELL AT $0.10, FINAL 48 HOURS" (deadline 20 juni) werd op 19 juni geschrapt en vervangen door een nieuwe "Ultimate Sale": "BUY AT $0.000024. SELL AT $0.0005 = 21X ROI! IT'S THAT SIMPLE." Geadverteerde sell-prijs stortte van $0.10 naar $0.0005 = 200x lager, overnight.
- **S P (00:15)**: "this morning buy at 0.00000044 and sell at 0.10 until 06-20-26... Now buying at 0.000024 and selling at 0.0005."
- **Wie al via $0.10 verkocht weet niet of hij betaald wordt**: pinned message verwijst nu alleen naar Ultimate Sale. Mr Gred: "is it mandatory to purchase the Ultimate Sale [to receive USDT]?" Maximilian Hänel + Paul: verwarring of legacy nog meetelt voor 1 oktober.
- **Nieuwe deadlines erbij gestapeld**: Super App "August 20th", miner deliveries "within the next 20 days" (Nde keer), BlockDAG Turbo listing "October 1st".
- Promise #126 toegevoegd (broken). Nieuw artikel: article-ultimate-sale.html. Telling nu 126 tracked, 119 broken (94.4%). Staking 120 dagen. Censuur gaat door: admin "if found fudding, the user will be banned permanently."

## NIEUW (June 18): de "FINAL 48 HOURS" countdown telt NIET af + admin noemt het zelf "marketing" (GEVERIFIEERD)
- **Countdown telt niet af**: exact dezelfde "FINAL 48 HOURS: $0.10 SELL OPTION CLOSING" post op 17 juni 04:37 én 18 juni 00:29 (vol etmaal later, nog steeds "48 hours"). Hercules M: "Final 48 hours should be till June 18, but on dashboard it says 20th of June." Thomas Peterfaj: "FINAL 24 / 48 / 72 / FINAL FINAL FINAL."
- **Admin noemt het zelf marketing**: "Marketing was good today, we are trying to build something sustainable." (18 juni 01:32)
- **Claimen/support/explorer nog stuk**: admin "keep trying until you successfully claim", "it should be rcp glitch, please keep trying", "website link to support is currently down."
- Verwerkt als **gedateerd UPDATE-blok** op article-final-price-moves.html (zelfde story als 17 juni, geen bijna-duplicaat). **Geen nieuwe promise** toegevoegd: telling blijft eerlijk op 125 tracked, 118 broken (94.4%). Staking 119 dagen. 2 timeline-events (17+18 juni nu compleet), 5 nieuwe quotes.

## NIEUW (June 17): "$0.05 FINAL" sell-prijs werd "$0.10" met nieuwe countdown + explorer plat (GEVERIFIEERD)
- **Bewegende "final" prijs**: 15 juni "SELL at $0.05, FINAL 72H" → 16 juni "24 HOURS ONLY: SELL AT $0.10 • TEST THE NEW 5,000 TPS LIVE" → 17 juni "FINAL 48 HOURS: $0.10 SELL OPTION CLOSING". Een "final" deadline die niet sluit maar terugkomt op een hoger getal met een verse klok. Allemaal uit hun eigen officiële kanaal.
- **Zelfde ~0.5% compressie**: hoger headline-getal verandert vrijwel niets. Tim Mc testte: 120M BDAG verkocht → dashboard $60.10K (= 0.5% van $0.10 × 120M = $12M). RCSoeiro: "before it was one price reduction after another; now it's one sell price increase after another."
- **Block explorer PLAT (admin-bevestigd, 17 juni)**: "I just checked and confirmed that it's not working... the team will fix the explorer asap." Houders (sahir, Vilphy, Jose Tirado) zien hun transfers/swaps niet op de explorer — vlak na de "5,000 TPS LIVE" claim, dus coins niet te verifiëren.
- **Koopprijs-mismatch**: berekend op $0.000088 i.p.v. geadverteerde $0.00000044. Admin: "a technical glitch... but the current price on your dashboard is the real price."
- Promise #125 toegevoegd (broken). Nieuw artikel: article-final-price-moves.html. Telling nu 125 tracked, 118 broken (94.4%). Staking 118 dagen.

## NIEUW (June 13-16): NETWERK LAG DAGEN PLAT tijdens buyback-deadline (GEVERIFIEERD)
- **BlockDAG-netwerk/RPC down ~13-15 juni**. Admin-bevestigd: "RPC is down until Tuesday, the BDAG network is down at the moment", "maintenance until Tuesday". Houders konden niet claimen/transferren/verkopen.
- **Botst met buyback-deadline**: officieel kanaal bleef "SELL AT $0.05, FINAL 72H/48H" pushen terwijl het netwerk plat lag. Maximilian Hänel: "rpc finished Tuesday but offer ends Monday. That's not great."
- **Coins verdwijnen uit wallets** (community): Honk Honk "the bdag I claimed to my binance wallet is gone"; Crypto King dashboard $23K→$5K. (community-reported)
- **Daarna**: "CHAIN UPGRADE COMPLETE: 5,000 TPS LIVE" (15 juni) — ironie: chain die 5.000 TPS adverteert lag dagen volledig onbereikbaar.
- Promise #124 toegevoegd (network outage, broken). Nieuw artikel: article-network-down.html.
- June 30 = zoveelste "final TGE" opnieuw bevestigd (14 juni). Miners "shipped in June" opnieuw.

## NIEUW (June 12): Etherscan PHISH/HACK flag op presale-deposit adres (GEVERIFIEERD, extern)
- **Adres 0x4C39Ed0438D5e8913aCF423db6d56CCe78B2d367** is op Etherscan getagd **"Blockdag Presale"** ÉN **"Phish / Hack"**, met waarschuwing "reports that this address was used in a Phishing scam. Reported by MetaMask."
- **Geverifieerd door mij** via WebFetch (etherscan toont het live) + onafhankelijk onderzoek (Jerry O'Callaghan, Medium nov 2025) dat dit adres door BlockDAG's EIGEN website als ETH deposit-adres werd gegeven. Saldo nu ~$175 (leeggehaald).
- **Eerlijke framing**: MetaMask's exacte rede is niet publiek; we claimen NIET dat het team zelf een phishing-scam runde, alleen dat het adres geflagd is. Iedereen kan het op Etherscan checken.
- **GEEN promise** (indicator), wel nieuw artikel **article-presale-phish-flag.html** + timeline + quote.
- **Compressie ontcijferd**: valus: "compress eligible BDAG to 99.5%, multiply result (0.5%) by buyback value = USDT shown." → payout ≈ 0.5% × headline-prijs.
- **15B coins teruggekocht vs $68M liquiditeit** (Rajesh: "do the math").
- **Staking weer DOWN** (113 dagen): "staking page not working", "error page", admin "up soon".

## NIEUW (June 11): sell-prijs naar $0.05, dashboard betaalt nog steeds een fractie
- **Sell-prijs nu $0.05** (was $0.03). Officiële FAQ: "Payout Currency: USDT, Single USDT Payment, offer ends Monday 6PM UTC". Prijsladder nu: $0.001→$0.01→$0.02→$0.005→$0.00025→$0.01→$0.03→**$0.05**.
- **Gat met dashboard groter**: Steven Boswell 283.8M → $56.77k (i.p.v. $11.3m, ~$0.0002); Thomas 130M → $32k (i.p.v. $5m). Effectieve prijs ~$0.0001-$0.0002.
- **Verkoop afgetrokken, niets betaald, geen hash**: één houder (05:46): "I received the confirmation. It didn't arrive at its destination. It didn't generate a hash and was deducted from my balance." → ernstige escalatie.
- **Community noemt het openlijk Ponzi** (Jeremy, Kurt: "where's that money coming from? 56x is not realistic").
- **Admin herschrijft geschiedenis**: "There was no fixed date for the launch" (09:56) — tegen het gedocumenteerde "100% guaranteed" record.
- **Verifieerbare marktdata** (CMC via community): market cap ~$3.14M, circulating ~79B van 102.7B minted, max supply 150B.
- Promise #123 toegevoegd. Artikel buyback-math KREEG GEDATEERD UPDATE-BLOK (geen duplicaat, conform [[feedback_verify_before_publish]]).

## NIEUW (June 10): geadverteerde $0.03 buyback vs dashboard ~$0.00015 + obligations > liquiditeit
- **Sell-prijs nu officieel $0.03** (buy $0.00000044), zoveelste "FINAL 24 HOURS" countdown. Prijsladder: $0.001→$0.01→$0.02→$0.005→$0.00025→$0.01→**$0.03**.
- **~200x gap**: houders melden dat het dashboard ~$0.00015 uitkeert, niet $0.03. İbrahim: "not at 0.30-0.01, but at 0.00015 per unit". Iemand: "320M tokens at $0.03 only $50k" (= ~$0.00015).
- **Committed volume overstijgt nu de ~$68.5M liquiditeit** (community-berekening, GEEN officiële disclosure): Darren Frost, Debin PT. Direct-send wallet ~5.94B BDAG ontvangen.
- **CAVEAT (eerlijk gelabeld)**: Debin PT betwist of die 4 wallets überhaupt buyback-wallets zijn ("old exchange-liquidity wallets") — als waar, dan nóg minder geoormerkt.
- **Claimen verergert**: coins gemarkeerd "claimed" maar niet ontvangen (G V, 三歲). "No claim went through in 7 hours."
- **2B burn zinloos**: supply op CMC ongewijzigd ~102B (Amir), circulating 70B+.
- Promise #122 toegevoegd. Nieuw artikel: article-buyback-math.html.

## NIEUW (June 9): claimen faalt breed — "transaction failed" (GEVERIFIEERD)
- **Claimen faalt over batches 1 t/m 6**: "Transaction likely to revert" / "Transaction failed". ~41 mislukkingsmeldingen in 2 dagen tegen een handvol bevestigde successen.
- **Regressie**: Jordan Romero claimde succesvol op de 6e, faalt nu (zelfde wallet) → wijst op contract-kant, niet wallet-setup.
- **Kova7 (verdediger!) postte zélf de fout**: "The problem persists in the claim for Batch 3" met het error-scherm. Sterkste bewijs.
- **De foutmelding lekt een developer debug-instructie naar eindgebruikers**: "Run node scripts/test-relayer-claim.js with a single address to debug" + verifieer merkle root / vesting contract balance.
- **BlockDAG's verweer**: "clear cache, RPC setup, many users have successfully claimed" — maar regressie + breedte + contract-checklist spreken dat tegen. Eerlijk benoemd in artikel.
- **Geclaimde coins zijn zwaar gecomprimeerd** (Clark): dashboard ≠ wallet ≠ verkoopbaar.
- Promise #121 toegevoegd (claim failure, broken). Nieuw artikel: article-claim-failed.html.

## GEVERIFIEERD deze ronde (extra zorgvuldig, na gezeik van gisteren)
- **10M minimum nu OFFICIEEL bevestigd** door admin (June 8 06:54: "if it states 10M is the minimum, transactions below may not qualify"). Was eerder alleen community.
- **LBank-storing was ECHT en is OPGELOST**: admin erkende ("we are working on LBank concern", June 8), community bevestigt fix (Homer Sm June 9: "working normally at LBANK"). Eerlijk als opgelost genoteerd (timeline note), niet als doorlopende freeze.
- **$68.5M wallet onafhankelijk gecorroboreerd** (P C en anderen noemen nu ook $68.5M).
- **Buyback receiving-wallet (BlockDAG chain) = 0x558999486d976ec2ddc18da9a97c7ccb78d9bd18**, ~4.6B BDAG ontvangen (SilentAlfa, bdagscan). Verplichting ~$34M aan $0.01 vs ~$68M op Tron.
- **Officiële RPC**: Chain ID 1404, rpc.bdagscan.com, explorer bdagscan.com.

## NIEUW (June 6-8): ~$68M in de buyback-wallets, maar geen contract en niemand betaald
- **"OVER 1 BILLION COINS SOLD IN THE BUYBACK PROGRAM"** (officieel kanaal June 6 16:42) — maar dat telt NIEUWE aankopen op $0.00000088, geen uitbetalingen. Niemand heeft gedocumenteerd betaald te zijn.
- **CORRECTIE (belangrijk)**: eerst stond op de site "wallet bevat ~$70k" (Nada's schatting). SilentAlfa (betrouwbare bron, corrigeerde eerder MEXC) traceerde de echte buyback-wallets op TronScan: **~$68M** over 4 adressen (TL1pfd...P8z $17.99M; TV8yRw...REU $15.51M; TXVDnR...y1C $19.98M; THKzqN...r2f $14.99M = $68.47M). Overal aangepast. De "$70k lege wallet" claim is VERWIJDERD.
- **Het echte verhaal (scherper)**: het geld staat er wél en is on-chain zichtbaar, MAAR er is GEEN smart contract, de keys zijn bij het team, custody is centraal, en ze betalen NU niet uit. SilentAlfa: "this does not guarantee anything since there is no smart contract and the control is centralized by the team and they have the keys. Why are they not paying now?" Zichtbaar ≠ veilig. Vraag verschuift van "kunnen ze betalen?" naar "waarom betalen ze niet?".
- **10 MILJOEN BDAG minimum** voor direct-send buyback — de meeste houders kunnen dat niet claimen. Bert Weekley: "Is anyone holding 10mil or more released? Only the ones that started this do."
- **"Robbing Peter to pay Paul"**: John Lombard: team neemt claim coins van de één, geeft ze aan de ander als claim.
- **Nieuw feit van SilentAlfa**: legacy buyback rekende effectief $0.00005 af (niet $0.01) of 200x compressie; direct-send 10M route was wél $0.01 zoals geadverteerd. (nog niet als losse promise, bewaren/overwegen)
- **BTSE/LBANK friction** (Homer Sm June 6) — NIET geverifieerd, alleen community-bericht; web toont juist hervattingen eerder in 2026. Overal als "community-reported, unverified" geframed.
- **June 30 = "final TGE" / Public Trading Launch** (admin June 7) — zoveelste finale datum; juni-aankopen nog niet claimbaar.
- **Casino API gooit 404** (CryptoTalkRadio, June): /casino/game-integration/open-game NotFoundException — mogelijk onbetaalde white-label vendor (niet bevestigd).
- Promises #119 ($68M wallets, geen contract, geen payout, broken) en #120 (10M minimum + June 30 final TGE, broken) toegevoegd
- **Artikel hernoemd-qua-inhoud**: article-buyback-empty-wallet.html (slug ongewijzigd) nu titel "buyback wallets hold $68 million... no smart contract, nobody paid"

## NIEUW (June 4-5): de CIRCULAIRE buyback + verdubbelde Legacy prijs
- **Buyback koopt alleen NIEUW gekochte tokens terug**. Om te kwalificeren moet je min. 10% van je oude balans in NIEUWE BDAG kopen, en alleen die nieuwe coins zijn verkoopbaar. Je oude presale BDAG kwalificeert NIET. Crypto Rich: "I purchased 107m BDAG yesterday to make me eligible, then the 107m I purchased was eligible to be sold right away."
- **Legacy Sale prijs VERDUBBELD in 24u**: $0.00000044 → $0.00000088 (June 5 00:29 UTC), nu gemarket als "56X ROI, 6 MONTHS." Nieuwe kopers buyback $0.01, bestaande houders $0.00025.
- **Dashboard toont NUL**: tientallen houders kochten specifiek voor de buyback en zien 0 eligible balance. Hillbilly Hitman: "Bought $250 today to try out the .01 buyback. It isn't working."
- **Kwalificatiedatum 3x verschoven**: eerst voor June 1, toen June 1+, nu alleen na June 3. Elke verschuiving maakt eerdere aankopen ongeldig → koop opnieuw.
- **De rekensom klopt niet**: STAS: 56M BDAG voor 42 USDT, buyback op 0.01 = 560,000 USDT. "Even a huge bank doesn't give you a profit like this for the 4 months period." Mark: "it's a complete lose for you, how will you give so much money to everyone?"
- Promises #117 (verdubbelde prijs/56X ROI, misleading) en #118 (circulaire buyback, broken) toegevoegd

## NIEUW (June 3-4): de buyback PRICE CUT bait-and-switch
- **LEGACY SALE + BUYBACK PROGRAM gelanceerd** (June 3 21:03 UTC). 9e distinct sales mechanism. Entry $0.00000044.
- **Buyback prijs 40x VERLAAGD NA registratie**: wie op $0.01 registreerde ziet nu $0.00025 op dashboard. jeremy: "the sell price has changed from $0.01 to $0.00025."
- **Twee tiers**: NIEUWE Legacy Sale kopers (op $0.00000044) krijgen $0.001 met "uncapped daily sell limits" en "no transfers required." BESTAANDE houders krijgen $0.00025 (4x minder).
- **Payout uitgesteld naar OKTOBER 1, 2026** — na een 48-uurs "FINAL HOURS" countdown. France аdola: "why was the countdown 44 hours and not 4 months?"
- **Admin geeft toe**: "Buyback prices are with a special limited time offer. It is not a fixed price." (June 3 21:41)
- **Om mee te doen**: stuur je al-geclaimde BDAG naar een buyback wallet en wacht 4 maanden voor payout in BDUSD
- De "buyback price" ladder in 18 dagen: $0.001 → $0.01 → $0.02 → $0.005 → $0.00025
- Promises #114-116 toegevoegd

## NIEUW (June 2-3): buyback bait-and-switch verergert
- **Buyback prijs HALVEERT per fase**: $0.02 (verlopen) → $0.01 (nu) → $0.005 (volgende fase). Marketing: "DOUBLE the buyback value is available right now!" Geen vaste floor, een countdown timer.
- **"You cannot sell as of now"** (admin June 3 10:00 UTC) — 3 dagen na de "June 1 buyback"
- **Verkopen uitgesteld naar June 30** (admin June 2 12:56: "You can sell only after that")
- **Payout calculation discrepancy**: Adriano Toledo meldt dashboard betaalt ~helft van de geadverteerde $0.01
- **Community consensus: payout in BDUSD niet USDT**. Szetto Raind: "Early investors will only be guinea pigs." Jamie: "give them another worthless token just to keep this presale going."
- Promises #111-113 toegevoegd

## NIEUW (June 1-2): de buyback BAIT-AND-SWITCH
- **De June 1 buyback is een REGISTRATIE FORMULIER, geen payout**. Admin 19:24 UTC: "You can't sell at the moment. You can only register for now and wait for further information."
- **Headline prijs van $0.001 naar $0.01** (10x marketing sprong) — maar alleen voor NIEUWE aankopen tijdens de 48u registratie window. Bestaande houders blijven op de lagere tier.
- **Payout in BDUSD, niet USDT** — BlockDAG's eigen "Beta" stablecoin (stablecoin.blockdag.network). Geen audit, geen reserve attestation, geen redemption pad gepubliceerd. Community Pedro: "Be careful, they're going to give you BDUSD, not USDT or USDC. Where will you exchange it?"
- **Exchange kopers EXPLICIET UITGESLOTEN** — admin 18:46 UTC: "Yes! Only purchase made from the official website will be eligible." Iedereen die op LBank/BitMart/Coinstore/BTSE/Poloniex kocht is uitgesloten.
- **$25M liquidity deployment** → "Liquidity will gradually be injected" (admin June 2 08:49)
- **Daily burns** → "Next burning event will be announced" (June 1 21:12)
- **Miners "this month JUNE"** voor de 9e datum verschuiving
- Sparks 10M TURBO JACKPOT als afleiding op de buyback dag

## NIEUW (May 30 - June 1):
- **Aftersale prijs gedropt naar $0.00000012** (May 31 15:55) — nieuwe low, "FINAL 24 HOURS" + "500X ROI" (echte math 8,333x)
- **9e "FINAL" deadline** van 2026 (May 7 casino, "no sale after May 7", Utility Presale "7 DAYS ONLY", TURBO "10 STAGES", buyback eligibility, burn, Batch 6 + lottery, May 31)
- **$25M liquidity deployment uitgesteld naar 30 juni** (community catch via O O: "doesn't inject until 06/30")
- **BlockDAG lobbyt CMC** om de supply data te wijzigen na de mislukte burn (admin May 31 04:27 + 23:55)
- **Op June 1 morgen UTC: niets gelanceerd** — geen stablecoin announcement, geen buyback activation, presale STILL selling
- Community: "Hehe another presale launched" (Xnova 101), "And they are still selling coins. Just shocking" (Wolf69), "Where is 0.001?" (James Bond)
- Staking 102 dagen broken. Miners "this month JUNE" (8e datumverschuiving). AMA 3 PM UTC June 1 op Binance Live (na export einde).

## NIEUW (May 28-29):
- **BlockDAG definieert eigen "ecosystem"** (May 29 09:00): "BDAG, TURBO, Casino & Gaming, Buyback, Sparks, Stablecoin". 4 van de 6 pijlers zijn gokproducten.
- **Sparks = volledige casino loyalty ladder** (May 28): Silver/Gold/Platinum/Diamond tiers (+2.5% tot +10% per win), 3-uurs "flash events" (dubbele punten). Loss-chasing mechaniek.
- **Admin ontkent ZachXBT onderzoek** expliciet (May 28 13:04): "we are not related to other projects" — geen transactie-bewijs. ZachXBT traceerde BlockDAG+ZKP presale fondsen via Ethereum→Tron, HTX/BTSE, naar Spartans casino hot wallet + influencer betalingen, met luxe auto's/horloges/vastgoed allegaties.
- **TURBO heeft "no timeline" en "roadmap yet to be released"** (admin May 28, 3 dagen na launch verkoop)
- **Big D community inzicht**: "controlled launch on cex only, the price was manufactured. Not the presale buyers."
- Staking 99 dagen broken. Vesting herbevestigd. Super App "coming soon" (Dex/staking/mining/nft op x1 app). Next AMA June 1.

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

## 9 sales mechanisms sinds 2024 (KRITIEKE LIJST)
1. Original presale (Batches 1-5) — March 2024
2. Aftersale — na "no sale after May 7" belofte
3. Live Swap — May 1, 2026 (closed May 20)
4. x10swap — May 6, 2026 (admin: "not a swap")
5. Utility Presale — May 8, 2026
6. BDAG Sparks (incl. chests) — May 14 (closed May 20, reopened May 23)
7. BlockDAG TURBO — May 25, 2026
8. Batch 6 — eind mei 2026
9. **Legacy Sale** — June 3, 2026, entry $0.00000044 → $0.00000088 (June 5). CURRENTLY LIVE

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
