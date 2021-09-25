from logging import StreamHandler, getLogger, Logger, INFO
from os import getenv

_handler = StreamHandler()


def create_logger(name: str) -> Logger:
    if getenv("DISABLE_LOGGING") in ("1", "TRUE", "True", "true"):
        return FakeLogger(name)

    logger = getLogger(name)
    logger.addHandler(_handler)
    logger.setLevel(INFO)

    return logger


class FakeLogger(Logger):  # pragma: no cover
    def critical(self, *args, **kwargs) -> None:
        pass

    def error(self, *args, **kwargs) -> None:
        pass

    def warning(self, *args, **kwargs) -> None:
        pass

    def info(self, *args, **kwargs) -> None:
        pass

    def debug(*args, **kwargs) -> None:
        pass
