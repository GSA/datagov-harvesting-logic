from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


def is_dcatus_schema(catalog):
    if "dataset" in catalog:
        return True

    return False


def parse_errors(errors):
    error_message = ""

    for error in errors:
        error_message += (
            f"error: {error.message}. offending element: {error.json_path} \n"
        )

    return error_message


def validate_json_schema(record, dataset_schema):
    validator = Draft202012Validator(dataset_schema)

    try:
        validator.validate(record.record)
        record.valid = True
    except Exception as e:
        record.value = False
        # do something with the exception

    return record
