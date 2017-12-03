import os
from datetime import timedelta, datetime

from urllib.parse import quote

from aiotg import Chat, aiohttp
from bot import Bot
import logging

# Logging
logging.basicConfig(
    level=getattr(logging, os.environ.get('BOT_LOGGING_LEVEL', 'DEBUG')),
    format='%(asctime)s | %(name)s | %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

DEBUG = "DEBUG" in os.environ


def get_moderators():
    moderators = [
        132982472,  # nonamenix
        59323058  # lig11
    ]
    try:
        moderators = os.environ['MODERATORS']
    except KeyError:
        pass
    else:
        moderators = [int(m.strip()) for m in moderators.split(' ')]
    logger.info(moderators)
    return moderators


bot = Bot(
    api_token=os.environ["BOT_TOKEN"],
    moderators=get_moderators()
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


@bot.moderator_command("/?ping")
async def ping(chat, message):
    await chat.reply("pong")


@bot.command("/?import __hello__")
async def hello(chat: Chat, message):
    await chat.reply("Hello world")


@bot.command("/rules")
@bot.command("/?import this")
@bot.command("/?import __this__")
@bot.command("\`import __this__\`")
@no_more_than_once_every(interval=timedelta(minutes=5), key='zen_of_chat')
async def zen(chat: Chat, message):
    # TODO: fetch it from chat_zen_url = "https://raw.githubusercontent.com/spbpython/orgs-wiki/master/chat/this.md"

    await chat.reply("""
*The Zen of SPb Python Chat*
_(Inspired by "The Zen of Python, by Tim Peters")_

- Short introduction of yourself is better than "hello".
- Link to gist is better than source paste.
- One long message is better than many short.
- Editing the message is better than correcting via another one.
- Staying on topic is better than offtopic.
- Good topic is worth discussing though.
- Unless it is started by a link to Habrahabr.
- Politeness counts.
- Bad mood is not a good reason to break the rules.
- Don't ask to ask just ask.
- Text message is better than voice message.
- Unless it is voice conference.
- Git repos are one honking great idea — let's do more of those!
""", parse_mode="Markdown")


def reply_with_let_me_search_for_you(chat: Chat, search_url: str, query: str):
    return chat.send_text(
        search_url.format(query=quote(query)),
        reply_to_message_id=chat.message["message_id"],
        disable_web_page_preview='true',
    )


@bot.moderator_command("/g (?P<query>.+)")
@bot.moderator_command("/google (?P<query>.+)")
async def google(chat: Chat, matched):
    await reply_with_let_me_search_for_you(
        chat,
        search_url="https://www.google.ru/search?q={query}",
        query=matched.group('query')
    )


@bot.moderator_command("/w (?P<query>.+)")
@bot.moderator_command("/wiki (?P<query>.+)")
async def wiki(chat: Chat, matched):
    await reply_with_let_me_search_for_you(
        chat,
        search_url="https://en.wikipedia.org/w/index.php?search={query}",
        query=matched.group('query')
    )


pep_link = "https://www.python.org/dev/peps/pep-{0:04d}/"


async def is_pep_exists(pep):
    async with aiohttp.ClientSession() as session:
        async with session.get(pep_link.format(pep)) as resp:
            return resp.status == 200


@bot.command("\#.*pep-?(?P<pep>\d{1,4})")
async def peps(chat: Chat, matched):
    try:
        pep = int(matched.group('pep'))
    except ValueError:
        pass
    else:
        if await is_pep_exists(pep):
            await chat.send_text(pep_link.format(pep), reply_to_message_id=chat.message["message_id"])


if __name__ == "__main__":
    logger.info("Running...")
    bot.run(debug=DEBUG)
