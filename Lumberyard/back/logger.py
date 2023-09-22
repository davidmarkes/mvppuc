import logging

logger = logging.getLogger("lumberyard_api")
handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

