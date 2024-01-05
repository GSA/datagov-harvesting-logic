import pytest


@pytest.fixture
def harvest_source_example():
    return {
        "name": "test_harvest_source_name",
        "url": "http://localhost/dcatus/dcatus_compare.json",
        "source_type": "dcatus",
        "config": {},
    }
