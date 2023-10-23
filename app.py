import logging
import threading
import time
import typing as tp

from anyio import CapacityLimiter
from anyio.lowlevel import RunVar
from fastapi import FastAPI, Request, Response


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
    file_handler = logging.StreamHandler()
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = setup_logger()

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next: tp.Callable[..., tp.Awaitable]) -> tp.Any:
    logger.info(f"---- Request received: {request.method} {request.url} ----")
    response: Response = await call_next(request)
    logger.info(f"**** Request processed: {request.method} {request.url} ****")
    return response


@app.on_event("startup")
def startup():
    RunVar("_default_thread_limiter").set(CapacityLimiter(5))


@app.post("/async-dummy-without-type")
async def async_dummy_endpoint_without_type():
    logger.info(f"[START] Dummy async endpoint without type.")
    logger.info(f"Current number of thread {threading.active_count()}.")
    time.sleep(1)
    logger.info(f"[END] Dummy async endpoint without type.")
    return {"message": "Hello from dummy async endpoint without type!"}


@app.post("/async-dummy-with-type")
async def async_dummy_endpoint_with_type() -> dict:
    logger.info(f"[START] Dummy async endpoint with type.")
    logger.info(f"Current number of thread {threading.active_count()}.")
    time.sleep(1)
    logger.info(f"[END] Dummy async endpoint with type.")
    return {"message": "Hello from dummy async endpoint with type!"}


@app.post("/sync-dummy-without-type")
def sync_dummy_endpoint_without_type():
    logger.info(f"[START] Dummy sync endpoint without type.")
    logger.info(f"Current number of thread {threading.active_count()}.")
    time.sleep(1)
    logger.info(f"[END] Dummy sync endpoint without type.")
    return {"message": "Hello from dummy sync endpoint without type!"}


@app.post("/sync-dummy-with-type")
def sync_dummy_endpoint_with_type() -> dict:
    logger.info(f"[START] Dummy sync endpoint with type.")
    logger.info(f"Current number of thread {threading.active_count()}.")
    time.sleep(1)
    logger.info(f"[END]  Dummy sync endpoint with type.")
    return {"message": "Hello from dummy sync endpoint with type!"}
