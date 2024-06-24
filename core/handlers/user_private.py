import logging
import os

from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import Router, types, F

import core.utils as utils

from core import keyboards_bot
from core.filters_bot import ChatTypeFilterMes, ChatTypeFilterCall
from core.logger_csm import CustomFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilterMes(['private']))
user_private_router.callback_query.filter(ChatTypeFilterCall(['private']))


@user_private_router.message(CommandStart())
async def cmd_start(message: types.Message):

    # функция проверки пользователя в json-файле users и в случае если пользователь новый то добавляем
    # нужно добавить проверку на существование файла или просто создавать
    if await utils.is_new_users(user_id=message.from_user.id):
        await utils.add_user_to_json(user_id=message.from_user.id)

    link = utils.get_link.getHyperLink(url='https://t.me/cashback_market_1', title='Кэшбэк.Маркет')
    text = (f'У нас можно купить товары со скидками до 100%\n'
            f'● Выкупайте любой товар из каталога\n'
            f'● Следуйте инструкции\n'
            f'● Кэшбэк выплачивается, даже если отзыв исключили\n'
            f'● Отзывы о нас читайте тут {link}\n'
            f'Каталог с товарами и инструкции по выкупу 👇')
    link_web_app = 'https://telegra.ph/O-servise-06-21'
    reply_markup = keyboards_bot.get_start_btns(link=link_web_app, sizes=(1,))
    await utils.bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=reply_markup,
                                 parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@user_private_router.callback_query(F.data.startswith("about"))
async def about_info(callback: types.CallbackQuery):
    await callback.answer()
    text = (f'<b>О сервисе:</b>\n'
            f'<b>Кешбэк.Маркет</b> - это удобное и безопасное решение для выкупа товаров за отзывы.\n'
            f'На нашей площадке собраны товары от проверенных поставщиков с кешбэком до 100%.\n'
            f'Мы упростили все процессы, чтобы вам было легко, понятно и безопасно делать выкуп.')
    reply_markup = keyboards_bot.get_about_btns((1,), )
    await callback.message.edit_text(inline_message_id=callback.inline_message_id, text=text, reply_markup=reply_markup,
                                     parse_mode=ParseMode.HTML)


@user_private_router.callback_query(F.data.startswith("place_instruct"))
async def place_instruct_info(callback: types.CallbackQuery):
    await callback.answer()
    link = utils.get_link.getHyperLink(url='https://telegra.ph/Instrukciya-razmeshcheniya-06-21', title='Инструкция')
    text = (f'<b>Разместить товар в каталоге</b>\n'
            f'Как работает бот можете посмотреть тут {link}\n'
            f'● 0% штрафов. Наш подход позволяет выкупать максимально органично\n'
            f'● Минимум переписок\n'
            f'● Тех. поддержка')
    link_web_app = 'https://telegra.ph/O-servise-06-21'
    reply_markup = keyboards_bot.get_place_instruct_info_btns(link=link_web_app, sizes=(1,))
    await callback.message.edit_text(inline_message_id=callback.inline_message_id, text=text, reply_markup=reply_markup,
                                     parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@user_private_router.callback_query(F.data.startswith("menu"))
async def main_menu(callback: types.CallbackQuery):
    await callback.answer()
    link = utils.get_link.getHyperLink(url='https://t.me/cashback_market_1', title='Кэшбэк.Маркет')
    text = (f'У нас можно купить товары со скидками до 100%\n'
            f'● Выкупайте любой товар из каталога\n'
            f'● Следуйте инструкции\n'
            f'● Кэшбэк выплачивается, даже если отзыв исключили\n'
            f'● Отзывы о нас читайте тут {link}\n'
            f'Каталог с товарами и инструкции по выкупу 👇')
    link_web_app = 'https://telegra.ph/O-servise-06-21'
    reply_markup = keyboards_bot.get_start_btns(link=link_web_app, sizes=(1,))
    await callback.message.edit_text(inline_message_id=callback.inline_message_id, text=text, reply_markup=reply_markup,
                                     parse_mode=ParseMode.HTML, disable_web_page_preview=True)


