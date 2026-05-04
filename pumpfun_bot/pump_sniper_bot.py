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

# Super filter drempelwaarden
MIN_SOL_INSTROOM  = 1.0    # minimaal 1 SOL in bonding curve na 30 sec
MIN_MCAP_GROEI    = 1.15   # mcap moet 15% gegroeid zijn na 60 sec
MIN_MCAP_START    = 3000   # token moet al boven $3k mcap zitten na 30 sec

# Trade instellingen
INZET_SOL         = 0.1
TAKE_PROFIT       = 2.0
STOP_LOSS_MINUTEN = 5

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
    mcap_start = token.get('usd_market_cap', 0)
    sol_start  = token.get('real_sol_reserves', 0) / 1e9
    res        = {}

    # Wacht 30 seconden
    log.info(f"  [{naam}] wacht 30 sec...")
    await asyncio.sleep(30)

    info30 = await haal_token_info(session, mint)
    if not info30:
        res['reden'] = 'Token niet meer beschikbaar'
        return None, res

    sol_30   = info30.get('real_sol_reserves', 0) / 1e9
    mcap_30  = info30.get('usd_market_cap', 0)
    sol_flow = sol_30 - sol_start
    res['sol_instroom'] = round(sol_flow, 3)
    res['mcap_30']      = round(mcap_30, 0)

    # Check 1: SOL instroom
    if sol_flow < MIN_SOL_INSTROOM:
        res['reden'] = f'Te weinig SOL: {sol_flow:.2f} (min {MIN_SOL_INSTROOM})'
        return None, res

    # Check 2: Mcap al boven minimum
    if mcap_30 < MIN_MCAP_START:
        res['reden'] = f'Mcap te laag: ${mcap_30:.0f} (min ${MIN_MCAP_START})'
        return None, res

    # Wacht nog 30 seconden (totaal 60 sec)
    log.info(f"  [{naam}] wacht nog 30 sec op mcap groei...")
    await asyncio.sleep(30)

    info60  = await haal_token_info(session, mint)
    mcap_60 = info60.get('usd_market_cap', 0) if info60 else 0
    sol_60  = info60.get('real_sol_reserves', 0) / 1e9 if info60 else 0
    res['mcap_60']  = round(mcap_60, 0)
    res['sol_60']   = round(sol_60, 3)

    # Check 3: Mcap groei tussen 30 en 60 sec
    if mcap_30 > 0 and mcap_60 < mcap_30 * MIN_MCAP_GROEI:
        groei = mcap_60 / mcap_30 if mcap_30 > 0 else 0
        res['reden'] = f'Geen groei: {groei:.2f}x (min {MIN_MCAP_GROEI:.2f}x)'
        return None, res

    # Creator stats
    c_totaal, c_grads = await haal_creator_stats(session, creator)
    res['creator_tokens']    = c_totaal
    res['creator_graduated'] = c_grads
    res['geslaagd']          = True

    return info60 or token, res


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
        "Pump.fun Bot v2 gestart (trades endpoint gefixed!)\n\n"
        f"Filter:\n"
        f"  Min SOL instroom 30s:  {MIN_SOL_INSTROOM} SOL\n"
        f"  Min mcap na 30s:       ${MIN_MCAP_START:,}\n"
        f"  Min mcap groei 60s:    {(MIN_MCAP_GROEI-1)*100:.0f}%\n"
        f"  Take profit:           {TAKE_PROFIT}x\n"
        f"  Stop loss:             {STOP_LOSS_MINUTEN} min\n\n"
        "Signalen komen zodra er een goed token is!"
    ))

    await monitor_loop(bot)


if __name__ == "__main__":
    asyncio.run(main())
