

chat_rules_header = """
*The Zen of SPb Python Chat*
_(Inspired by "The Zen of Python, by Tim Peters")_
"""


rule_not_found = """
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: cannot import name '{}'```
"""


rules = [
    [
        ["hi", "hello", "intro"],  # from this import hi
        ['Short introduction of yourself is better than "hello".'],
    ],
    [
        ["gist", "source"],  # from this import gist
        ["Link to gist is better than source paste."],
    ],
    [
        ["spam", "long_better"],  # from this import long_message
        ["One long message is better than many short."],
    ],
    [
        ["edit", "correct"],  # from this import correct
        ["Editing the message is better than correcting via another one."],
    ],
    [
        ["topic", "offtopic"],  # from this import offtopic
        [
            "Staying on topic is better than offtopic.",
            "Good topic is worth discussing though.",
            "Unless it is started by a link to Habrahabr.",
        ],
    ],
    [["politeness"], ["Politeness counts."]],  # from this import politeness
    [
        ["mood"],  # from this import bad_mood
        ["Bad mood is not a good reason to break the rules."],
    ],
    [["ask"], ["Don't ask to ask just ask."]],  # from this import ask
    [
        ["voice"],  # from this import voice
        [
            "Text message is better than voice message.",
            "Unless it is voice conference.",
        ],
    ],
    [["git"], ["Git repos are one honking great idea — let's do more of those!"]],
]

help_test = """
Help on module this: 

*NAME*
    this

*EXAMPLES*

```
{examples}
```
"""

about_chat = """
*SPb Python Chats and Channels*    

- [News Channel](https://t.me/spbpythonnews)
- [Main chat](https://t.me/spbpython)
- [Site](https://spbpython.guru/)
- [Drinkup & Bar Hopping](https://t.me/joinchat/BA9zxD_Df8rTlNpiXhDSig) 
- [Biking](https://t.me/joinchat/B-0myFDmUqDvwWU4e58WQw)
- [IT-FIT](https://t.me/joinchat/B-0myE_XfRFQvoLiVscDGQ)
- [Facebook Group](https://www.facebook.com/groups/spbpython/) and [Page](https://www.facebook.com/spbpython/)
- [Meetup.com](https://www.meetup.com/ru-RU/spbpython/)
"""

def make_zen_md(rules, wrap=False):
    rules = ["- {}".format(rule) for rule in rules]

    if wrap:
        rules.insert(0, "...")
        rules.append("...")

    return "\n".join([chat_rules_header, *rules])


inline_commands = (
    "/version", "import __hello__", "import this", "zen", "/about", "from this import"
)


def make_queries_from_rules(rules):
    return [
        f"from this import {keys[0]}" for keys, _ in rules
    ]

import_queries = make_queries_from_rules(rules)
