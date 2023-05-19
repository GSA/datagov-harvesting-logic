from .celery import app
import requests


@app.task
def download_json(url):
    return requests.get(url).json()