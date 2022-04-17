import asyncio
import json
import aiohttp
from core.support import toFixed

from config_init import config


async def miner_connect(api_url, session, wats):
    async with session.get(api_url) as resp:
        miner_data = await resp.json()
    return miner_data


async def miner_stats():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for miner in config['miners']:
            if miner['name'] == 'trex':
                tasks.append(asyncio.ensure_future(miner_connect(miner['api'], session, miner['def_wats'])))
            else:
                print("=============!!!!!!!==============")
                print(config['name'], 'Unsuported Schema')
                print("=============!!!!!!!==============")
        data = await asyncio.gather(*tasks)

        return data


def trex_parcer(data):
    difficulty = data['active_pool']['difficulty']
    ping = data['active_pool']['ping']
    algo = data['algorithm']
    description = data['description']
    driver = data['driver']
    accepted_count = data['accepted_count']
    rejected_count = data['rejected_count']
    invalid_count = data['invalid_count']
    hashrate = data['hashrate']
    uptime = data['uptime']
    os = data['os']
    name = data['name']
    version = data['version']
    time_server = data['time']
    gpus = data['gpus']
    return locals()


def get_miner_stats():
    miner_power = []
    total_gpu = []
    total_hash = []
    accepted_total = []
    rejected_total = []
    invalid_total = []
    all_gpu = []
    total_stok_power = []
    try:
        miener_data = asyncio.run(miner_stats())


        workers_num = int(len(miener_data))
        if miener_data:
            for data in miener_data:
                difficulty = data['active_pool']['difficulty']
                ping = data['active_pool']['ping']
                algo = data['algorithm']
                description = data['description']
                driver = data['driver']
                total_gpu.append(data['gpu_total'])
                accepted_total.append(data['accepted_count'])
                rejected_total.append(data['rejected_count'])
                invalid_total.append(data['invalid_count'])
                total_hash.append(float(data['hashrate'] / 1000000))
                uptime = data['uptime']
                os = data['os']
                name = data['name']
                version = data['version']
                time_server = data['time']
                gpus = data['gpus']
                for gpu in gpus:
                    miner_power.append(gpu['power'])
                    all_gpu.append(gpu)
            power_total = int(sum(miner_power)) + 150
            gpu_total = int(sum(total_gpu))
            hashrate = toFixed(float(sum(total_hash)), 2)
            accepted_count = int(sum(accepted_total))
            rejected_count = int(sum(rejected_total))
            invalid_count = int(sum(invalid_total))
            return difficulty, ping, algo, description, driver, gpu_total, accepted_count, rejected_count, invalid_count, hashrate, uptime, os, name, version, time_server, all_gpu, power_total, False, workers_num
        else:
            return None, None, None, None, None, 0, 0, 0, 0, 0, None, None, None, None, None, [], None, True, 0
    except:
        return None, None, None, None, None, 0, 0, 0, 0, 0, None, None, None, None, None, [], None, True, 0
