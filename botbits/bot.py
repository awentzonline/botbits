import importlib

from geventirc import Client, handlers, message


class Bot(object):

    def __init__(self, settings):
        self.settings = settings

    """Derive your hateful new robot from this class."""
    def start(self):
        self.nick = self.settings["nick"]
        self.host = self.settings["host"]
        self.port = self.settings.get("port", 6667)
        password = self.settings.get("password")
        irc = self.irc = Client(self.host, self.nick, port=self.port)
        if password:
            irc.send_message(message.Pass(password))
        # required handlers
        irc.add_handler(handlers.ping_handler, "PING")
        channels = self.settings["channels"]
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
        self.irc.add_handler(handlers.print_handler)
        for handler_path, handler_settings in self.settings.get("handlers", {}).items():
            class_data = handler_path.split(".")
            module_path = ".".join(class_data[:-1])
            class_str = class_data[-1]

            handler_module = importlib.import_module(module_path)

            handler_cls = getattr(handler_module, class_str)
            handler = handler_cls(**handler_settings)
            self.irc.add_handler(handler)

    def webhook(self, name):
        # remote_addr = bottle.request.headers.get('X-Forwarded-For') or bottle.request.remote_addr
        # if name in bot.webhooks and bottle.request.json:
        #     self.webooks[name].call(bottle.request.json, remote_addr=remote_addr)
        return "HOOKED: {}".format(name)
