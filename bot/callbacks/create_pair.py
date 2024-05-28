import asyncio

from bot import dp, bot
from aiogram import types
from aiogram.filters import Command

from bot.functions import get_lang, check_user, generate_pair_code, find_pair


@dp.message(Command("create_pair"))
@dp.callback_query(lambda query: query.data == "create_pair")
async def main_menu(callback: types.CallbackQuery):
    from bot import mongo
    from datetime import datetime

    user = await check_user(callback)
    lang_data = await get_lang(callback)

    if not all(s is None for s in await find_pair(user)):
        text = lang_data["messages"]["errors"]["pair_already_exists"]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text=lang_data["buttons"]["back"], callback_data="main_menu")
            ]
        ])
        try:
            return await callback.message.edit_text(
                text=text,
                reply_markup=keyboard
            )
        except:
            return await bot.send_message(
                chat_id=callback.chat.id,
                text=text,
                reply_markup=keyboard
            )

    pair_code = await generate_pair_code()
    timestamp = datetime.now().timestamp()
    await mongo["pairs"].insert_one({
        "pair_creator": int(user.get("telegram_id")),
        "pair_member": None,
        "pair_code": str(pair_code),
        "settings": [],
        "creation_timestamp": int(timestamp),
        "update_timestamp": int(timestamp)
    })

    text = lang_data["messages"]["create_pair"].replace("{link}", f"https://t.me/lovetracker_bot?start=pair_{pair_code}")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=lang_data["buttons"]["cancel"], callback_data="cancel_create_pair"),
            types.InlineKeyboardButton(text=lang_data["buttons"]["generate_new_link"], callback_data="generate_new_link")
        ],
        [
            types.InlineKeyboardButton(text=lang_data["buttons"]["back"], callback_data="main_menu")
        ]
    ])

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
