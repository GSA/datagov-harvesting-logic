from .celery import app
import requests


@app.task
def fetch_url(url):
    return requests.get(url).json()
