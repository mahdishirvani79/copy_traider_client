import pdb
import time

import requests

import MetaTrader5 as mt5
from copy_traider.models import OpenOrders, OpenPositions, Symbols

# BASE_URL = "http://185.190.39.107/"
BASE_URL = "http://127.0.0.1:8000/"
copyTrade_taking_url = BASE_URL + "copy_traider/copyTrade_taking/"
cancel_trade_url = BASE_URL + "copy_traider/Cancel_order/"
updata_pending_order_url = BASE_URL + "copy_traider/updata_pending_order/"
new_position_url = BASE_URL + "copy_traider/new_position/"
update_position_sltp_url = BASE_URL + "copy_traider/update_position_sltp/"
close_position_volume_url = BASE_URL + "copy_traider/close_position/"
close_position_url = BASE_URL + "copy_traider/close_position/"

REST = True
# This part is for when client and server is on one computer. if its not simply change
# REST to True
# SEYED Hadi Toloui investor
login_num = 110770
password = 'r0agknmf'
server = 'STPTraiding-Server'

# My Demo
# login_num = 68503915
# password = 'alkcuv2k'
# server = 'MetaQuotes-Demo'


# The 8 million demo
# login_num = 5012375215
# password = 'zu1gwclt'
# server = 'MetaQuotes-Demo'


def login():
    time.sleep(1)
    mt5.initialize()
    # if ~REST:
    #     mt5.login(login=login_num, password=password, server=server)


def get_active_orders():
    orders = mt5.orders_get()
    orders = [order._asdict() for order in orders]
    active_orders_ticket = [order["ticket"] for order in orders]
    return orders, active_orders_ticket


def get_data_base_orders():
    all_orders = OpenOrders.objects.filter(active=True)
    tickets = [o.ticket for o in all_orders]
    return all_orders, tickets


def get_active_positions():
    positions = mt5.positions_get()
    positions = [position._asdict() for position in positions]
    active_positions_ticket = [position["ticket"] for position in positions]
    return positions, active_positions_ticket


def get_data_base_positions():
    all_positions = OpenPositions.objects.filter(active=True)
    tickets = [o.ticket for o in all_positions]
    return all_positions, tickets


def new_pending_orders(active_orders, db_orders_ticket):
    for order in active_orders:
        # order = order._asdict()
        if order["ticket"] not in db_orders_ticket:
            type = "buy"
            if order["type"] == 3:
                type = "sell"
            balance = mt5.account_info()._asdict()['balance']
            volume = balance / order["volume_current"]
            data = {
                "symbol": order["symbol"],
                "type": type,
                "price": order["price_open"],
                "tp": order["tp"],
                "sl": order["sl"],
                "ticket": order["ticket"],
                "volume": volume,
            }
            print("pending order sent...")
            # pdb.set_trace()
            _order = requests.post(copyTrade_taking_url, data)
            login()
            if _order.status_code == 200:
                symbol = Symbols.objects.get(name=order["symbol"])
                model = OpenOrders.objects.create(
                    symbol=symbol,
                    price=order["price_open"],
                    tp=order["tp"],
                    sl=order["sl"],
                    ticket=order["ticket"],
                    volume=order["volume_current"],
                )
                model.save()
                print("order executed")
            elif _order.status_code == 500:
                print("server problem")
            else:
                print("problem: ", _order.text)
            # print("waiting...")


def new_position(active_positions, db_positions_ticket):
    for position in active_positions:
        # order = order._asdict()
        if position["ticket"] not in db_positions_ticket:
            type = "buy"
            if position["type"] == 1:
                type = "sell"
            balance = mt5.account_info()._asdict()['balance']
            volume = balance / position["volume"]
            data = {
                "symbol": position["symbol"],
                "type": type,
                "price": position["price_open"],
                "tp": position["tp"],
                "sl": position["sl"],
                "ticket": position["ticket"],
                "volume": volume,
                "price": position["price_open"],
            }
            # pdb.set_trace()
            print("position creating sent")
            _order = requests.post(new_position_url, data)
            login()
            if _order.status_code == 200:
                symbol = Symbols.objects.get(name=position["symbol"])
                model = OpenPositions.objects.create(
                    symbol=symbol,
                    open_price=position["price_open"],
                    tp=position["tp"],
                    sl=position["sl"],
                    ticket=position["ticket"],
                    volume=position["volume"],
                    side=type,
                    active=True,
                )
                model.save()
                print("position executed")
            elif _order.status_code == 500:
                print("server problem")
            else:
                print("problem: ", _order.text)


def update_pending_order(active_orders, db_orders, db_orders_ticket):
    for order in active_orders:
        if order["ticket"] in db_orders_ticket:
            # print(order)
            this_db_order = db_orders.get(ticket=order["ticket"])
            old_sl = this_db_order.sl
            old_tp = this_db_order.tp
            old_price = this_db_order.price
            if (
                order["sl"] != old_sl
                or order["tp"] != old_tp
                or order["price_open"] != old_price
            ):
                # pdb.set_trace()
                data = {
                    "ticket": order["ticket"],
                    "tp": order["tp"],
                    "sl": order["sl"],
                    "price": order["price_open"],
                }
                print("update pending sent")
                _order = requests.post(updata_pending_order_url, data)
                login()
                if _order.status_code == 200:
                    this_db_order.tp = order["tp"]
                    this_db_order.sl = order["sl"]
                    this_db_order.price = order["price_open"]
                    this_db_order.save()
                    print("order updated")
                elif _order.status_code == 500:
                    print("server problem")
                else:
                    print("problem: ", _order.text)


def update_position(
    active_positions, db_active_positions, db_positions_tickets
):
    for position in active_positions:
        if position["ticket"] in db_positions_tickets:
            # print(position)
            this_db_position = db_active_positions.get(
                ticket=position["ticket"]
            )
            old_sl = this_db_position.sl
            old_tp = this_db_position.tp
            if position["sl"] != old_sl or position["tp"] != old_tp:
                # pdb.set_trace()
                data = {
                    "ticket": position["ticket"],
                    "tp": position["tp"],
                    "sl": position["sl"],
                    "symbol": position["symbol"],
                }
                print("update sltp sent")
                _order = requests.post(update_position_sltp_url, data)
                login()
                if _order.status_code == 200:
                    this_db_position.tp = position["tp"]
                    this_db_position.sl = position["sl"]
                    this_db_position.open_price = position["price_open"]
                    this_db_position.save()
                    print("sltp updated")
                elif _order.status_code == 500:
                    print("server problem")
                else:
                    print("problem: ", _order.text)

            old_volume = this_db_position.volume
            if position["volume"] != old_volume:
                # pdb.set_trace()
                # type 1 is sell and 0 is buy
                volume = old_volume - position["volume"]
                volume_fraction = volume / old_volume
                data = {
                    "ticket": position["ticket"],
                    "volume_fraction": volume_fraction,
                    "type": position["type"],
                    "symbol": position["symbol"],
                }
                print("update volume sent")
                _order = requests.post(close_position_volume_url, data)
                login()
                if _order.status_code == 200:
                    this_db_position.volume = position["volume"]
                    this_db_position.save()
                    print("volume updated")
                elif _order.status_code == 500:
                    print("server problem")
                else:
                    print("problem: ", _order.text)


def close_position(db_positions, active_position_tickets):
    for position in db_positions:
        if position.ticket not in active_position_tickets:
            # pdb.set_trace()
            data = {
                "ticket": position.ticket,
                "volume_fraction": 1,
                "type": position.side,
                "symbol": position.symbol.name,
            }
            print("position close sent")
            _order = requests.post(close_position_url, data)
            login()
            if _order.status_code == 200:
                position.active = False
                position.save()
                print("position closed")
            elif _order.status_code == 500:
                print("server problem")
            else:
                print("problem: ", _order.text)


def order_cancel(db_orders, active_orders_ticket, active_position_tickets):
    for order in db_orders:
        if order.ticket not in active_orders_ticket:
            # pdb.set_trace()
            if order.ticket not in active_position_tickets:
                # order is closed
                data = {"ticket": order.ticket}
                print("order cancel sent")
                _order = requests.post(cancel_trade_url, data)
                login()
                if _order.status_code == 200:
                    order.active = False
                    order.save()
                    print("order canceled")
                elif _order.status_code == 500:
                    print("server problem")
                else:
                    print("problem: ", _order.text)
            else:
                order.active = False
                order.save()
