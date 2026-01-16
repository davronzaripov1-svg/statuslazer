from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """States for new order flow"""
    waiting_client_type = State()      # S_NEW_TYPE
    waiting_branch = State()           # S_NEW_BRANCH (for branch clients)
    waiting_client_name = State()      # S_NEW_CLIENT_NAME (for regular clients)
    waiting_delivery = State()         # S_NEW_DELIVERY
    waiting_sheets = State()           # S_NEW_SHEETS
    checking_capacity = State()        # S_NEW_CAPACITY_CHECK
    waiting_overload_decision = State() # S_NEW_OVERLOAD - user decides to accept or cancel
    waiting_file = State()             # S_NEW_FILE


class MyOrdersStates(StatesGroup):
    """States for viewing orders"""
    viewing_list = State()             # S_MY_ORDERS
    viewing_card = State()             # S_ORDER_CARD
