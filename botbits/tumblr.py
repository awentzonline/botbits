import pytumblr
from geventirc.message import PrivMsg

from .conf import settings
from .handlers import MessageMatcher


class TumblrYouTubePoster(MessageMatcher):
    pattern = r"(https?://www.youtube.com/watch?[^ ]+)"

    def __init__(self, blog, *args, **kwargs):
        self.blog = blog
        super(TumblrYouTubePoster, self).__init__(*args, **kwargs)

    def get_tumblr_client(self):
        if not hasattr(self, "_tumblr_client"):
            conf = settings.TUMBLR
            self._tumblr_client = pytumblr.TumblrRestClient(
                conf["CONSUMER_KEY"], conf["CONSUMER_SECRET"],
                conf["TOKEN_KEY"], conf["TOKEN_SECRET"])
        return self._tumblr_client

    def on_match(self, match, client, msg, channel, content):
        tumblr = self.get_tumblr_client()
        url = match.group(0)
        caption = content.replace(url, "").strip()
        client.send_message(
            PrivMsg(channel, "Posting {}: {}".format(caption, url)))
        tumblr.create_video(self.blog, embed=url, caption=caption)
