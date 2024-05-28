from bot import bot, dp

from aiogram import types
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.functions import check_user, get_lang, find_pair


@dp.message(CommandStart())
async def command_start(message: Message):
    user = await check_user(message)
    lang_data = await get_lang(message)

    referral_code = message.text.split()
    if len(referral_code) < 2:
        print("no")
    else:
        referral_code = referral_code[1]
        print(referral_code)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])

    if not all(s is None for s in await find_pair(user)):
        keyboard.inline_keyboard.append(
            [
                types.InlineKeyboardButton(text=lang_data["buttons"]["my_pair"], callback_data="my_pair"),
                types.InlineKeyboardButton(text=lang_data["buttons"]["main_menu"], callback_data="main_menu")
            ]
        )
    else:
        keyboard.inline_keyboard.append(
            [
                types.InlineKeyboardButton(text=lang_data["buttons"]["create_pair"], callback_data="create_pair"),
                types.InlineKeyboardButton(text=lang_data["buttons"]["main_menu"], callback_data="main_menu")
            ]
        )

    keyboard.inline_keyboard.append(
        [
            types.InlineKeyboardButton(text=lang_data["buttons"]["help"], callback_data="help"),
            types.InlineKeyboardButton(text=lang_data["buttons"]["change_language"], callback_data="change_language")
        ]
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text=lang_data["messages"]["start"],
        reply_markup=keyboard
    )
