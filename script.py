import logging
import threading
import time

import requests

from app import setup_logger

ASYNC = True
NUMBER_OF_REQUESTS = 20
REQUEST_INTERVAL = 0.01

# URL = "http://localhost:5000/sync-dummy-without-type"
# URL = "http://localhost:5000/sync-dummy-with-type"
# URL = "http://localhost:5000/async-dummy-without-type"
URL = "http://localhost:5000/async-dummy-with-type"

BODY = {
}


def synchronous_post(logger: logging.Logger, url: str, body: dict, no_test: int) -> None:
    t0 = time.time()
    logger.info(f"{no_test}: {requests.post(url, json=body, timeout=1000).json()} | Time: {time.time() - t0}")


def asynchronous_post(logger: logging.Logger, url: str, body: dict, no_test: int) -> None:
    logger.info(f"Scheduling {no_test} request")
    threading.Thread(target=synchronous_post, args=(logger, url, body, no_test)).start()


def main(logger) -> None:
    for i in range(NUMBER_OF_REQUESTS):
        task = asynchronous_post if ASYNC else synchronous_post
        task(logger, URL, BODY, i)
        time.sleep(REQUEST_INTERVAL)


if __name__ == "__main__":
    logger = setup_logger()
    main(logger)
