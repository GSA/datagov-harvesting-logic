from harvester.extract import download_waf, traverse_waf, extract


def extract_dcatus_harvest_source(waf_url):
    waf_catalog = extract(
        {"url": waf_url, "type": "waf"}, {"filters": ["../", "dcatus/"]}
    )
    assert len(waf_catalog) > 0


def test_traverse_waf(get_waf_url):
    files = traverse_waf(get_waf_url, filters=["../", "dcatus/"])
    assert len(files) == 7

    downloaded_files = download_waf(files)
    assert len(downloaded_files) == 7
