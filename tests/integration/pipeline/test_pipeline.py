from harvester.validate.dcat_us import validate_json_schema


class HarvestSource:
    def __init__(self, name, url, source_type, config) -> None:
        self.name = name
        self.url = url
        self.source_type = source_type
        self.config = config


class HarvestRecord:
    def __init__(self, identifier, record, data_hash) -> None:
        self.identifier = identifier
        self.record = record
        self.record_hash = record_hash


def assign_operation_to_record(record, operation):
    record.operation = operation


def compare(harvest_source) -> {str: list}:
    """Compares records"""
    logger.info("Hello from harvester.compare()")

    harvest_ids = set(harvest_source.records.keys())
    ckan_ids = set(ckan_source.keys())
    same_ids = harvest_ids & ckan_ids

    create += list(harvest_ids - ckan_ids)
    delete += list(ckan_ids - harvest_ids)
    update += [
        i for i in same_ids if harvest_source.records[i].data_hash != ckan_source[i]
    ]

    for operation, ids in [("create", create), ("delete", delete), ("update", update)]:
        map(
            assign_operation_to_record(operation),
            filter(lambda r: r.identifier in ids, harvest_source.records),
        )

    return harvest_source


def extract(harvest_source):
    harvest_source.extracted_data = extract(
        harvest_source.url, harvest_source.source_type
    )

    harvest_source.records = {
        r["identifier"]: HarvestRecord(
            r["identifier"], r, dataset_to_hash(sort_dataset(r))
        )
        for r in harvest_source.extracted_data["dataset"]
    }

    ckan_source = harvester.search_ckan()["results"]
    ckan_source = convert_datasets_to_id_hash(ckan_source)

    harvest_source = compare(harvest_source)

    return harvest_source


def validate(harvest_record):
    validator = Draft202012Validator(dcatus_dataset_schema)
    validator.validate(harvest_record.record)

    # harvest_record.valid = True or False
    return harvest_record


def load(harvest_record):
    ckan = harvester.create_ckan_entrypoint(ckan_url, api_key)
    operations = {
        "delete": harvester.purge_ckan_package,
        "create": harvester.create_ckan_package,
        "update": harvester.update_ckan_package,
    }
    operations[harvest_record.operation](ckan, harvest_record.record)


def test_pipeline(harvest_source_example):
    # harvest source setup
    harvest_source = HarvestSource(**harvest_source_example)

    # EXTRACTION
    # download the data
    harvest_source.extracted_data = extract(
        harvest_source.url, harvest_source.source_type
    )["dataset"]

    # format and store the records
    harvest_source.records = {
        r["identifier"]: HarvestRecord(
            r["identifier", r, dataset_to_hash(sort_dataset(r))]
        )
        for r in harvest_source.extracted_data
    }

    # COMPARISON
    # get the associated records on ckan
    ckan_source_datasets = search_ckan(
        ckan_entrypoint,
        {
            "q": 'harvest_source_name:"test_harvest_source_name"',
            "fl": [
                "extras_harvest_source_name",
                "extras_dcat_metadata",
                "extras_identifier",
            ],
        },
    )["results"]

    # format the ckan records for comparison
    ckan_source = convert_datasets_to_id_hash(ckan_source_datasets)

    # run our comparison
    compare_result = compare(harvest_source, ckan_source)

    ckan = harvester.create_ckan_entrypoint(ckan_url, api_key)
    operations = {
        "delete": harvester.purge_ckan_package,
        "create": harvester.create_ckan_package,
        "update": harvester.update_ckan_package,
    }

    # VALIDATE AND LOAD
    for record_id, record in harvest_source.records.items():
        validate_json_schema(record.record)
        record.record_as_ckan = dcatus_to_ckan(record.record)
        operations[record.operation](ckan, record.record_as_ckan)
