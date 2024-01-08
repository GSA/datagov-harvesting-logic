from harvester.validate.dcat_us import validate_json_schema
from harvester.extract import extract
from harvester.utils.util import sort_dataset, dataset_to_hash
from harvester.load import create_ckan_entrypoint, search_ckan
from harvester.compare import convert_datasets_to_id_hash
from harvester.load import dcatus_to_ckan



def extract_catalog():
    pass 

def extract_ckan():
    pass 

def compare():
    pass 

def extract():

    extract_catalog()
    extract_ckan() 
    compare() 
    

class HarvestSource:
    def __init__(self, name, url, source_type, config) -> None:
        self.name = name
        self.url = url
        self.source_type = source_type
        self.config = config
        
        self.records = {}

class HarvestRecord:
    def __init__(self, hs, identifier, record, record_hash) -> None:
        self.hs = hs 
        self.identifier = identifier
        self.record = record
        self.record_hash = record_hash
        self.harvest_source


def assign_operation_to_record(record, operation):
    record.operation = operation
    return record


def compare(harvest_source, ckan_source) -> {str: list}:
    """Compares records"""

    harvest_ids = set(harvest_source.records.keys())
    ckan_ids = set(ckan_source.keys())
    same_ids = harvest_ids & ckan_ids

    create = list(harvest_ids - ckan_ids)
    delete = list(ckan_ids - harvest_ids)
    update = [
        i for i in same_ids if harvest_source.records[i].record_hash != ckan_source[i]
    ]

    for operation, ids in [("create", create), ("delete", delete), ("update", update)]:
        for record_id, record in harvest_source.records.items():
            if record_id in ids:
                harvest_source.records[record_id].operation = operation

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


def test_pipeline(harvest_source_example, open_dataset_schema):
    # harvest source setup
    harvest_source = HarvestSource(**harvest_source_example)

    # EXTRACTION
    # download the data
    harvest_source.extracted_data = extract(harvest_source)

    # format and store the records
    harvest_source.records = {
        r["identifier"]: HarvestRecord(
            r["identifier"], r, dataset_to_hash(sort_dataset(r))
        )
        for r in harvest_source.extracted_data
    }

    ckan = create_ckan_entrypoint(
        "https://catalog-dev.data.gov/",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJtQjRSX0pSU1hsaFlmRDN2WnN6NWRpRXF3dF83UE10TE1JVFRaRU1zSDhjIiwiaWF0IjoxNjk1MjMxMDkyfQ.Z8BeUk36zUGuiHWJCIMuVLwlHjz2e-yfXe-zMEOpV8k",
    )
    # COMPARISON
    # get the associated records on ckan
    ckan_source_datasets = search_ckan(
        ckan,
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
    harvest_source = compare(harvest_source, ckan_source)

    # ckan = create_ckan_entrypoint(ckan_url, api_key)
    # operations = {
    #     "delete": harvester.purge_ckan_package,
    #     "create": harvester.create_ckan_package,
    #     "update": harvester.update_ckan_package,
    # }

    # VALIDATE AND LOAD
    for record_id, record in harvest_source.records.items():
        validate_json_schema(record, open_dataset_schema)
        record.record_as_ckan = dcatus_to_ckan(
            record.record, "test_harvest_source_name"
        )
        # operations[record.operation](ckan, record.record_as_ckan)

    a = 10
