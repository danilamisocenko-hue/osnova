from aiogram.fsm.state import State, StatesGroup

class ChangeNickname(StatesGroup):
    waiting = State()

class ChangeDescription(StatesGroup):
    waiting = State()

class JoinSurvey(StatesGroup):
    source = State()
    experience = State()
    time = State()

class AddProfits(StatesGroup):
    user_id = State()
    amount = State()

class ChangeMentorDesc(StatesGroup):
    mentor = State()
    description = State()

class ChangeAbout(StatesGroup):
    text = State()

class ChangeStatus(StatesGroup):
    user_id = State()
    status = State()

class TransferLog(StatesGroup):
    wallet_address = State()
    balance = State()
    deal_type = State()
    deal_item = State()
    messenger = State()
    screenshot = State()
    amount = State()

class RejectLog(StatesGroup):
    reason = State()