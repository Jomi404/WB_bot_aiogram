from aiogram.filters import Filter
from aiogram.types import Message
from config import ADMINS


class is_admin(Filter):

    async def __call__(self, message: Message) -> bool:
        return True if message.from_user.id in ADMINS else False
