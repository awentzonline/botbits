from gevent.monkey import patch_all; patch_all()  # noqa

from botbits.bot import BaseBot
from botbits.conf import settings
from botbits.handlers import BadWordKicker
from botbits.twitter import TwitterQuotePoster
from geventirc import handlers


class Bot(BaseBot):
    """Beep boop"""
    def add_handlers(self):
        # optional handlers
        twitter_conf = getattr(settings, "TWITTER", None)
        if twitter_conf:
            self.irc.add_handler(TwitterQuotePoster(twitter_conf))
        bad_words = getattr(settings, "BAD_WORDS", ("kickme",))
        if bad_words:
            self.irc.add_handler(
                BadWordKicker(bad_words, ignore_users=[self.nick]))
        self.irc.add_handler(handlers.print_handler)


if __name__ == "__main__":
    import os
    from botbits.conf import SETTINGS_MODULE_ENV_VAR

    os.environ[SETTINGS_MODULE_ENV_VAR] = "example.example_settings"
    bot = Bot()
    bot.start()
    try:
        bot.wait()
    except KeyboardInterrupt:
        pass
