import logging

logging.basicConfig(
    filename="logfile.log", filemode="w", format="%(levelname)s %(asctime)s - %(message)s", level=logging.ERROR
)

logging.error("This is an error message")
logging.warning("This is a warning message")
logging.info("This is an info message")
logging.debug("This is a debug message")
logger = logging.getLogger()
