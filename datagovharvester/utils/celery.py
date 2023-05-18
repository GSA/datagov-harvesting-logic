from celery import Celery
import os
import requests


def create_celery_app():
    broker_host = os.getenv("TEST_REDIS_HOST")
    broker_port = os.getenv("TEST_REDIS_PORT")
    broker_url = f"redis://{broker_host}:{broker_port}"

    return Celery(broker=broker_url)


celery = create_celery_app()


@celery.task
def fetch_url():
    return requests.get("https://data.wa.gov/api/views/f6w7-q2d2/columns.json")
