import logging
from harvester.utils.util import dataset_to_hash, sort_dataset

logger = logging.getLogger("harvester")


def convert_datasets_to_id_hash(
    harvest_source: [dict], ckan_source: [dict]
) -> (list, list):
    """converts the input catalogs into [{ dataset_id: metadata_hash },...] format.
    the harvest source metadata is sorted"""

    harvest_datasets = {
        d["identifier"]: dataset_to_hash(sort_dataset(d)) for d in harvest_source
    }

    ckan_datasets = {}

    for d in ckan_source:
        oid, meta = None, None
        for e in d["extras"]:
            if e["key"] == "dcat_metadata":
                meta = eval(e["value"], {"__builtins__": {}})
            if e["key"] == "identifier":
                oid = e["value"]
        ckan_datasets[oid] = dataset_to_hash(
            meta
        )  # ckan datasets will always be stored sorted

    return harvest_datasets, ckan_datasets


def compare(harvest_source: [dict], ckan_source: [dict]) -> {str: list}:
    """Compares records"""
    logger.info("Hello from harvester.compare()")

    output = {
        "create": [],
        "update": [],
        "delete": [],
    }

    harvest_ids = set(harvest_source.keys())
    ckan_ids = set(ckan_source.keys())
    same_ids = harvest_ids & ckan_ids

    output["create"] += list(harvest_ids - ckan_ids)
    output["delete"] += list(ckan_ids - harvest_ids)
    output["update"] += [i for i in same_ids if harvest_source[i] != ckan_source[i]]

    return output
