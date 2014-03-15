import re
from collections import defaultdict

import tweepy

from .conf import settings
from .handlers import MessageHandler


re_quote = re.compile(r'>>.+<<')


class TwitterQuotePoster(MessageHandler):
    """Saves great quotes to twitter for posterity."""
    def __init__(self, twitter_conf, channel_whitelist=[]):
        self.channel_whitelist = channel_whitelist
        self.quotes = defaultdict(set)
        self.num_quotes_to_post = getattr(settings, "NUM_QUOTES_TO_POST", 2)
        self.setup_client(twitter_conf)

    def setup_client(self, conf):
        auth = tweepy.OAuthHandler(
            conf["CONSUMER_KEY"], conf["CONSUMER_SECRET"])
        auth.set_access_token(
            conf["TOKEN_KEY"], conf["TOKEN_SECRET"])
        self.twitter = tweepy.API(auth)

    def handle_message(self, client, msg, channel, content):
        # early out
        if self.channel_whitelist and not channel in self.channel_whitelist:
            return None
        # let's do this
        nick, _, _ = msg.prefix_parts
        quote_match = re_quote.match(content)
        if quote_match:
            user_set = self.quotes[content]
            user_set.add(nick)
            if len(user_set) >= self.num_quotes_to_post:
                self.send_tweet(content)
                del self.quotes[content]

    def send_tweet(self, content):
        self.twitter.update_status(content)
