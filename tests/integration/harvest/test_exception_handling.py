# ruff: noqa: F841

from unittest.mock import Mock, patch

import ckanapi
import pytest

from harvester.exceptions import ExtractExternalException, ExtractInternalException
from harvester.harvest import HarvestSource


def download_mock(_, __):
    return dict({"dataset": []})


class TestHarvestJobExceptionHandling:
    def test_bad_harvest_source_url_exception(
        self,
        interface,
        organization_data,
        source_data_dcatus_bad_url,
        job_data_dcatus_bad_url,
    ):
        interface.add_organization(organization_data)
        interface.add_harvest_source(source_data_dcatus_bad_url)
        harvest_job = interface.add_harvest_job(job_data_dcatus_bad_url)

        harvest_source = HarvestSource(harvest_job.id)

        with pytest.raises(ExtractExternalException) as e:
            harvest_source.prepare_external_data()

        assert harvest_job.status == "error"

        harvest_error = interface.get_harvest_job_errors_by_job(harvest_job.id)[0]
        assert harvest_error.type == "ExtractExternalException"

    def test_extract_internal_exception(
        self,
        interface,
        organization_data,
        source_data_dcatus,
        job_data_dcatus,
    ):
        interface.add_organization(organization_data)
        interface.add_harvest_source(source_data_dcatus)
        harvest_job = interface.add_harvest_job(job_data_dcatus)

        harvest_source = HarvestSource(harvest_job.id)

        harvest_source.internal_records_to_id_hash = Mock()
        harvest_source.internal_records_to_id_hash.side_effect = Exception("Broken")

        with pytest.raises(ExtractInternalException) as e:
            harvest_source.get_record_changes()

        assert harvest_job.status == "error"

        harvest_error = interface.get_harvest_job_errors_by_job(harvest_job.id)[0]
        assert harvest_error.type == "ExtractInternalException"

    def test_no_source_info_exception(self, job_data_dcatus):
        with pytest.raises(ExtractInternalException) as e:
            HarvestSource(job_data_dcatus["id"])


class TestHarvestRecordExceptionHandling:
    @patch("harvester.harvest.ckan", ckanapi.RemoteCKAN("mock_address"))
    @patch("harvester.harvest.download_file", download_mock)
    def test_delete_exception(
        self,
        interface,
        organization_data,
        source_data_dcatus,
        job_data_dcatus,
        single_internal_record,
    ):
        interface.add_organization(organization_data)
        interface.add_harvest_source(source_data_dcatus)
        harvest_job = interface.add_harvest_job(job_data_dcatus)

        interface.add_harvest_record(single_internal_record)

        harvest_source = HarvestSource(harvest_job.id)
        harvest_source.get_record_changes()
        harvest_source.write_compare_to_db()
        harvest_source.synchronize_records()

        interface_record = interface.get_harvest_record(
            harvest_source.internal_records_lookup_table[
                single_internal_record["identifier"]
            ]
        )
        interface_errors = interface.get_harvest_record_errors_by_record(
            harvest_source.internal_records_lookup_table[
                single_internal_record["identifier"]
            ]
        )
        assert (
            interface_record.id
            == harvest_source.internal_records_lookup_table[
                single_internal_record["identifier"]
            ]
        )
        assert interface_record.status == "error"
        assert interface_errors[0].type == "SynchronizeException"

    def test_validation_exception(
        self,
        interface,
        organization_data,
        source_data_dcatus_invalid,
        job_data_dcatus_invalid,
    ):
        interface.add_organization(organization_data)
        interface.add_harvest_source(source_data_dcatus_invalid)
        harvest_job = interface.add_harvest_job(job_data_dcatus_invalid)

        harvest_source = HarvestSource(harvest_job.id)
        harvest_source.get_record_changes()
        harvest_source.write_compare_to_db()
        harvest_source.synchronize_records()
        test_record = harvest_source.external_records["null-spatial"]

        interface_record = interface.get_harvest_record(
            harvest_source.internal_records_lookup_table[test_record.identifier]
        )
        interface_errors = interface.get_harvest_record_errors_by_record(
            harvest_source.internal_records_lookup_table[test_record.identifier]
        )
        assert (
            interface_record.id
            == harvest_source.internal_records_lookup_table[test_record.identifier]
        )
        assert interface_record.status == "error"
        assert interface_errors[0].type == "ValidationException"

    @patch("harvester.harvest.ckanify_dcatus", side_effect=Exception("Broken"))
    def test_dcatus_to_ckan_exception(
        self,
        ckanify_dcatus_mock,
        interface,
        organization_data,
        source_data_dcatus,
        job_data_dcatus,
    ):
        interface.add_organization(organization_data)
        interface.add_harvest_source(source_data_dcatus)
        harvest_job = interface.add_harvest_job(job_data_dcatus)

        harvest_source = HarvestSource(harvest_job.id)
        harvest_source.get_record_changes()
        harvest_source.write_compare_to_db()
        harvest_source.synchronize_records()

        test_record = harvest_source.external_records["cftc-dc1"]

        interface_record = interface.get_harvest_record(
            harvest_source.internal_records_lookup_table[test_record.identifier]
        )
        interface_errors = interface.get_harvest_record_errors_by_record(
            harvest_source.internal_records_lookup_table[test_record.identifier]
        )

        assert ckanify_dcatus_mock.call_count == len(harvest_source.external_records)
        assert (
            interface_record.id
            == harvest_source.internal_records_lookup_table[test_record.identifier]
        )
        assert interface_record.status == "error"
        assert interface_errors[0].type == "DCATUSToCKANException"

    # ruff: noqa: F401
    @patch("harvester.harvest.ckan", ckanapi.RemoteCKAN("mock_address"))
    def test_ckan_sync_exception(
        self,
        interface,
        organization_data,
        source_data_dcatus,
        job_data_dcatus,
    ):
        interface.add_organization(organization_data)
        interface.add_harvest_source(source_data_dcatus)
        harvest_job = interface.add_harvest_job(job_data_dcatus)

        harvest_source = HarvestSource(harvest_job.id)
        harvest_source.get_record_changes()
        harvest_source.write_compare_to_db()
        harvest_source.synchronize_records()

        test_record = harvest_source.external_records["cftc-dc1"]

        interface_record = interface.get_harvest_record(
            harvest_source.internal_records_lookup_table[test_record.identifier]
        )

        interface_errors = interface.get_harvest_record_errors_by_record(
            harvest_source.internal_records_lookup_table[test_record.identifier]
        )

        assert (
            interface_record.id
            == harvest_source.internal_records_lookup_table[test_record.identifier]
        )
        assert interface_record.status == "error"
        assert interface_errors[0].type == "SynchronizeException"
