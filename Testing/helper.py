import logging

logger = logging.getLogger(__name__)


sh = logging.StreamHandler()
fileh = logging.FileHandler("file.log")

sh.setLevel(logging.WARNING)
fileh.setLevel(logging.ERROR)

formatter = logging.Formatter("%(name)s-%(levelname)s-%(message)s")
sh.setFormatter(formatter)
fileh.setFormatter(formatter)

logger.addHandler(sh)
logger.addHandler(fileh)

logger.warning("this warning")
logger.error("this error")
