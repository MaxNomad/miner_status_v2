from core.support import toFixed


def get_ether_hash(data):
    if data['ethermine']:
        if data['ethermine']['data']['currentStatistics']['unpaid'] != 0:
            unpaid = toFixed((int(data['ethermine']['data']['currentStatistics']['unpaid']) / 1000000000000000000), 4)
        else:
            unpaid = 0
        try:
            current_hashrate = toFixed(
                ((float(data['ethermine']['data']['currentStatistics']['currentHashrate'])) / 1000000), 2)
            hash_total_ = int(data['ethermine']['data']['currentStatistics']['currentHashrate'])
            reported_hashrate = toFixed(
                ((float(data['ethermine']['data']['currentStatistics']['reportedHashrate'])) / 1000000), 2)
            average_hashrate = toFixed(((float(current_hashrate) + float(reported_hashrate)) / 2), 2)
            validShares = int(data['ethermine']['data']['currentStatistics']['validShares'])

            invalidShares = int(data['ethermine']['data']['currentStatistics']['invalidShares'])
            staleShares = int(data['ethermine']['data']['currentStatistics']['staleShares'])
            if validShares != 0:
                stale_pers = float(toFixed(((staleShares / validShares) * 100), 2))
            else:
                stale_pers = 0
            valid_pers = float(toFixed((100 - stale_pers), 2))
            invalid_pers = float(toFixed(100 - (valid_pers + stale_pers), 2))
            if reported_hashrate == "0.00":
                return 0, 0, 0, 0, 0, 0, False, 0, 0, 0, unpaid, 0
            return current_hashrate, reported_hashrate, average_hashrate, validShares, staleShares, invalidShares, True, valid_pers, stale_pers, invalid_pers, unpaid, hash_total_
        except:
            return 0, 0, 0, 0, 0, 0, False, 0, 0, 0, unpaid, 0
    else:
        return 0, 0, 0, 0, 0, 0, False, 0, 0, 0, 0, 0


def get_ezil_hash(data):
    try:
        if data['ezil_stats']:
            current_hashrate = toFixed(((int(data['ezil_stats']['current_hashrate']))/1000000), 2)
            average_hashrate = toFixed(((int(data['ezil_stats']['average_hashrate']))/1000000), 2)
            reported_hashrate = toFixed(((int(data['ezil_stats']['reported_hashrate']))/1000000), 2)
            hash_total = int(data['ezil_stats']['current_hashrate'])
            if current_hashrate == "0.00":
                return current_hashrate, average_hashrate, reported_hashrate, False, 0
            return current_hashrate, average_hashrate, reported_hashrate, True, hash_total
        else:
            return 0, 0, 0, False, 0
    except:
        return 0, 0, 0, False, 0


def get_ezil_balance(data):
    if data['ezil_balance']:
        eth = toFixed(data['ezil_balance']['eth'], 4)
        zil = toFixed(data['ezil_balance']['zil'], 2)
        return eth, zil
    else:
        return 0, 0


def get_flockpool(data_json):
    if data_json['flockpool']:
        if data_json['flockpool']['balance']['immature'] != 0:
            balance_immature = toFixed((data_json['flockpool']['balance']['immature']) / 100000000, 4)
        else:
            balance_immature = data_json['flockpool']['balance']['immature']
        if data_json['flockpool']['balance']['mature'] != 0:
            balance_mature = toFixed((data_json['flockpool']['balance']['mature']) / 100000000, 2)
        else:
            balance_mature = data_json['flockpool']['balance']['mature']
        if data_json['flockpool']['balance']['paid'] != 0:
            balance_paid = toFixed((data_json['flockpool']['balance']['paid']) / 100000000, 2)
        else:
            balance_paid = data_json['flockpool']['balance']['paid']
        workers = data_json['flockpool']['workers']
        hash_now = []
        hash_avg = []
        shares_accepted = []
        shares_stale = []
        shares_rejected = []
        for worker in workers:
            hash_now.append(worker['hashrate']['now'])
            hash_avg.append(worker['hashrate']['avg'])
            shares_accepted.append(worker['shares']['accepted'])
            shares_stale.append(worker['shares']['stale'])
            shares_rejected.append(worker['shares']['rejected'])
        hash_now_total = toFixed(float(sum(hash_avg)), 2)
        hash_avg_total = toFixed(float(sum(hash_now)), 2)
        shares_accepted_total = sum(shares_accepted)
        shares_stale_total = sum(shares_stale)
        shares_rejected_total = sum(shares_rejected)
        if shares_accepted_total != 0:
            stale_pers = float(toFixed(((shares_stale_total / shares_accepted_total) * 100), 2))
        else:
            stale_pers = 0
        valid_pers = float(toFixed((100 - stale_pers), 2))
        invalid_pers = float(toFixed(100 - (valid_pers + stale_pers), 2))
        if hash_avg_total == "0.00":
            return balance_immature, balance_mature, balance_paid, 0, 0, 0, 0, 0, 0, 0, 0, False
        return balance_immature, balance_mature, balance_paid, hash_avg_total, hash_now_total, shares_accepted_total, shares_stale_total, shares_rejected_total, valid_pers, stale_pers, invalid_pers, True
    else:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False