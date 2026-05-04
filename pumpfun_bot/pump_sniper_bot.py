"""
Pump.fun Super Filter Sniper Bot v2
Monitort nieuwe tokens via coin-info endpoint en stuurt Telegram alerts.
"""

import asyncio
import aiohttp
import time
import logging
from datetime import datetime

from telegram import Bot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)

# =============================================================================
# JOUW INSTELLINGEN
# =============================================================================
TELEGRAM_TOKEN = "8731475814:AAFB3amJgTJe2R-bCLCYZ3d6tUtWZRHWs3Q"
CHAT_ID        = "6172720508"

# =============================================================================
# SCHERPE FILTER  (veel minder maar veel betere signalen)
# =============================================================================
MIN_SOL_30S       = 3.0    # minimaal 3 SOL instroom in EERSTE 30 seconden
MIN_SOL_60S       = 5.0    # minimaal 5 SOL totaal na 60 seconden
MIN_MCAP_30S      = 5000   # mcap al boven $5k na 30 sec (echte interesse)
MIN_MCAP_GROEI    = 1.50   # mcap moet 50% gegroeid zijn tussen 30 en 60 sec
SOL_MAG_NIET_DALEN = True  # SOL reserves mogen NIET dalen (geen verkopers)

# Trade instellingen
INZET_SOL         = 0.1
TAKE_PROFIT       = 2.0
STOP_LOSS_MINUTEN = 3      # sneller stoppen: 3 min geen groei = exit

# Technisch
POLL_INTERVAL     = 5
API_BASE          = "https://frontend-api-v3.pump.fun"
# =============================================================================

seen_mints = set()


# ── API ───────────────────────────────────────────────────────────────────────

async def api_get(session, path):
    try:
        async with session.get(
            f"{API_BASE}{path}",
            timeout=aiohttp.ClientTimeout(total=10)
        ) as r:
            if r.status == 200:
                return await r.json()
    except Exception as e:
        log.debug(f"API fout {path}: {e}")
    return None


async def haal_nieuwe_tokens(session):
    data = await api_get(session,
        "/coins?offset=0&limit=50&sort=created_timestamp&order=DESC&includeNsfw=true")
    return data if isinstance(data, list) else []


async def haal_token_info(session, mint):
    return await api_get(session, f"/coins/{mint}")


async def haal_creator_stats(session, creator):
    data = await api_get(session,
        f"/coins?creator={creator}&limit=50&includeNsfw=true")
    if not isinstance(data, list):
        return 0, 0
    totaal    = len(data)
    graduated = sum(1 for c in data if c.get('complete', False))
    return totaal, graduated


# ── Super filter (via coin info) ──────────────────────────────────────────────

async def super_filter(session, token):
    mint       = token.get('mint', '')
    creator    = token.get('creator', '')
    naam       = token.get('name', '?')
    sol_start  = token.get('real_sol_reserves', 0) / 1e9
    res        = {}

    # ── Check na 30 seconden ─────────────────────────────────────────────────
    log.info(f"  [{naam}] check 1 na 30 sec...")
    await asyncio.sleep(30)

    info30 = await haal_token_info(session, mint)
    if not info30:
        res['reden'] = 'Token verdwenen'
        return None, res

    sol_30  = info30.get('real_sol_reserves', 0) / 1e9
    mcap_30 = info30.get('usd_market_cap', 0)
    sol_in  = sol_30 - sol_start
    res['sol_30'] = round(sol_30, 2)
    res['mcap_30'] = round(mcap_30, 0)

    # Check 1: Minimaal 3 SOL instroom in eerste 30 sec
    if sol_in < MIN_SOL_30S:
        res['reden'] = f'SOL 30s te laag: {sol_in:.2f} (min {MIN_SOL_30S})'
        return None, res

    # Check 2: Mcap al boven $5k na 30 sec
    if mcap_30 < MIN_MCAP_30S:
        res['reden'] = f'Mcap 30s te laag: ${mcap_30:.0f} (min ${MIN_MCAP_30S})'
        return None, res

    # ── Check na 60 seconden ─────────────────────────────────────────────────
    log.info(f"  [{naam}] check 2 na 60 sec...")
    await asyncio.sleep(30)

    info60  = await haal_token_info(session, mint)
    if not info60:
        res['reden'] = 'Token verdwenen bij check 2'
        return None, res

    sol_60  = info60.get('real_sol_reserves', 0) / 1e9
    mcap_60 = info60.get('usd_market_cap', 0)
    res['sol_60']  = round(sol_60, 2)
    res['mcap_60'] = round(mcap_60, 0)

    # Check 3: Minimaal 5 SOL totaal na 60 sec
    if sol_60 < MIN_SOL_60S:
        res['reden'] = f'SOL 60s te laag: {sol_60:.2f} (min {MIN_SOL_60S})'
        return None, res

    # Check 4: SOL mag niet gedaald zijn (mensen verkopen niet)
    if SOL_MAG_NIET_DALEN and sol_60 < sol_30 * 0.95:
        res['reden'] = f'SOL daalt: {sol_30:.2f} -> {sol_60:.2f} (verkopers!)'
        return None, res

    # Check 5: Mcap minimaal 50% gegroeid tussen 30 en 60 sec
    if mcap_30 > 0 and mcap_60 < mcap_30 * MIN_MCAP_GROEI:
        groei = mcap_60 / mcap_30 if mcap_30 > 0 else 0
        res['reden'] = f'Groei 30->60s te laag: {groei:.2f}x (min {MIN_MCAP_GROEI:.2f}x)'
        return None, res

    # ── Alle checks geslaagd ──────────────────────────────────────────────────
    c_totaal, c_grads = await haal_creator_stats(session, creator)
    res['creator_tokens']    = c_totaal
    res['creator_graduated'] = c_grads
    res['sol_instroom']      = round(sol_in, 2)
    res['geslaagd']          = True

    return info60, res


# ── Berichten ─────────────────────────────────────────────────────────────────

def bouw_koop_bericht(token, res):
    naam    = token.get('name', '?')
    symbol  = token.get('symbol', '?')
    mint    = token.get('mint', '')
    mcap    = res.get('mcap_60', 0)
    sol_in  = res.get('sol_instroom', 0)
    sol_60  = res.get('sol_60', 0)
    c_t     = res.get('creator_tokens', 0)
    c_g     = res.get('creator_graduated', 0)

    return (
        f"KOOPSIGNAAL\n\n"
        f"{naam} (${symbol})\n\n"
        f"Market Cap:        ${mcap:,.0f}\n"
        f"SOL instroom 30s:  {sol_in:.2f} SOL\n"
        f"SOL totaal 60s:    {sol_60:.2f} SOL\n"
        f"Creator:           {c_t} tokens, {c_g} graduated\n\n"
        f"Inzet:             {INZET_SOL} SOL\n"
        f"Take profit bij:   {INZET_SOL * TAKE_PROFIT:.2f} SOL (2x)\n"
        f"Stop loss na:      {STOP_LOSS_MINUTEN} min geen groei\n\n"
        f"Tijd: {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"Link: pump.fun/coin/{mint}"
    )


def bouw_exit_bericht(naam, symbol, mint, mcap_entry, mcap_nu, reden):
    mult  = mcap_nu / mcap_entry if mcap_entry > 0 else 1
    winst = INZET_SOL * (mult - 1)
    icon  = "VERKOPEN" if winst >= 0 else "STOPPEN"
    return (
        f"{icon}: {naam} (${symbol})\n\n"
        f"Multiplier:    {mult:.2f}x\n"
        f"Mcap nu:       ${mcap_nu:,.0f}\n"
        f"Resultaat:     {INZET_SOL:.2f} -> {INZET_SOL*mult:.3f} SOL\n"
        f"Winst/verlies: {winst:+.3f} SOL\n"
        f"Reden:         {reden}\n\n"
        f"Tijd: {datetime.now().strftime('%H:%M:%S')}\n"
        f"Link: pump.fun/coin/{mint}"
    )


# ── Exit monitor ──────────────────────────────────────────────────────────────

async def monitor_exit(bot, mint, naam, symbol, mcap_entry):
    start = time.time()
    async with aiohttp.ClientSession() as session:
        while True:
            await asyncio.sleep(30)
            verstreken = (time.time() - start) / 60
            token = await haal_token_info(session, mint)
            if not token:
                continue
            mcap_nu = token.get('usd_market_cap', 0)
            mult    = mcap_nu / mcap_entry if mcap_entry > 0 else 1

            if mult >= TAKE_PROFIT:
                await bot.send_message(chat_id=CHAT_ID,
                    text=bouw_exit_bericht(naam, symbol, mint, mcap_entry, mcap_nu,
                                          "Take profit bereikt!"))
                log.info(f"TAKE PROFIT: {naam} {mult:.2f}x")
                break

            if verstreken >= STOP_LOSS_MINUTEN and mult < 1.15:
                await bot.send_message(chat_id=CHAT_ID,
                    text=bouw_exit_bericht(naam, symbol, mint, mcap_entry, mcap_nu,
                                          f"{STOP_LOSS_MINUTEN} min geen groei"))
                log.info(f"STOP LOSS: {naam}")
                break

            if verstreken > 60:
                break


# ── Analyse ───────────────────────────────────────────────────────────────────

async def analyseer_token(bot, session, token):
    naam   = token.get('name', '?')
    symbol = token.get('symbol', '?')
    mint   = token.get('mint', '')

    log.info(f"Analyseer: {naam} ({symbol})")
    try:
        resultaat, scores = await super_filter(session, token)
        if resultaat:
            await bot.send_message(chat_id=CHAT_ID,
                text=bouw_koop_bericht(resultaat, scores))
            log.info(f"SIGNAAL VERZONDEN: {naam}")
            mcap_entry = scores.get('mcap_60', token.get('usd_market_cap', 0))
            asyncio.create_task(monitor_exit(bot, mint, naam, symbol, mcap_entry))
        else:
            log.info(f"Afgewezen: {naam}  ({scores.get('reden', '?')})")
    except Exception as e:
        log.error(f"Fout bij {naam}: {e}")


# ── Hoofdloop ─────────────────────────────────────────────────────────────────

async def monitor_loop(bot):
    log.info("Monitor gestart...")
    async with aiohttp.ClientSession() as session:
        bestaand = await haal_nieuwe_tokens(session)
        for t in bestaand:
            seen_mints.add(t.get('mint', ''))
        log.info(f"{len(seen_mints)} bestaande tokens geladen")

        while True:
            try:
                tokens = await haal_nieuwe_tokens(session)
                nieuw  = [t for t in tokens if t.get('mint') not in seen_mints]
                for t in nieuw:
                    seen_mints.add(t.get('mint', ''))
                    asyncio.create_task(analyseer_token(bot, session, t))
                if nieuw:
                    log.info(f"{len(nieuw)} nieuwe token(s)")
            except Exception as e:
                log.error(f"Monitor fout: {e}")
            await asyncio.sleep(POLL_INTERVAL)


# ── Start ─────────────────────────────────────────────────────────────────────

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        ik = await bot.get_me()
        log.info(f"Verbonden: @{ik.username}")
    except Exception as e:
        print(f"Telegram fout: {e}")
        return

    await bot.send_message(chat_id=CHAT_ID, text=(
        "Pump.fun Bot v3 gestart  —  SCHERPE FILTER\n\n"
        "Nieuwe filter (veel strenger):\n"
        f"  Min SOL eerste 30 sec:  {MIN_SOL_30S} SOL\n"
        f"  Min SOL totaal 60 sec:  {MIN_SOL_60S} SOL\n"
        f"  Min mcap na 30 sec:     ${MIN_MCAP_30S:,}\n"
        f"  Min groei 30->60 sec:   {(MIN_MCAP_GROEI-1)*100:.0f}%\n"
        f"  Verkopers check:        aan\n"
        f"  Take profit:            {TAKE_PROFIT}x\n"
        f"  Stop loss:              {STOP_LOSS_MINUTEN} min\n\n"
        "Verwacht: veel minder signalen, veel betere kwaliteit.\n"
        "Koop alleen als je een bericht krijgt!"
    ))

    await monitor_loop(bot)


if __name__ == "__main__":
    asyncio.run(main())
