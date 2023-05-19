from .celery import app
import requests


@app.task
def fetch_json(url):
    return requests.get(url).json()
