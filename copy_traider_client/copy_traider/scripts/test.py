import MetaTrader5 as mt5
from copyTrader_c.models import Symbols, OpenOrders, OpenPositions
import requests

copyTrade_taking_url = "http://127.0.0.1:8000/copyTrader/copyTrade_taking/"
cancel_trade_url = "http://127.0.0.1:8000/copyTrader/Cancel_order/"


def run():
    mt5.initialize()
    mt_active_positions = mt5.open_positions()
    print(mt_active_positions)
