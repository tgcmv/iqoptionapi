from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from dateutil import tz
import time, json
import data

def datetime_converter(param, format, timezone):
    _date = datetime.strptime(datetime.utcfromtimestamp(param).strftime(format), format)
    _date = _date.replace(tzinfo=tz.gettz('GMT'))
    return str(_date.astimezone(tz.gettz(timezone)))[:-6]

def time_converter(param):
    return datetime_converter(param, '%Y-%m-%d %H:%M:%S', 'America/Sao Paulo')

def login():
    _API = IQ_Option(data.email,data.password)
    while True:
        if _API.check_connect():
            print('Conectado com sucesso')
            break
        else:
            print('Erro ao se conectar')
        time.sleep(1)
    return _API

def api():
    if data.API is None:
        data.API = login()
        data.API.change_balance(data.balance_type)
        data.initial_balance = data.API.get_balance()
    return data.API

def actives():
    if data.actives is None: #default
        _all_asset = api().get_all_open_time()
        if _all_asset["turbo"]["EURUSD"]["open"]:
            data.actives="EURUSD"
        else:
            data.actives="EURUSD-OTC"
    return data.actives

def get_candles(count):
    return api().get_candles(actives(), data.interval_candle, count, time.time())

def stop_loose_balance():
    return data.initial_balance*(1-data.stoploose)

def stop_gain_balance():
    return data.initial_balance*(1-data.stopgain)

def stop_loose():
    return (stop_loose_balance() < api().get_balance())

def stop_gain():
    return (stop_gain_balance() < api().get_balance())

def buy(input_value, direction):
    return api().buy(input_value, actives(), direction, data.timeframe)