import sys
import aiohttp
import asyncio
from config_init import config
from core.support import toFixed


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


wallet_ethermine = config["wallets"]["wallet_ethermine"]
wallet_ezil = config["wallets"]["wallet_ezil"]
wallet_flock = config["wallets"]["wallet_flock"]

if wallet_flock:
    link_flock = "https://flockpool.com/miners/rtm/" + wallet_flock
    api_flock = "https://flockpool.com/api/v1/wallets/rtm/" + wallet_flock

if wallet_ezil:
    api_ezil_stats = "https://stats.ezil.me/current_stats/" + wallet_ezil + "/reported"
    api_ezil_balance = "https://billing.ezil.me/balances/" + wallet_ezil
    link_ezil = "https://ezil.me/personal_stats?wallet=" + wallet_ezil

if wallet_ethermine:
    api_ether = "https://api.ethermine.org/miner/" + wallet_ethermine + "/dashboard"
    link_ether = "https://ethermine.org/miners/" + wallet_ethermine + "/dashboard"


async def get_ether_stats(session):
    if wallet_ezil:
        try:
            async with session.get(api_ether) as resp:
                ezil_stats = await resp.json()
                return {'ethermine': ezil_stats}
        except:
            return {'ethermine': None}
    else:
        return {'ethermine': None}


async def get_ezil_stats(session):
    if wallet_ezil:
        try:
            async with session.get(api_ezil_stats) as resp:
                ezil_stats = await resp.json()
                return {'ezil_stats': ezil_stats}
        except:
            return {'ezil_stats': None}
    else:
        return {'ezil_stats': None}


async def get_ezil_balance(session):
    if wallet_ezil:
        try:
            async with session.get(api_ezil_balance) as resp:
                ezil_balance = await resp.json()
                return {'ezil_balance': ezil_balance}
        except:
            return {'ezil_balance': None}
    else:
        return {'ezil_balance': None}


async def get_flockpool(session):
    if wallet_flock:
        try:
            async with session.get(api_flock) as resp:
                flockpool = await resp.json()
                return {'flockpool': flockpool}
        except:
            return {'flockpool': None}
    else:
        return {'flockpool': None}


async def async_get_stats():
    async with aiohttp.ClientSession() as session:
        tasks = []
        tasks.append(asyncio.ensure_future(get_flockpool(session)))
        tasks.append(asyncio.ensure_future(get_ezil_stats(session)))
        tasks.append(asyncio.ensure_future(get_ezil_balance(session)))
        tasks.append(asyncio.ensure_future(get_ether_stats(session)))
        data = await asyncio.gather(*tasks)
        return data


async def get_estimates_ezil(session, hashrate, scale):
    if hashrate > 0:
        api_ezil_calc = "https://mining-profits.ezil.me/reports/forecast.json/?preset_name=LAST_24_HOURS&hashrate=" + str(
            hashrate) + "&scale=" + str(scale)
        async with session.get(api_ezil_calc) as resp:
            estimate = await resp.json()
            eth_with_zil_in_usd = toFixed(float(estimate['eth']['eth_with_zil_in_usd']), 2)
            return {'ezil_estimate': eth_with_zil_in_usd}
    else:
        return {'ezil_estimate': 0}


async def get_estimates_ether(session, hashrate, scale):
    if hashrate > 0:
        api_ezil_calc = "https://mining-profits.ezil.me/reports/forecast.json/?preset_name=LAST_24_HOURS&hashrate=" + str(
            hashrate) + "&scale=" + str(scale)
        async with session.get(api_ezil_calc) as resp:
            estimate = await resp.json()
            only_eth_in_usd = toFixed(float(estimate['eth']['only_eth_in_usd']), 2)
            return {'ethermine_estimate': only_eth_in_usd}
    else:
        return {'ethermine_estimate': 0}


async def async_calculate_estimates(ethermine, ezil, scale):
    estimate = []
    async with aiohttp.ClientSession() as session:
        estimate.append(asyncio.ensure_future(get_estimates_ether(session, ethermine, scale)))
        estimate.append(asyncio.ensure_future(get_estimates_ezil(session, ezil, scale)))
        data = await asyncio.gather(*estimate)
        return data


def get_stats():
    try:
        get_stats_data = asyncio.run(async_get_stats())
        return get_stats_data
    except:
        pass


def get_estimate(ethermine, ezil, scale):
    global get_estimate_data
    try:
        get_estimate_data = asyncio.run(async_calculate_estimates(ethermine, ezil, scale))
    except:
        pass
    return get_estimate_data