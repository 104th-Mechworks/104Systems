import socket

from CLogging import logger


def get_lavalink_status(timeout=10):
    logger.info("Checking lavalink status")
    while True:
        try:
            # Get the lavalink status
            socket.create_connection(("localhost", 2333), timeout=timeout)
            socket.close()
            break
        except OSError:
            logger.error("Lavalink is not running")
            return None

    logger.success("Lavalink is running")
    return 0
