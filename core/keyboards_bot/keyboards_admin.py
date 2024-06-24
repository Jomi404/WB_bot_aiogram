from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_cancel_btns(sizes: tuple[int, ...] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Отмена', callback_data='cancel')

    return keyboard.adjust(*sizes).as_markup()


def getKeyboardConfirm():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Верно', callback_data='yes'))
    keyboard.add(types.InlineKeyboardButton(text='Неверно', callback_data='no'))
    keyboard.adjust(2)

    return keyboard.as_markup()


def get_is_need_photo_btns(sizes: tuple[int, ...] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='yes'))
    keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='no'))

    return keyboard.adjust(*sizes).as_markup()
