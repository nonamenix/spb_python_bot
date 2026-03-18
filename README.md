SPb Python Bot
==============

![spbpython bot status](https://healthchecks.io/badge/67e18dff-5605-4a51-9792-2f8614/REOpd_Jz/spbpython.svg) [![tag](https://img.shields.io/github/tag/nonamenix/spb_python_bot.svg)](./CHANGELOG.md)


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

Команда разрешена только для модератора

```text
/google query
/g query
/wiki query
/w query
```

PEPs link
---------

Match peps in messages and send links for them.

Chats
-----

Показывает чаты и ссылки

```text
/chats
/links
/about
```

Other commands
--------------

```text
/version   — show current bot version
/ping      — moderator-only ping/pong check
/rules     — show all chat rules (also: /zen, import this)
```

Environment variables
---------------------

```bash
BOT_TOKEN              # telegram bot token (required)
BOT_LOGGING_LEVEL      # logging level: DEBUG, INFO, WARNING, ERROR (default: DEBUG)
MODERATORS             # moderator Telegram user IDs separated by spaces
HEALTHCHECKIO_TOKEN    # healthcheck.io ping token (optional)
```

See [.env.example](.env.example) for a ready-to-use template.

Run with Docker
---------------

**Build and run locally:**

```bash
cp .env.example .env
# edit .env and set BOT_TOKEN
docker compose up --build
```

**Deploy to a remote server:**

The image is built and pushed to GitHub Container Registry on every push to `master`.

```bash
# Copy deploy/docker-compose.yml and .env to the server, then:
DEPLOY_HOST=user@yourserver ./deploy/deploy.sh
```

Or manually on the server:

```bash
docker compose pull
docker compose up -d
```
