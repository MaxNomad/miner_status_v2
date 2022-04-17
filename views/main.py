import threading
import time

from SiviumMinerScreen import app, turbo
from flask import render_template

from core.http_get import get_stats, get_estimate, link_ether, link_ezil, link_flock
from core.miner_loader import get_miner_stats
from core.pool_data_decoder import get_ether_hash, get_ezil_hash, get_ezil_balance, get_flockpool


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_miner_load).start()


def update_miner_load():
    with app.app_context():
        while True:
            difficulty, ping, algo, description, driver, gpu_total, accepted_count, rejected_count, invalid_count, hashrate, uptime, os, name, version, time_server, gpus, power_total, miner_errors, workers_num  = get_miner_stats()
            turbo.push(turbo.replace(render_template('miner.html', difficulty=difficulty, ping=ping, algo=algo,
                                                     description=description, driver=driver, gpu_total=gpu_total,
                                                     accepted_count=accepted_count, rejected_count=rejected_count,
                                                     invalid_count=invalid_count, hashrate=hashrate,
                                                     uptime=time.strftime('%d:%H:%M:%S', time.gmtime(uptime)), os=os,
                                                     name=name,
                                                     version=version, time_server=time_server, gpus=gpus,
                                                     power_total=power_total, workers_num=workers_num, miner_errors=miner_errors), 'miner'))
            time.sleep(1)


@app.route("/", methods=["GET"])
def get_status():
        start_time = time.time()
        data = get_stats()
        difficulty, ping, algo, description, driver, gpu_total, accepted_count, rejected_count, invalid_count, hashrate, uptime, os, name, version, time_server, gpus, power_total, miner_errors, workers_num = get_miner_stats()
        current_hashrate_eth, reported_hashrate_eth, average_hashrate_eth, validShares_eth, staleShares_eth, invalidShares_eth, if_eth_online, valid_pers_eth, stale_pers_eth, invalid_pers_eth, unpaid_eth, hash_total_eth = get_ether_hash(
            data[3])
        current_hashrate_ezil, average_hashrate_ezil, reported_hashrate_ezil, if_ezil_online, hash_total_ezil = get_ezil_hash(data[1])

        ezil_eth, ezil_zil = get_ezil_balance(data[2])
        balance_immature_flock, balance_mature_flock, balance_paid_flock, hash_now_flock, hash_avg_flock, shares_accepted_total_flock, shares_stale_total_flock, shares_rejected_total_flock, valid_pers_flock, stale_pers_flock, invalid_pers_flock, is_flock_online = get_flockpool(
            data[0])
        estimete_pools = get_estimate(hash_total_eth, hash_total_ezil, 1)
        ezil_estimate = (estimete_pools[1])['ezil_estimate']
        ethermine_estimate = (estimete_pools[0])['ethermine_estimate']
        print("--- Total time: %s ---" % (time.time() - start_time))
        return render_template("status.html", difficulty=difficulty, ping=ping, algo=algo, description=description,
                               driver=driver, gpu_total=gpu_total, accepted_count=accepted_count,
                               rejected_count=rejected_count, invalid_count=invalid_count, hashrate=hashrate,
                               uptime=time.strftime('%d:%H:%M:%S', time.gmtime(uptime)), os=os, name=name, version=version,
                               time_server=time_server, gpus=gpus, power_total=power_total,
                               if_ethermine_online=if_eth_online, current_hashrate_eth=current_hashrate_eth,
                               reported_hashrate_eth=reported_hashrate_eth, average_hashrate_eth=average_hashrate_eth,
                               validShares_eth_eth=validShares_eth, staleShares_eth=staleShares_eth,
                               invalidShares_eth=invalidShares_eth,
                               valid_pers_eth=valid_pers_eth,
                               stale_pers_eth=stale_pers_eth, invalid_pers_eth=invalid_pers_eth, unpaid_eth=unpaid_eth,
                               current_hashrate_ezil=current_hashrate_ezil, average_hashrate_ezil=average_hashrate_ezil,
                               reported_hashrate_ezil=reported_hashrate_ezil, if_ezil_online=if_ezil_online,
                               ezil_eth=ezil_eth, ezil_zil=ezil_zil, balance_immature_flock=balance_immature_flock,
                               balance_mature_flock=balance_mature_flock,
                               balance_paid_flock=balance_paid_flock, hash_now_flock=hash_now_flock,
                               hash_avg_flock=hash_avg_flock, shares_accepted_total_flock=shares_accepted_total_flock,
                               shares_stale_total_flock=shares_stale_total_flock,
                               shares_rejected_total_flock=shares_rejected_total_flock,
                               valid_pers_flock=valid_pers_flock,
                               stale_pers_flock=stale_pers_flock, invalid_pers_flock=invalid_pers_flock,
                               if_flock_online=is_flock_online,ezil_usd=ezil_estimate,only_eth_in_usd=ethermine_estimate, workers_num=workers_num,link_ethermine=link_ether, link_ezil=link_ezil, link_flock=link_flock, miner_errors=miner_errors
                               )

