from __future__ import absolute_import

import bottle

from botbits.bot import Bot


def main():
    bot = Bot()
    bot.start()

    application = bottle.Bottle()
    bottle.post(path="/webhooks/<name>", callback=bot.webhook)
    bottle.run(application, host='localhost', port=8080)


if __name__ == "__main__":
    main()
