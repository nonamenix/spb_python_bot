from typing import List

from aiotg import Bot as BaseBot, API_TIMEOUT, Chat
import re


class Bot(BaseBot):
    def __init__(self, api_token: str, moderators: List[int],
                 api_timeout: int = API_TIMEOUT,
                 botan_token=None,
                 name=None):
        super(Bot, self).__init__(
            api_token=api_token,
            api_timeout=api_timeout,
            botan_token=botan_token,
            name=name
        )

        self.moderators = moderators
        self._moderators_commands = []

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

        if message['from']['id'] in self.moderators and 'text' in message:
            for patterns, handler in self._moderators_commands:
                m = re.search(patterns, message["text"], re.I)
                if m:
                    self.track(message, handler.__name__)
                    return handler(chat, m)

        handler = super(Bot, self)._process_message(message)

        return handler
