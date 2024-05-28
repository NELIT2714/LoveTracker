from bot import bot, dp

from aiogram import types
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.functions import check_user, get_lang, find_pair, get_start_argument


@dp.message(CommandStart())
async def command_start(message: Message):
    from bot import mongo

    user = await check_user(message)
    lang_data = await get_lang(message)
    text = lang_data["messages"]["start"]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    if not all(s is None for s in await find_pair(user)):
        pair = await mongo["pairs"].find_one({"pair_creator": user.get("telegram_id")})
        if not pair.get("pair_member") is None:
            text = lang_data["messages"]["start_with_pair"]

        keyboard.inline_keyboard.append([
            types.InlineKeyboardButton(text=lang_data["buttons"]["my_pair"], callback_data="my_pair"),
            types.InlineKeyboardButton(text=lang_data["buttons"]["main_menu"], callback_data="main_menu")
        ])
    else:
        keyboard.inline_keyboard.append([
            types.InlineKeyboardButton(text=lang_data["buttons"]["create_pair"], callback_data="create_pair"),
            types.InlineKeyboardButton(text=lang_data["buttons"]["main_menu"], callback_data="main_menu")
        ])

    keyboard.inline_keyboard.append([
        types.InlineKeyboardButton(text=lang_data["buttons"]["help"], callback_data="help"),
        types.InlineKeyboardButton(text=lang_data["buttons"]["change_language"], callback_data="change_language")
    ])

    pair_code = await get_start_argument(message)
    if pair_code is not None:
        home_button = types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(text=lang_data["buttons"]["main_menu"], callback_data="main_menu")
        ]])

        if not all(s is None for s in await find_pair(user)):
            return await bot.send_message(
                chat_id=message.chat.id,
                text=lang_data["messages"]["errors"]["already_have_pair"],
                reply_markup=home_button
            )

        pair = await mongo["pairs"].find_one({"pair_code": str(pair_code.split("_")[-1])})
        if pair is None:
            return await bot.send_message(
                chat_id=message.chat.id,
                text=lang_data["messages"]["errors"]["invalid_link"],
                reply_markup=home_button
            )
        else:
            text = lang_data["messages"]["pairing_invitation"]
            pair_creator = await mongo["users"].find_one({"telegram_id": int(pair.get("pair_creator"))})

            if pair_creator.get("username") is None:
                text = text.replace("{username}", f"<a href='tg://user?id={str(pair_creator.get('telegram_id'))}'>{pair_creator.get('first_name')}{' ' + pair_creator.get('last_name') if pair_creator.get('last_name') is not None else ''}</a>")
            else:
                text = text.replace("{username}", f"@{pair_creator.get('username')}")

            return await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [
                        types.InlineKeyboardButton(text=lang_data["buttons"]["accept"], callback_data="accept_pair_invitation"),
                        types.InlineKeyboardButton(text=lang_data["buttons"]["cancel"], callback_data="cancel_pair_invitation")
                    ],
                    [
                        types.InlineKeyboardButton(text=lang_data["buttons"]["ignore"], callback_data="ignore_pair_invitation")

                    ]
                ]),
                parse_mode="html"
            )

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard
    )
