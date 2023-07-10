from harvester.extract.dcatus import parse_catalog
from harvester.utils.json import download_json
from harvester.utils.s3 import upload_to_S3
from harvester.utils import railway
from harvester.validate.dcat_us import is_dcatus_schema

# ruff: noqa: F841

# @railway.tracks
def main(job_info, S3_client):
    """extract a file, mild validation, upload to s3 bucket.
    job_info (dict)             :   info on the job ( e.g. source_id, job_id, url )
    S3_client (boto3.client)    :   S3 client
    """


    # step 1 download json                  F
    # step 2 check if valid dcatus          F 
    # step 3 loading each record into s3    F 
    
    """
        class Fail:
            def __init__( self, exception, func, *args, **kwargs ):
                self.exception = exception
                self.func = func 
                self.args = args
                self.kwargs = kwargs

        class errorhandler
            self.e = exception
            self.f = 
    """

    """
    ...--S--\     /
    --F--    [...]
    """


    output = {"job_id": job_info["job_id"], "s3_paths": []}

    # download file
    catalog = download_json(job_info["url"])

    # # check schema
    # if not is_dcatus_schema(catalog):
    #     return "invalid dcatus catalog"

    # parse catalog and upload records
    for record_info in parse_catalog(catalog, job_info):
        upload_to_S3(S3_client, record_info)
        output["s3_paths"].append(record_info["Key"])

    return output
