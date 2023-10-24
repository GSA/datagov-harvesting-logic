from harvester.extract.dcatus import download_dcatus_catalog
from requests.exceptions import ConnectionError, JSONDecodeError


def test_extract_dcatus(get_dcatus_job):
    """download dcat-us json file
    get_dcatus_job (dict)           :   fixture of a valid dcatus url
    """

    assert isinstance(download_dcatus_catalog(get_dcatus_job), dict)


def test_extract_bad_url(get_bad_url):
    """download a bad url.
    get_bad_url (dict)              :   fixture of a bad url
    """

    res = download_dcatus_catalog(get_bad_url)

    if hasattr(res, "status_code"):
        assert res.status_code == 404
    else:
        assert isinstance(res, ConnectionError) or isinstance(res, JSONDecodeError)


def test_extract_bad_json(get_bad_json):
    """download a malformed json.
    get_bad_json (str)  :   fixture of malformed json
    """
    assert isinstance(download_dcatus_catalog(get_bad_json), JSONDecodeError)


def test_extract_no_dataset_key(get_no_dataset_key_dcatus_json):
    """download a invalid dcatus catalog.
    get_no_dataset_key_dcatus_json (dict)
        :   fixture of a dcatus with no "dataset" key
    """

    assert "dataset" not in download_dcatus_catalog(get_no_dataset_key_dcatus_json)
