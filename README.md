SPb Python Bot
==============

The Zen of SPb Python Chat
--------------------------

```python
import this
```

[Read Zen of SPb Python Chat](https://github.com/spbpython/orgs-wiki/blob/master/chat/this.md)


Hello world
-----------

```python
import __hello__ 
``` 

Let me google for you
---------------------

### Google

```
/google query
/g query
```

### Wiki 

```
/wiki query
/w query
```

PEPs link
---------

Match peps in messages and send links for them.


Environment variables
---------------------

```basg
BOT_TOKEN  # telegram bot token
BOT_LOGGING_LEVEL  # logging level
SHOW_PEP_INFO  # match PEPs in messages
MODERATORS  # moderators identifiers splited by space
DEBUG  # bot autoreload on file save
```

Run with condo
--------------
[Condo](https://github.com/prepor/condo) — reliable and simple idempotent supervisor for Docker containers.


```edn
{
    :spec {
        :Name "spb_python_bot"
        :Image "nonamenix/spb_python_bot:latest"
        :Env [
            "BOT_TOKEN=339614247:************************************"
            "MODERATORS=132982472 59323058"
            "BOT_LOGGING_LEVEL=ERROR"
        ]
        :HostConfig {
            :RestartPolicy {:Name "always"}
            :NetworkMode "petprojects_default"
        }
    }

    :health-timeout 45
}
```
