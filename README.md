SPb Python Bot
==============

[![spbpython bot status](https://healthchecks.io/badge/67e18dff-5605-4a51-9792-2f8614/REOpd_Jz/spbpython.svg)](https://t.me/spb_python_bot) [![tag](https://img.shields.io/github/tag/nonamenix/spb_python_bot.svg)](./CHANGELOG.md)


The Zen of SPb Python Chat
--------------------------

```python
import this
```

[Read Zen of SPb Python Chat](https://github.com/spbpython/orgs-wiki/blob/master/chat/this.md)

### Help with `this`
```python
help(this)

>>> from this import hi  # hello, intro
Short introduction of yourself is better than "hello".

>>> from this import gist  # source
Link to gist is better than source paste.

>>> from this import spam  # long_better
One long message is better than many short.

>>> from this import edit  # correct
Editing the message is better than correcting via another one.

>>> from this import topic  # offtopic
Staying on topic is better than offtopic.
Good topic is worth discussing though.
Unless it is started by a link to Habrahabr.

>>> from this import ask
Don't ask to ask just ask.
```

Hello world
-----------

```python
import __hello__ 
``` 

Let me google for you
---------------------

### Google

Команда разрешена только для модератора

```
/google query
/g query
```

### Wiki 

Команда разрешена только для модератора

```
/wiki query
/w query
```

PEPs link
---------

Match peps in messages and send links for them.


### Chats

Показывает чаты и ссылки

```
/chats
/links
```

How to run
----------

```bash
BOT_TOKEN  # telegram bot token
BOT_LOGGING_LEVEL  # logging level
MODERATORS  # moderators identifiers splited by space
DEBUG  # bot autoreload on file save
```

Put it to `.env` file and run with do `docker-compose up`