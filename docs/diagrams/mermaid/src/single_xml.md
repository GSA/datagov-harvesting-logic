```mermaid
flowchart LR

  %% Algorithm
  gather_stage ==> fetch_stage
  fetch_stage ==> import_stage

  subgraph gather_stage [Gather Stage]
    direction TB
    gs([GATHER STARTED])
    ge([GATHER ENDED])
    gs ==> _get_content_as_unicode
    _get_content_as_unicode ==> is_existing_object
    is_existing_object == Yes ==> get_existing_object
    is_existing_object == No ==> create_object
    get_existing_object ==> change_object
    change_object ==> guess_standard
    create_object ==> guess_standard
    guess_standard ==> is_iso
    is_iso == Yes ==> save_content
    is_iso == No ==> save_original_document
    save_content ==> ge
    save_original_document ==> ge
    _get_content_as_unicode-. Exception .-> error
  end
  subgraph fetch_stage [Fetch Stage]
    direction TB
    fs([FETCH STARTED])
    fe([FETCH ENDED])
    fs ==> do_nothing
    do_nothing ==> fe
  end
  subgraph import_stage [Import Stage]
    direction TB
    is([IMPORT STARTED])
    ie([IMPORT ENDED])
    is ==> is_object_empty
    is_object_empty == No ==> is_force_import
    is_force_import == Yes ==> change_object_2
    is_force_import == No ==> check_status_from_gather
    change_object_2 ==> get_existing_object_2
    check_status_from_gather ==> get_existing_object_2
    get_existing_object_2 ==> is_delete
    is_delete == Yes ==> delete
    is_delete == No ==> is_iso_2
    is_iso_2 == No ==> transform_to_iso
    transform_to_iso == Success ==> save_content_2
    save_content_2 == tranform ==> parse_iso
    is_iso_2 == Yes ==> is_object_content_empty
    is_object_content_empty == No ==> _validate_document
    _validate_document == valid ==> parse_iso
    _validate_document == not valid ==> continue_on_validation_errors
    continue_on_validation_errors == Yes ==> parse_iso
    continue_on_validation_errors == No ==> ie
    parse_iso ==> update_object_reference
    update_object_reference ==> is_guid_current
    is_guid_current == No ==> update_guid
    update_guid ==> is_guid_present
    is_guid_present == No ==> generate_guid
    is_guid_present == Yes ==> get_modified_date
    generate_guid ==> get_modified_date
    get_modified_date ==> spatial_package_create
    spatial_package_create ==> is_source_private
    is_source_private == Yes ==> mark_object_private
    %% BUG: if source marked as private --> harvest --> changed to public --> harvest --> datasets remain private
    is_source_private == No ==> is_source_part_of_topic
    mark_object_private ==> is_source_part_of_topic
    is_source_part_of_topic == Yes ==> mark_object_part_of_topic
    is_source_part_of_topic == No ==> mark_as_geospatial
    mark_object_part_of_topic ==> mark_as_geospatial
    mark_as_geospatial ==> update_object_reference_2
    update_object_reference_2 ==> is_status_new
    is_status_new == Yes ==> create
    is_status_new == No ==> is_modified_newer
    is_modified_newer == No ==> transfer_job_history
    transfer_job_history ==> delete_old_object
    delete_old_object ==> reindex_package
    is_modified_newer == Yes ==> update
    create ==> ie
    update ==> ie
    is_object_content_empty-. Yes .-> error_2
    parse_iso-. exception .-> error_2
    is_guid_current-. Yes .-> error_2
    get_modified_date-. exception .-> error_2
    is_object_empty-. Yes .-> skip
    reindex_package -.-> skip
  end

  %% Data
  error[\Error/]
  error_2[\Error/]
  skip[/Skip\]

  %% Functons

  %% Code: https://github.com/ckan/ckanext-spatial/blob/e59a295431247fcd605fe55bb4fd9a2ecfc28d2b/ckanext/spatial/harvesters/base.py#L835-L860
  _get_content_as_unicode[[Download XML File]]

  get_existing_object[[Get Existing Object]]
  get_existing_object_2[[Get Existing Object]]
  create_object[[Create New Object]]
  change_object[[Mark Existing Object as Changed]]
  change_object_2[[Mark Existing Object as Changed]]
  guess_standard[[Guess Metadata Standard]]
  save_content[["Save Content (ISO)"]]
  save_content_2[["Save Content (ISO)"]]
  save_original_document[["Save Original Content (non-ISO)"]]
  update[[Update Dataset]]
  do_nothing[[Nothing to do]]
  create[[Create New Package]]
  update_object_reference[[Make this package the Current Harvest Object]]
  update_object_reference_2[[Make this package the Current Harvest Object]]
  transform_to_iso[[Transform to ISO]]
  _validate_document[[Validate Dataset]]
  parse_iso[[Parse ISO Document]]
  update_guid[[Update GUID]]
  generate_guid[[Generate GUID]]
  check_status_from_gather[[Get status from Gather]]
  get_modified_date[[Get Modified Date]]
  mark_object_private[[Mark Object as private]]
  mark_object_part_of_topic[[Mark Object as part of topic]]
  mark_as_geospatial[[Mark Object as geospatial]]
  transfer_job_history[[Transfer old object job history to new object]]
  delete_old_object[[Delete old object]]
  reindex_package[[Reindex package to reflect new date]]
  %% Spatial Package Create: https://github.com/ckan/ckanext-spatial/blob/e59a295431247fcd605fe55bb4fd9a2ecfc28d2b/ckanext/spatial/harvesters/base.py#L233-L492
  spatial_package_create[[Create Package Data ..see reference in code..]]


  %% Conditional Checks
  is_existing_object{Does the object exist?}
  is_iso{Is document ISO?}
  is_iso_2{Is document ISO?}
  is_object_empty{Is Object Empty?}
  is_force_import{Is the Object being forcible imported?}
  is_object_content_empty{Is the Object content empty?}
  continue_on_validation_errors{Continue if validation has errors?}
  is_guid_current{Is the GUID current?}
  is_guid_present{Does the GUID exist?}
  is_delete{Should the dataset be deleted?}
  is_source_private{Is the Harvest Source Private?}
  is_source_part_of_topic{Is the Harvest Source part of a Topic?}
  is_status_new{Is the Status new?}
```
