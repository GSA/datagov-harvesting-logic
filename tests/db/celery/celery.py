from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

broker_host = os.getenv("TEST_REDIS_HOST")
broker_port = os.getenv("TEST_REDIS_PORT")
broker_url = f"redis://{broker_host}:{broker_port}"

app = Celery(
    "harvester",
    broker=broker_url,
    backend=broker_url,
    include=["tests.db.celery.tasks"],
)