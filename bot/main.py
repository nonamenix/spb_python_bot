import os

from aiotg import Bot, Chat, aiohttp
import logging

# Logging
logging.basicConfig(
    level=getattr(logging, os.environ.get('BOT_LOGGING_LEVEL', 'DEBUG')),
    format='%(asctime)s | %(name)s | %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

show_pep_info = os.environ.get("SHOW_PEP_INFO", True)

bot = Bot(
    api_token=os.environ["BOT_TOKEN"],
)


def send_code(chat: Chat, text: str):
    """Wrap text to code snippet and send as answer"""
    return chat.reply("```{}```".format(text), parse_mode="Markdown")


if show_pep_info:
    pep_link = "https://www.python.org/dev/peps/pep-{0:04d}/"


    async def is_pep_exists(pep):
        async with aiohttp.ClientSession() as session:
            async with session.get(pep_link.format(pep)) as resp:
                return resp.status == 200


    @bot.command(".*pep-?(?P<pep>\d{1,4})")
    async def peps(chat: Chat, matched):
        try:
            pep = int(matched.group('pep'))
        except ValueError:
            pass
        else:
            if await is_pep_exists(pep):
                await chat.send_text(pep_link.format(pep), reply_to_message_id=chat.message["message_id"])


@bot.command("/?ping")
async def ping(chat, message):
    await chat.reply("pong")


@bot.command("/?import __hello__")
async def hello(chat: Chat, message):
    await send_code(chat, " Hello world")


@bot.command("/?import this")
async def zen(chat: Chat, message):
    # TODO: fetch it from chat_zen_url = "https://raw.githubusercontent.com/spbpython/orgs-wiki/master/chat/this.md"
    await chat.send_chat_action('typing')
    await send_code(chat, """
# The Zen of SPb Python Chat
*(Inspired by "The Zen of Python, by Tim Peters")*

- Short inroduction of yourself is better than "hello".
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
- Git repos are one honking great idea -- let's do more of those!
""")


if __name__ == "__main__":
    logger.info("Running...")
    bot.run()
