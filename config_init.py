import json
import os


def where_json(file_name):
    return os.path.exists(file_name)


if where_json('config.json'):
    with open("config.json", "r") as jsonfile:
        config = json.load(jsonfile)
else:
    data = {
        "version": "1.234",
        "bind": {
            "host": "127.0.0.1",
            "port": 8080
        },
        "debug": True,
        "log": True,
        "wallets": {
            "wallet_ethermine": "51C56ABC1cAE715D5D1011E7523a9954917D8e19",
            "wallet_ezil": "0xbf688d4614340bb7696ff9c65ea6d3331d3c7697.zil13jckvpc6dcq5x3htqet66mr5gxpcv9vcfmkcup",
            "wallet_flock": "RMKeAFYwbAZpWTaMHUkuMgj1ZK5HksKcvU"
        },

        "miners": [
            {
                "name": "trex",
                "api": "http://192.168.0.148:4059/summary",
                "def_wats": 150
            }
        ]
    }
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)
    with open("config.json", "r") as jsonfile:
        config = json.load(jsonfile)