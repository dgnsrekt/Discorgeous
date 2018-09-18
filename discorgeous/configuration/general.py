import toml
import structlog
from discorgeous.paths import GENERAL_CONFIGURATION_PATH


class InvalidSettingError(ValueError):
    pass


class DefaultConfigurationSection:
    DEFAULT_CONFIG = dict()

    def __init__(self, subclass, **kwargs):
        self.key = subclass.__class__.__name__
        self.value = kwargs
        DefaultConfigurationSection.DEFAULT_CONFIG[self.key] = self.value

    def __repr__(self):
        return f"{self.key}: {self.value}"


class General(DefaultConfigurationSection):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)


class Configuration:

    General(DEBUG_MODE=False, LANGUAGE="en-au", LOGGING="DEBUG")

    DEFAULT_CONFIG = DefaultConfigurationSection.DEFAULT_CONFIG
    PATH = GENERAL_CONFIGURATION_PATH
    logger = structlog.get_logger()

    def __init__(self):
        self.settings = None
        self.name = self.PATH
        self._check()
        self._load()

    def _check(self):
        self.PATH.parent.mkdir(exist_ok=True)

        if not self.PATH.exists():
            self.logger.info("Configuration file not found.", path=self.PATH)
            self.write_clean_configuration_file()

    def _load(self):
        self.settings = self._readfile()

        self.logger.info("Configuration file loaded.", path=self.PATH)
        for setting in self.settings:
            self.logger.info(f"{setting} settings:", current=self[setting])

    def _readfile(self):
        with open(self.PATH, "r") as file:
            return toml.loads(file.read())

    def write_clean_configuration_file(self):
        with open(self.PATH, "w") as file:
            file.write(toml.dumps(self.DEFAULT_CONFIG))
            self.logger.info("Configuration file cleaned.", path=self.PATH)
        self._load()

    def items(self):
        return self.settings.items()

    def __iter__(self):
        return iter(list(self.settings.keys()))

    def __getitem__(self, section):
        try:
            return self.settings[section]
        except KeyError as e:
            raise InvalidSettingError(
                f"{section} is an invalid configuration key. "
                "Use the following configuration keys: ",
                list(self.settings.keys()),
            )

    def __repr__(self):
        repr = "----CONFIGURATION----\n"
        for key, value in self.settings.items():
            repr += f"{key}: {value}\n"
        return repr
