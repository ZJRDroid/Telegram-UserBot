try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, String, UnicodeText


class Filters(BASE):
    __tablename__ = "filters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText, nullable=False)

    async def __init__(self, chat_id, keyword, reply):
        self.chat_id = str(chat_id)  # ensure string
        self.keyword = keyword
        self.reply = reply

    async def __eq__(self, other):
        return bool(
            isinstance(other, Filters)
            and self.chat_id == other.chat_id
            and self.keyword == other.keyword
        )


Filters.__table__.create(checkfirst=True)


async def get_filter(chatid, keyword):
    try:
        return SESSION.query(Filters).get((str(chat_id), keyword))
    finally:
        SESSION.close()
    
    
async def get_filters(chat_id):
    try:
        return SESSION.query(Filters).filter(Filters.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()

        
async def add_filter(chat_id, keyword, reply):
    to_check = await get_filter(chatid, keyword)
    if not to_check:
        adder = Filters(str(chat_id), keyword, reply)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        return False


async def remove_filter(chat_id, keyword):
    to_check = await get_filter(chatid, keyword)
    
    if not to_check:
        return False
    else:
        # rem = SESSION.query(Filters).get((str(chat_id), keyword))
        rem = Filters(str(chat_id), keyword, reply)
        SESSION.delete(rem)
        SESSION.commit()
        return True
