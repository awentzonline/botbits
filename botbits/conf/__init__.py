import importlib
import os

import default_settings


SETTINGS_MODULE_ENV_VAR = "BOTBITS_SETTINGS_MODULE"


class ModuleSettings(object):
    """Settings loaded from a specified python module."""
    def __init__(self):
        self._wrapped = None

    def _setup(self):
        try:
            settings_module_name = os.environ[SETTINGS_MODULE_ENV_VAR]
            if not settings_module_name:  # set but blank
                raise KeyError
        except KeyError:
            raise Exception(
                "Settings module not configured. Please define `{}`.".format(
                    SETTINGS_MODULE_ENV_VAR))
        self._wrapped = Settings(settings_module_name)

    def __getattr__(self, name):
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, name)


class Settings(object):
    def __init__(self, settings_module_name):
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))
        mod = importlib.import_module(settings_module_name)
        for setting in dir(mod):
            if setting.isupper():
                setattr(self, setting, getattr(mod, setting))


settings = ModuleSettings()
