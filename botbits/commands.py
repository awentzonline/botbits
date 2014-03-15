from geventirc import message


class Kick(message.Command):
    def __init__(self, channel, nick, reason, prefix=None):
        super(Kick, self).__init__([channel, nick, reason], prefix=prefix)
