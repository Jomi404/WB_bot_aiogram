from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Router, types, F, filters
from aiogram.fsm.context import FSMContext

import core.utils as utils

from core import keyboards_bot
from core.filters_bot import ChatTypeFilterMes, ChatTypeFilterCall, is_admin
from core.states import Admin

admin_private_router = Router()
admin_private_router.message.filter(ChatTypeFilterMes(['private']))
admin_private_router.callback_query.filter(ChatTypeFilterCall(['private']))


@admin_private_router.message(is_admin(), Command('mailing'))
async def cmd_admin(message: types.Message, state: FSMContext):
    await state.set_state(Admin.create_mailling)
    await state.set_data({})
    text = (f'Вы начали создание рассылки.\n\n'
            f'<b>Пожалуйста введите название рассылки:</b>')
    reply_markup = keyboards_bot.get_cancel_btns()
    await utils.bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=reply_markup,
                                 parse_mode=ParseMode.HTML)


@admin_private_router.message(filters.StateFilter(Admin.create_mailling))
async def process_confirm_mailling(message: types.Message, state: FSMContext):
    await state.update_data({'mailling_name': message.text})
    await state.set_state(Admin.confirm_mailling_name)
    reply_markup = keyboards_bot.getKeyboardConfirm()
    text = (f'Вы отправили <b>{message.text}</b>\n\n'
            f'Пожалуйста проверьте название рассылки.\n'
            f'И нажмите соответствующую клавишу <b>Верно/Неверно</b>')

    await utils.bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=reply_markup,
                                 parse_mode=ParseMode.HTML)


@admin_private_router.callback_query(filters.StateFilter(Admin.confirm_mailling_name), F.data.startswith("no"))
async def process_confirm_no_mailling(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.create_mailling)
    text = f'Пожалуйста введите название рассылки снова:'
    await utils.bot.send_message(chat_id=callback.from_user.id, text=text)


@admin_private_router.callback_query(filters.StateFilter(Admin.confirm_mailling_name), F.data.startswith("yes"))
async def process_confirm_yes_mailling(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.input_mailling_desc)
    text = f'Пожалуйста введите <b>Описание рассылки</b>:'
    await utils.bot.send_message(chat_id=callback.from_user.id, text=text, parse_mode=ParseMode.HTML)


@admin_private_router.message(filters.StateFilter(Admin.input_mailling_desc))
async def process_confirm_descMailling(message: types.Message, state: FSMContext):
    await state.set_state(Admin.confirm_mailling_desc)
    data = await state.get_data()
    await state.update_data({'mailling_description': message.text})
    reply_markup = keyboards_bot.getKeyboardConfirm()
    text = (f'Вы отправили <b>{message.text}</b>\n\n'
            f'Пожалуйста проверьте введенное описание рассылки.\n'
            f'И нажмите соответствующую клавишу <b>Верно/Неверно</b>')
    await utils.bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=reply_markup,
                                 parse_mode=ParseMode.HTML)


@admin_private_router.callback_query(filters.StateFilter(Admin.confirm_mailling_desc), F.data.startswith("no"))
async def process_confirm_no_descMailling(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.input_mailling_desc)
    text = f'Пожалуйста введите <b>описание рассылки</b> снова:'
    await utils.bot.send_message(chat_id=callback.from_user.id, text=text, parse_mode=ParseMode.HTML)


@admin_private_router.callback_query(filters.StateFilter(Admin.confirm_mailling_desc), F.data.startswith("yes"))
async def process_confirm_yes_descMailling(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.is_need_photo)
    reply_markup = keyboards_bot.get_is_need_photo_btns()
    text = f'Нужно ли добавить картинку к рассылке?'
    await utils.bot.send_message(chat_id=callback.from_user.id, text=text, reply_markup=reply_markup)


@admin_private_router.callback_query(filters.StateFilter(Admin.is_need_photo), F.data.startswith("no"))
async def process_sending_mailing_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    users_json = await utils.get_data_json(path='W:\\WB_BOT\\WB_bot_aiogram\\core\\data\\users.json')  # ЗАМЕНИТЬ ПУТЬ
    for user in users_json['users']:
        await utils.bot.send_message(chat_id=user['id'],
                                     text=f"{data['mailling_name']}\n{data['mailling_description']}")

    await utils.bot.send_message(chat_id=callback.from_user.id, text='Рассылка отправлена.')
    await state.clear()


@admin_private_router.callback_query(filters.StateFilter(Admin.is_need_photo), F.data.startswith("yes"))
async def process_sending_mailing_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.get_photo)
    text = (f'Пожалуйста отправьте картинку для рассылки:')

    await utils.bot.send_message(chat_id=callback.from_user.id, text=text)


@admin_private_router.message(Admin.get_photo, F.photo)
async def set_photo_handler(message: types.Message, state: FSMContext):
    await state.update_data(msg_photo=message.photo[-1].file_id)
    await state.set_state(Admin.confirm_photo)
    text = (f'Вы отправили картинку\n\n'
            f'Пожалуйста проверьте та ли это картинка.\n'
            f'И нажмите соответствующую клавишу <b>Верно/Неверно</b>')
    reply_markup = keyboards_bot.getKeyboardConfirm()
    await message.reply(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


@admin_private_router.callback_query(filters.StateFilter(Admin.confirm_photo), F.data.startswith("no"))
async def process_get_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.get_photo)
    text = f'Пожалуйста отправьте картинку для рассылки снова:'
    await utils.bot.send_message(chat_id=callback.from_user.id, text=text,
                                 parse_mode=ParseMode.HTML)


@admin_private_router.callback_query(filters.StateFilter(Admin.confirm_photo), F.data.startswith("yes"))
async def process_get_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    caption = (f"{data['mailling_name']}\n"
               f"{data['mailling_description']}")
    users_json = await utils.get_data_json(path="core/data/users.json")
    for user in users_json['users']:
        await utils.bot.send_photo(chat_id=user['id'], photo=data['msg_photo'], caption=caption)

    await utils.bot.send_message(chat_id=callback.from_user.id, text='Рассылка отправлена.')
    await state.clear()


@admin_private_router.message(Admin.get_photo, ~F.photo)
async def set_photo_handler(message: types.Message, state: FSMContext):
    await message.reply(text='Пожалуйста отправьте картинку 🏞')


@admin_private_router.callback_query(F.data.startswith("cancel"))
async def process_callback_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer("Действие отменено.")
