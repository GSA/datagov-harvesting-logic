import logging

logger = logging.getLogger("harvester")


def convert_datasets_to_id_hash(ckan_source):
    """converts the input catalogs into [{ dataset_id: metadata_hash },...] format.
    the harvest source metadata is sorted"""

    # harvest_datasets = {
    #     d["identifier"]: dataset_to_hash(sort_dataset(d)) for d in harvest_source
    # }

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

    return ckan_datasets


def compare(harvest_source, ckan_source):
    """Compares records"""
    logger.info("Hello from harvester.compare()")

    harvest_ids = set(harvest_source.keys())
    ckan_ids = set(ckan_source.keys())
    same_ids = harvest_ids & ckan_ids

    create += list(harvest_ids - ckan_ids)
    delete += list(ckan_ids - harvest_ids)
    update += [i for i in same_ids if harvest_source[i] != ckan_source[i]]

    compare_res = compare(*data_sources)

    # for record in harvest_source.records:
    #     if record.identifier in create:
    #         record.operation = "create"
    #     if record.identifier in delete:
    #         record.operation = "delete"
    #     if record.identifier in update:
    #         record.operation = "update"

    return harvest_source
