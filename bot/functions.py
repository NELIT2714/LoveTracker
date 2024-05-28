async def check_user(callback):
    from bot import mongo

    user = await mongo["users"].find_one({"telegram_id": callback.from_user.id})
    if user is None:
        return await new_user(callback)

    await update_user(callback)
    return user


async def new_user(callback):
    from bot import mongo
    from datetime import datetime

    user = await mongo["users"].find_one({"telegram_id": callback.from_user.id})
    if user is not None:
        return await check_user(callback)

    timestamp = datetime.now().timestamp()
    await mongo["users"].insert_one({
        "telegram_id": int(callback.from_user.id),
        "first_name": str(callback.from_user.first_name),
        "last_name": str(callback.from_user.last_name) if callback.from_user.last_name is not None else None,
        "username": str(callback.from_user.username),
        "language_code": str(callback.from_user.language_code),
        "is_premium": bool(callback.from_user.is_premium),
        "creation_timestamp": int(timestamp),
        "update_timestamp": int(timestamp)
    })
    return check_user(callback)


async def update_user(callback):
    from bot import mongo
    from datetime import datetime

    user = await mongo["users"].find_one({"telegram_id": callback.from_user.id})
    if user is None:
        return await check_user(callback)

    timestamp = datetime.now().timestamp()
    await mongo["users"].update_one(
        {"telegram_id": callback.from_user.id},
        {"$set": {
            "first_name": str(callback.from_user.first_name),
            "last_name": str(callback.from_user.last_name) if callback.from_user.last_name is not None else None,
            "username": str(callback.from_user.username),
            "language_code": str(callback.from_user.language_code),
            "is_premium": bool(callback.from_user.is_premium),
            "update_timestamp": int(timestamp)
        }}
    )
    return True


async def get_lang(callback):
    import yaml
    from bot import mongo

    user = await mongo["users"].find_one({"telegram_id": callback.from_user.id})
    if user is None:
        return

    languages = {
        "ru": "ru_lang.yml"
    }

    lang_file = languages.get(user.get("language_code")) if languages.get(user.get("language_code"), None) is not None \
        else "en_lang.yml"

    with open(f"resources/languages/{lang_file}", "r", encoding="utf-8") as lang_file:
        lang_data = reformat_yaml(yaml.safe_load(lang_file))

    return lang_data


def reformat_yaml(yaml_data):
    lang_data = {}
    for key, value in yaml_data.items():
        if isinstance(value, list):
            result = ""
            for item in value:
                result += str(item) + "\n"
            lang_data[key] = result
        elif isinstance(value, dict):
            lang_data[key] = reformat_yaml(value)
        else:
            lang_data[key] = value
    return lang_data


async def generate_pair_code(length=8):
    import string, random
    from bot import mongo

    pair_codes = await mongo["pairs"].find({}, {"pair_code": 1, "_id": 0}).to_list(length=None)

    characters = string.ascii_letters + string.digits
    pair_code = "".join(random.choice(characters) for i in range(length))

    for item in pair_codes:
        if str(pair_code) == str(item.get("pair_code")):
            return await generate_pair_code()

    return pair_code


async def find_pair(user):
    import asyncio
    from bot import mongo

    user_pair_creator, user_pair_member = await asyncio.gather(
        mongo["pairs"].find_one({"pair_creator": int(user.get("telegram_id"))}),
        mongo["pairs"].find_one({"pair_member": int(user.get("telegram_id"))})
    )
    return [user_pair_creator, user_pair_member]
