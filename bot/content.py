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
    [
        ["politeness"],  # from this import politeness
        ["Politeness counts."]
    ],
    [
        ["bad_mood"],  # from this import bad_mood
        ["Bad mood is not a good reason to break the rules."]
    ],
    [
        ["ask"],  # from this import ask
        ["Don't ask to ask just ask."]
    ],
    [
        ["text", "voice"],  # from this import voice
        ["Text message is better than voice message.", "Unless it is voice conference."]
    ],
    [
        [],
        ["Git repos are one honking great idea — let's do more of those!"]
    ],
]