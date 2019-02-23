chat_rules_header = """
*The Zen of SPb Python Chat*
_(Inspired by "The Zen of Python, by Tim Peters")_
"""


rule_not_found = """
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: cannot import name '{}'
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
    [[], ["Politeness counts."]],  # from this import politeness
    [
        [],  # from this import bad_mood
        ["Bad mood is not a good reason to break the rules."],
    ],
    [["ask"], ["Don't ask to ask just ask."]],  # from this import ask
    [
        [],  # from this import voice
        [
            "Text message is better than voice message.",
            "Unless it is voice conference.",
        ],
    ],
    [[], ["Git repos are one honking great idea — let's do more of those!"]],
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
