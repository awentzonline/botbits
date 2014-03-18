from gevent import monkey; monkey.patch_all()  # noqa

import bottle

from botbits.bot import Bot
from botbits.conf import settings


def main():

    for bot_settings in settings.get("bots", []):
        bot = Bot(bot_settings)
        bot.start()

    application = bottle.Bottle()
    # application.post(path="/webhooks/<name>", callback=bot.webhook)
    bottle.run(application, host='localhost', port=8080)

if __name__ == "__main__":
    main()
