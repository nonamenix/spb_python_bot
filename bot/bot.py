from typing import List

from aiotg import Bot as BaseBot, API_TIMEOUT, Chat, asyncio, aiohttp
import re

USER_AGENT = "SPbPython / 0.5.10"


class Bot(BaseBot):
    healthcheckio_url = "https://hchk.io/{token}"
    healthcheckio_interval = 150  # seconds
    healthcheckio_token = None

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


    

    async def still_alive(self):
        async with aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as session:
            await session.get(
                self.healthcheckio_url.format(token=self.healthcheckio_token)
            )

        await asyncio.sleep(self.healthcheckio_interval)
        await self.still_alive()



    def run(self, debug=False, reload=None):
        if self.healthcheckio_token is not None:
            loop = asyncio.get_event_loop()
            loop.create_task(self.still_alive())

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
