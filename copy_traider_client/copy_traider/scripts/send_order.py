import pdb
import time

import MetaTrader5 as mt5
from copy_traider.scripts.utils import *


def run():
    while True:
        pdb.set_trace()
        # time.sleep(1)
        mt5.initialize()
        login()
        # mt5.login(login=login, password=password, server=server)
        # add_new_pending_order and update existing ones
        active_orders, active_orders_ticket = get_active_orders()
        db_orders, db_orders_ticket = get_data_base_orders()
        new_pending_orders(active_orders, db_orders_ticket)
        db_orders, db_orders_ticket = get_data_base_orders()
        update_pending_order(active_orders, db_orders, db_orders_ticket)

        # # # cancel an order
        active_orders, active_orders_ticket = get_active_orders()
        db_orders, db_orders_ticket = get_data_base_orders()
        active_positions, active_position_tickets = get_active_positions()
        order_cancel(db_orders, active_orders_ticket, active_position_tickets)

        # # make new position and update existing ones
        active_positions, active_positions_ticket = get_active_positions()
        db_active_positions, db_positions_tickets = get_data_base_positions()
        new_position(active_positions, db_positions_tickets)
        update_position(
            active_positions, db_active_positions, db_positions_tickets
        )

        # # close closed positions
        # pdb.set_trace()
        active_positions, active_positions_ticket = get_active_positions()
        db_active_positions, db_positions_tickets = get_data_base_positions()
        close_position(db_active_positions, active_positions_ticket)
        time.sleep(1)
