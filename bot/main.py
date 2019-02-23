import os
import logging
from datetime import timedelta, datetime
from urllib.parse import quote

from aiotg import Chat, aiohttp

from bot import Bot
import content

# Logging
logging.basicConfig(
    level=getattr(logging, os.environ.get("BOT_LOGGING_LEVEL", "DEBUG")),
    format="%(asctime)s | %(name)s | %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

DEBUG = "DEBUG" in os.environ
VERSION_URL = "https://img.shields.io/github/tag/nonamenix/spb_python_bot.json"


flatten = lambda l: [item for sublist in l for item in sublist]


def make_zen_md(rules, wrap=False):
    rules = ["- {}".format(rule) for rule in rules]

    if wrap:
        rules.insert(0, "...")
        rules.append("...")

    return "\n".join([content.chat_rules_header, *rules])


def get_moderators():
    moderators = [132982472, 59323058]  # nonamenix  # lig11
    try:
        moderators = os.environ["MODERATORS"]
    except KeyError:
        pass
    else:
        moderators = [int(m.strip()) for m in moderators.split(" ")]
    logger.info("Moderators: %s", moderators)
    return moderators


# spb_python_bot
bot = Bot(
    api_token=os.environ["BOT_TOKEN"],
    healthcheckio_token=os.environ["HEALTHCHECKIO_TOKEN"],
    moderators=get_moderators(),
    mongo_url=os.environ.get("MONGO_URL"),
    mongo_healthcheckio_token=os.environ.get("MONGO_HEALTHCHECKIO_TOKEN"),
)


def no_more_than_once_every(interval=timedelta(minutes=5), key: str = None):
    restrictions = {}

    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            try:
                restriction = restrictions[key]
            except KeyError:
                restrictions[key] = datetime.now() + interval
                result = func(*args, **kwargs)
            else:
                if datetime.now() > restriction:
                    restrictions[key] = datetime.now() + interval
                    result = func(*args, **kwargs)

            return result

        return wrapper

    return actual_decorator


@bot.command("/version")
async def version(chat, message):
    async with aiohttp.ClientSession() as session:
        async with session.get(VERSION_URL) as resp:
            data = await resp.json()
            version = data["value"]
            await chat.reply("version: {}".format(version))


@bot.moderator_command("/?ping$")
async def ping(chat, message):
    await chat.reply("pong")


@bot.command("/?import __hello__")
async def hello(chat: Chat, message):
    await chat.reply("Hello world")


@bot.command("/?help\(this\)")
async def rule_help(chat: Chat, message):
    body = []
    for keys, rules in content.rules:
        if len(keys) > 0:
            row = ">>> from this import {}".format(keys[0])
            if len(keys) > 1:
                row += "  # {}".format(", ".join(keys[1:]))
            body.append(row)
            body.extend(rules)
            body.append("")

    await chat.reply(
        content.help_test.format(examples="\n".join(body)), parse_mode="Markdown"
    )


@bot.command("/?from this import (?P<key>.+)")
async def rule_of_zen(chat: Chat, matched):
    key = matched.group("key")
    rules = [rules for keys, rules in content.rules if key in keys][0]

    if len(rules) > 0:
        await chat.reply(make_zen_md(rules, wrap=True), parse_mode="Markdown")
    else:
        await chat.reply(content.rule_not_found.format(key), parse_mode="Markdown")


@bot.command("/?rules")
@bot.command("/?zen")
@bot.command("/?import this")
@no_more_than_once_every(interval=timedelta(minutes=5), key="zen_of_chat")
async def zen(chat: Chat, message):
    # TODO: fetch it from chat_zen_url = "https://raw.githubusercontent.com/spbpython/orgs-wiki/master/chat/this.md"

    await chat.reply(
        make_zen_md(flatten([rules for _, rules in content.rules])),
        parse_mode="Markdown",
    )


def reply_with_let_me_search_for_you(chat: Chat, search_url: str, query: str):
    return chat.send_text(
        search_url.format(query=quote(query)),
        reply_to_message_id=chat.message["message_id"],
        disable_web_page_preview="true",
    )


@bot.moderator_command("/g (?P<query>.+)")
@bot.moderator_command("/google (?P<query>.+)")
async def google(chat: Chat, matched):
    await reply_with_let_me_search_for_you(
        chat,
        search_url="https://www.google.ru/search?q={query}",
        query=matched.group("query"),
    )


@bot.moderator_command("/w (?P<query>.+)")
@bot.moderator_command("/wiki (?P<query>.+)")
async def wiki(chat: Chat, matched):
    await reply_with_let_me_search_for_you(
        chat,
        search_url="https://en.wikipedia.org/w/index.php?search={query}",
        query=matched.group("query"),
    )


pep_link = "https://www.python.org/dev/peps/pep-{0:04d}/"


async def is_pep_exists(pep):
    async with aiohttp.ClientSession() as session:
        async with session.get(pep_link.format(pep)) as resp:
            return resp.status == 200


@bot.command("\#.*pep-?(?P<pep>\d{1,4})")
async def peps(chat: Chat, matched):
    try:
        pep = int(matched.group("pep"))
    except ValueError:
        pass
    else:
        if await is_pep_exists(pep):
            await chat.send_text(
                pep_link.format(pep), reply_to_message_id=chat.message["message_id"]
            )


@bot.command("/about")
@bot.command("/chats")
@bot.command("/links")
async def chats(chat: Chat, matched):
    await chat.reply(
        """
*SPb Python Chats and Channels*    

- [News Channel](https://t.me/spbpythonnews)
- [Main chat](https://t.me/spbpython)
- [Site](https://spbpython.guru/)
- [Drinkup & Bar Hopping](https://t.me/joinchat/BA9zxD_Df8rTlNpiXhDSig) 
- [Biking](https://t.me/joinchat/B-0myFDmUqDvwWU4e58WQw)
- [IT-FIT](https://t.me/joinchat/B-0myE_XfRFQvoLiVscDGQ)
- [Facebook Group](https://www.facebook.com/groups/spbpython/) and [Page](https://www.facebook.com/spbpython/)
- [Meetup.com](https://www.meetup.com/ru-RU/spbpython/)""",
        parse_mode="Markdown",
    )


if __name__ == "__main__":
    logger.info("Running...")
    bot.run(debug=DEBUG)
