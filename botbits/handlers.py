import random
import re

from geventirc import message

from .commands import Kick


class MessageHandler(object):
    """Makes chat messages simpler to work with?"""
    commands = ["PRIVMSG"]

    def __call__(self, client, msg):
        channel, content = msg.params[0], u" ".join(msg.params[1:])
        self.handle_message(client, msg, channel, content)

    def handle_message(self, client, msg, channel, content):
        raise NotImplementedError("Override `handle_message`")


class MessageMatcher(MessageHandler):
    pattern = None

    def __init__(self, *args, **kwargs):
        self.re_pattern = self.get_re_pattern()
        super(MessageMatcher, *args, **kwargs)

    def get_re_pattern(self):
        return re.compile(self.pattern)

    def handle_message(self, client, msg, channel, content):
        match = self.re_pattern.search(content)
        if match:
            self.on_match(match, client, msg, channel, content)

    def on_match(self, match, client, msg, channel, content):
        raise NotImplementedError("Implement `on_match`")


class SalutationMatcher(MessageMatcher):
    salutations = [
        "hey {}", "hello {}", "que pedo {}?"
    ]

    def __init__(self, nick, *args, **kwargs):
        self.nick = nick
        super(SalutationMatcher, self).__init__(*args, **kwargs)

    def get_re_pattern(self):
        return re.compile(self.nick)

    def on_match(self, match, client, msg, channel, content):
        nick = msg.prefix_parts[0]
        client.send_message(message.PrivMsg(channel, self.get_salutation(nick)))

    def get_salutation(self, target_nick):
        salutation = random.choice(self.salutations)
        return salutation.format(target_nick)


class OperatorHandler(object):

    commands = ['001']

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, client, msg):
        client.send_message(message.Command([self.username, self.password], command="OPER"))


class ModeHandler(object):

    commands = ['002']

    def __init__(self, target, mode, username):
        self.target = target
        self.mode = mode
        self.username = username

    def __call__(self, client, msg):
        client.send_message(message.Command([self.target, self.mode, self.username], command="MODE"))


class BadWordKicker(MessageHandler):
    """Kicks foul-mouthed users"""
    def __init__(self, bad_words, kick_msg="See ya", ignore_users=[]):
        self.bad_words = bad_words
        self.kick_msg = kick_msg
        self.ignore_users = ignore_users

    def handle_message(self, client, msg, channel, content):
        for word in self.bad_words:
            if word in content:
                nick, agent, host = msg.prefix_parts
                client.send_message(
                    Kick(channel, nick, self.kick_msg))
