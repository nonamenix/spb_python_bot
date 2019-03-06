from typing import List

from aiotg import Bot as BaseBot, API_TIMEOUT, Chat, asyncio, aiohttp
import motor.motor_asyncio
import re

USER_AGENT = "SPbPython / 0.5.10"


class Bot(BaseBot):
    healthcheckio_url = "https://hchk.io/{token}"
    healthcheckio_interval = 150  # seconds
    healthcheckio_token = None

    mongo_healthcheckio_token = None
    mongodb = None
    mongo_healthcheckio_interval = 1800
    mongo_max_db_size = 512 * 1024 * 1024  # mlab.com free limitation
    mongo_alert_on_fullness = 0.5
    saved_updates_kinds = [
        "message",
        "edited_message",
        "inline_query",
        "chosen_inline_result",
        "callback_query",
    ]

    def __init__(
        self,
        api_token: str,
        moderators: List[int],
        api_timeout: int = API_TIMEOUT,
        botan_token: str = None,
        healthcheckio_token: str = None,
        mongo_url=None,
        mongo_healthcheckio_token=None,
        name=None,
    ):
        super(Bot, self).__init__(
            api_token=api_token,
            api_timeout=api_timeout,
            botan_token=botan_token,
            name=name,
        )
        self.healthcheckio_token = healthcheckio_token
        self.moderators = moderators
        self._moderators_commands = []

        if mongo_url is not None:
            mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
            self.mongodb = mongo_client[mongo_url.split("/")[-1]]
            self.mongo_healthcheckio_token = mongo_healthcheckio_token

    async def save_update_to_mongo(self, update):
        collection = list(set(self.saved_updates_kinds).intersection(update.keys()))[0]
        if self.mongodb is not None:
            await self.mongodb[collection].insert_one(update)

    async def still_alive(self):
        async with aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as session:
            await session.get(
                self.healthcheckio_url.format(token=self.healthcheckio_token)
            )

        await asyncio.sleep(self.healthcheckio_interval)
        await self.still_alive()

    async def mongo_still_enough(self):
        stats = await self.mongodb.command("dbstats")
        file_size = stats["fileSize"]

        fullness = file_size / self.mongo_max_db_size
        user_agent = "SPbPython - {}%".format(fullness * 100)

        if fullness <= self.mongo_alert_on_fullness:
            async with aiohttp.ClientSession(
                headers={"User-Agent": user_agent}
            ) as session:
                await session.get(
                    self.healthcheckio_url.format(token=self.mongo_healthcheckio_token)
                )

        await asyncio.sleep(self.mongo_healthcheckio_interval)
        await self.mongo_still_enough()

    def run(self, debug=False, reload=None):
        if self.healthcheckio_token or self.mongo_healthcheckio_token:
            loop = asyncio.get_event_loop()

            if self.healthcheckio_token is not None:
                loop.create_task(self.still_alive())

            if self.mongo_healthcheckio_token is not None:
                loop.create_task(self.mongo_still_enough())

        super(Bot, self).run(debug=debug, reload=reload)

    def add_moderators_command(self, regexp, fn):
        """
        Manually register regexp based command
        """
        self._moderators_commands.append((regexp, fn))

    def moderator_command(self, regexp):
        """
        Register a new command that allowed only for moderators

        :param str regexp: Regular expression matching the command to register

        :Example:

        >>> @bot.moderator_command(r"/echo (.+)")
        >>> def echo(chat, match):
        >>>     return chat.reply(match.group(1))
        """

        def decorator(fn):
            self.add_moderators_command(regexp, fn)
            return fn

        return decorator

    def _process_message(self, message):

        chat = Chat.from_message(self, message)

        if (
            "text" in message
            and "from" in message
            and message["from"]["id"] in self.moderators
        ):
            for patterns, handler in self._moderators_commands:
                m = re.search(patterns, message["text"], re.I)
                if m:
                    self.track(message, handler.__name__)
                    return handler(chat, m)

        handler = super(Bot, self)._process_message(message)

        return handler

    def _process_update(self, update):
        if self.mongodb is not None:
            loop = asyncio.get_event_loop()
            loop.create_task(self.save_update_to_mongo(update))

        super(Bot, self)._process_update(update)
