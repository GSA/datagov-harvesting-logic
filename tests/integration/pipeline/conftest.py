import pytest
from harvester.utils.json import open_json
from pathlib import Path

BASE_DIR = Path(__file__).parents[3]
DATA_DIR = BASE_DIR / "data" / "dcatus"
SCHEMA_DIR = DATA_DIR / "schemas"


@pytest.fixture
def open_dataset_schema():
    dataset_schema = SCHEMA_DIR / "dataset.json"
    return open_json(dataset_schema)


@pytest.fixture
def harvest_source_example():
    return {
        "name": "test_harvest_source_name",
        "url": "http://localhost/dcatus/dcatus_compare.json",
        "source_type": "dcatus",
        "config": {},
    }
