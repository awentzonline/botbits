import os
import yaml


BOTBITS_CONF = "BOTBITS_CONF"


class NonprintableLoader(yaml.Loader):
    def check_printable(self, data):
        return True


class LazySettings(object):

    def __init__(self, filename=None):
        self._config = None

    def __getitem__(self, name):
        if self._config is None:
            with open(os.environ.get(BOTBITS_CONF, "botconf.yml"), "rb") as stream:
                self._config = yaml.load(stream, NonprintableLoader)
        return self._config.__getitem__(name)

    def get(self, name, default=None):
        try:
            return self.__getitem__(name)
        except IndexError:
            return default


settings = LazySettings()
