from config_init import config
import argparse
import sys
from flask_bootstrap import Bootstrap
from flask import Flask
from turbo_flask import Turbo
import flask_restful


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=config['debug'])
    parser.add_argument('--log', default=config['log'])
    return parser


namespace = arg_parse().parse_args(sys.argv[1:])
app = Flask(__name__, template_folder='templates', static_folder='static')
api = flask_restful.Api(app, catch_all_404s=True)
Bootstrap(app)
turbo = Turbo(app)
from views.main import *

if __name__ == '__main__':
    app.run(host=config['bind']['host'], port=config['bind']['port'], debug=namespace.debug)
