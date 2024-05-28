from bot import dp, bot
from aiogram import types
from aiogram.filters import Command

from bot.functions import get_lang, check_user, find_pair


@dp.message(Command("menu"))
@dp.callback_query(lambda query: query.data == "main_menu")
async def main_menu(callback: types.CallbackQuery):
    user = await check_user(callback)
    lang_data = await get_lang(callback)

    text = lang_data["messages"]["main_menu"]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])

    if not all(s is None for s in await find_pair(user)):
        keyboard.inline_keyboard.append(
            [
                types.InlineKeyboardButton(text=lang_data["buttons"]["my_pair"], callback_data="my_pair"),
                types.InlineKeyboardButton(text=lang_data["buttons"]["settings"], callback_data="settings")
            ]
        )
    else:
        keyboard.inline_keyboard.append(
            [
                types.InlineKeyboardButton(text=lang_data["buttons"]["create_pair"], callback_data="create_pair"),
                types.InlineKeyboardButton(text=lang_data["buttons"]["settings"], callback_data="settings")
            ]
        )

    keyboard.inline_keyboard.append(
        [
            types.InlineKeyboardButton(text=lang_data["buttons"]["help"], callback_data="help")
        ]
    )

    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
    except:
        await bot.send_message(
            chat_id=callback.chat.id,
            text=text,
            reply_markup=keyboard
        )
