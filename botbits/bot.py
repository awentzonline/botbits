from geventirc import Client, handlers, message

from .conf import settings


class BaseBot(object):
    """Derive your hateful new robot from this class."""
    def start(self):
        self.nick = settings.NICK
        self.host = settings.HOST
        self.port = settings.PORT
        password = getattr(settings, "PASSWORD", None)
        irc = self.irc = Client(self.host, self.nick, port=self.port)
        if password:
            irc.send_message(message.Pass(password))
        # required handlers
        irc.add_handler(handlers.ping_handler, "PING")
        channels = settings.CHANNELS
        self.join_channels(channels)

        self.add_handlers()

        irc.start()

    def wait(self):
        """Block until irc ends somehow."""
        self.irc.join()

    def join_channels(self, channels):
        for channel in channels:
            self.irc.add_handler(handlers.JoinHandler(channel))

    def add_handlers(self):
        pass
