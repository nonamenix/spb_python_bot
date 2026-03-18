import asyncio
import logging
import os
import re
from datetime import timedelta, datetime
from urllib.parse import quote

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message

import content

logging.basicConfig(
    level=getattr(logging, os.environ.get("BOT_LOGGING_LEVEL", "DEBUG")),
    format="%(asctime)s | %(name)s | %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

VERSION_URL = "https://img.shields.io/github/tag/nonamenix/spb_python_bot.json"
HEALTHCHECKIO_URL = "https://hchk.io/{token}"
HEALTHCHECKIO_INTERVAL = 150
USER_AGENT = "SPbPython / 0.5.10"

flatten = lambda l: [item for sublist in l for item in sublist]


def get_moderators():
    try:
        moderators = [int(m.strip()) for m in os.environ["MODERATORS"].split(" ")]
    except KeyError:
        moderators = [132982472]  # nonamenix 
    logger.info("Moderators: %s", moderators)
    return moderators


MODERATORS = get_moderators()


class ModeratorFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user is not None and message.from_user.id in MODERATORS


def make_zen_md(rules, wrap=False):
    rules = ["- {}".format(rule) for rule in rules]
    if wrap:
        rules.insert(0, "...")
        rules.append("...")
    return "\n".join([content.chat_rules_header, *rules])


def no_more_than_once_every(interval=timedelta(minutes=5), key: str = None):
    restrictions = {}

    def actual_decorator(func):
        async def wrapper(message: Message):
            now = datetime.now()
            if key not in restrictions or now > restrictions[key]:
                restrictions[key] = now + interval
                await func(message)

        return wrapper

    return actual_decorator


bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher()


async def still_alive():
    token = os.environ.get("HEALTHCHECKIO_TOKEN")
    if not token:
        return
    while True:
        try:
            async with aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as session:
                await session.get(HEALTHCHECKIO_URL.format(token=token))
        except Exception as e:
            logger.error("Healthcheck ping failed: %s", e)
        await asyncio.sleep(HEALTHCHECKIO_INTERVAL)


@dp.message(Command("version"))
async def version(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(VERSION_URL) as resp:
            data = await resp.json()
            await message.reply("version: {}".format(data["value"]))


@dp.message(Command("ping"), ModeratorFilter())
async def ping(message: Message):
    await message.reply("pong")


@dp.message(F.text.regexp(r"^/?import __hello__$"))
async def hello(message: Message):
    await message.reply("Hello world")


@dp.message(F.text.regexp(r"^/?help\(this\)$"))
async def rule_help(message: Message):
    body = []
    for keys, rules in content.rules:
        if len(keys) > 0:
            row = ">>> from this import {}".format(keys[0])
            if len(keys) > 1:
                row += "  # {}".format(", ".join(keys[1:]))
            body.append(row)
            body.extend(rules)
            body.append("")
    await message.reply(
        content.help_test.format(examples="\n".join(body)), parse_mode="Markdown"
    )


@dp.message(F.text.regexp(r"^/?from this import (?P<key>.+)"))
async def rule_of_zen(message: Message):
    m = re.search(r"^/?from this import (?P<key>.+)", message.text)
    key = m.group("key")
    matching = [rules for keys, rules in content.rules if key in keys]
    if not matching or not matching[0]:
        await message.reply(content.rule_not_found.format(key), parse_mode="Markdown")
        return
    await message.reply(make_zen_md(matching[0], wrap=True), parse_mode="Markdown")


@dp.message(F.text.regexp(r"^/?(rules|zen|import this)$"))
@no_more_than_once_every(interval=timedelta(minutes=5), key="zen_of_chat")
async def zen(message: Message):
    await message.reply(
        make_zen_md(flatten([rules for _, rules in content.rules])),
        parse_mode="Markdown",
    )


async def reply_with_let_me_search_for_you(message: Message, search_url: str, query: str):
    await message.reply(
        search_url.format(query=quote(query)),
        disable_web_page_preview=True,
    )


@dp.message(F.text.regexp(r"^/?(g|google) (?P<query>.+)"), ModeratorFilter())
async def google(message: Message):
    m = re.search(r"^/?(g|google) (?P<query>.+)", message.text)
    await reply_with_let_me_search_for_you(
        message,
        search_url="https://www.google.ru/search?q={query}",
        query=m.group("query"),
    )


@dp.message(F.text.regexp(r"^/?(w|wiki) (?P<query>.+)"), ModeratorFilter())
async def wiki(message: Message):
    m = re.search(r"^/?(w|wiki) (?P<query>.+)", message.text)
    await reply_with_let_me_search_for_you(
        message,
        search_url="https://en.wikipedia.org/w/index.php?search={query}",
        query=m.group("query"),
    )


pep_link = "https://www.python.org/dev/peps/pep-{0:04d}/"


async def is_pep_exists(pep):
    async with aiohttp.ClientSession() as session:
        async with session.get(pep_link.format(pep)) as resp:
            return resp.status == 200


@dp.message(F.text.regexp(re.compile(r"\#.*pep-?\d{1,4}", re.IGNORECASE)))
async def peps(message: Message):
    m = re.search(r"\#.*pep-?(\d{1,4})", message.text, re.IGNORECASE)
    if not m:
        return
    try:
        pep = int(m.group(1))
    except ValueError:
        return
    if await is_pep_exists(pep):
        await message.reply(pep_link.format(pep))


@dp.message(Command(commands=["about", "chats", "links"]))
async def chats(message: Message):
    await message.reply(
        """
*SPb Python Chats and Channels:*
- [News Channel](https://t.me/spbpythonnews)
- [Main chat](https://t.me/+S0GjOFmLIyBjZWYy)
- [Drinkup & Bar Hopping](https://t.me/joinchat/BA9zxD_Df8rTlNpiXhDSig)""",
        parse_mode="Markdown",
    )


async def main():
    asyncio.create_task(still_alive())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Running...")
    asyncio.run(main())
