```mermaid
flowchart LR

  %% Algorithm
  gather_stage ==> fetch_stage
  fetch_stage ==> import_stage

  subgraph gather_stage [Gather Stage]
    direction TB
    gs([GATHER STARTED])
    ge([GATHER ENDED])
    gs ==> load_remote_catalog
    load_remote_catalog ==> validate_conforms_to
    validate_conforms_to == No ==> error
    validate_conforms_to == Yes ==> check_schema_version
    load_remote_catalog --> source_data
    load_remote_catalog --> catalog_values
    catalog_values --> check_schema_version
    check_schema_version-- No -->default_schema_version
    check_schema_version-- Yes -->schema_version
    schema_version --> get_existing_datasets
    default_schema_version --> get_existing_datasets
    get_existing_datasets --> existing_datasets
    get_existing_datasets ==> is_parent_
    is_parent_ == Yes ==> existing_parents
    existing_parents --> is_parent_demoted
    is_parent_ == No ==> is_parent_demoted
    is_parent_demoted -- Yes --> orphaned_parents
    is_parent_demoted == No ==> is_parent_promoted
    existing_datasets --> is_parent_promoted
    is_parent_promoted -- Yes --> new_parents
    is_parent_promoted == No ==> load_config
    load_config --> hc_filter
    load_config --> hc_defaults
    load_config ==> is_identifier_both
    is_identifier_both-. Yes .-> error
    is_identifier_both == No ==> for_each_dataset
    hc_filter --> dataset_contains_filter
    for_each_dataset ==> dataset_contains_filter
    dataset_contains_filter-. Yes .-> skip
    dataset_contains_filter == No ==> has_identifier
    has_identifier-. No .-> error
    has_identifier == Yes ==> multiple_identifier
    multiple_identifier-. Yes .-> skip
    multiple_identifier == No ==> unique_datsets
    unique_datsets --> unique_existing
    unique_existing == Yes ==> hash_exists
    unique_existing -- Yes --> seen_datasets
    unique_existing == No ==> new_pkg_id
    hash_exists == Yes ==> get_source_hash
    get_source_hash ==> is_active
    is_active == Yes ==> make_upstream_content_hash
    is_active == No ==> HarvestObjectExtra
    hash_exists == No ==> make_upstream_content_hash
    orphaned_parents-- Disjunction -->make_upstream_content_hash
    new_parents-- Disjunction -->make_upstream_content_hash
    make_upstream_content_hash ==> check_hash
    check_hash-. Yes .-> skip
    check_hash-- No -->HarvestObjectExtra
    new_pkg_id --> HarvestObjectExtra
    Append__is_collection --> HarvestObjectExtra
    schema_version --> HarvestObjectExtra
    default_schema_version --> HarvestObjectExtra
    catalog_values --> HarvestObjectExtra
    Append__collection_pkg_id --> HarvestObjectExtra
    HarvestObjectExtra ==> is_parent_2
    is_parent_2 == Yes ==> Harvest_first
    is_parent_2 == No ==> Harvest_second
    Harvest_first ==> for_each_dataset_end
    Harvest_second ==> for_each_dataset_end
    for_each_dataset_end ==> for_each_existing
    for_each_existing --> seen_datasets
    for_each_existing ==> is_deleted
    seen_datasets-. Inverse .-> skip
    is_deleted-. Yes .-> skip
    seen_datasets --> delete
    is_deleted== No ==>delete
    delete-. exception .-> error
    delete ==> for_each_existing_end
    for_each_existing_end ==> ge
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
    is ==> empty_dataset
    empty_dataset == Yes ==> ie
    empty_dataset == No ==> has_title
    has_title == Yes ==> extract_extras
    has_title-. No .->error_2
    extract_extras --> default_schema_version_2
    extract_extras --> default_collection
    extract_extras --> default_parent
    extract_extras --> default_catalog
    extract_extras ==> does_parent_exist
    does_parent_exist == Yes ==> fetch_parent
    does_parent_exist == No ==> new_pkg_title
    does_parent_exist-. No .->error_2
    default_collection --> does_parent_exist
    default_parent --> does_parent_exist
    fetch_parent ==> new_pkg_title
    new_pkg_title ==> is_title_valid
    is_title_valid== Yes ==> is_federal
    is_title_valid-. No .->error_2
    default_schema_version_2 --> is_federal
    hc_defaults_2 --> is_federal
    new_pkg_title ==> is_federal
    is_federal == Yes ==> federal_validation
    is_federal == No ==> non_federal_validation
    federal_validation ==> validate_dataset
    non_federal_validation ==> validate_dataset
    validate_dataset ==> get_owner_org
    get_owner_org ==> make_upstream_content_hash_2
    make_upstream_content_hash_2 ==> assemble_basic_dataset_info
    assemble_basic_dataset_info ==> add_dataset_specific_info
    add_dataset_specific_info ==> is_geospatial
    is_geospatial == Yes ==> tag_geospatial
    is_geospatial == No ==> is_collection
    tag_geospatial ==> is_collection
    is_collection == Yes ==> tag_collection_parent
    is_collection == No ==> tag_collection_child
    tag_collection_parent ==> tag_catalog_values
    tag_collection_child ==> tag_catalog_values
    tag_catalog_values ==> is_existing
    is_existing == Yes ==> get_existing_pkg
    is_existing == No ==> create
    get_existing_pkg ==> avoid_resource_overwriting
    avoid_resource_overwriting ==> update
    create ==> update_object_reference
    update ==> update_object_reference
    update_object_reference ==> ie
  end
  

  %% Data
  error[\Error/]
  error_2[\Error/]
  skip[/Skip\]
  source_data[(Source Datasets)]
  catalog_values[(Catalog Values)]
  schema_version[(Schema Version)]
  %% all_parents[(All Parent Identifiers)]
  existing_datasets[(Existing Datasets)]
  existing_parents[(Existing Parent Dataset Identifiers)]
  new_parents[(New Parent Dataset Identifiers)]
  orphaned_parents[(Parent Identifiers who no longer have children)]
  unique_datsets[(Unique Datasets)]
  seen_datasets[(Seen Datasets)]
  default_schema_version[(schema_version = 1.0)]
  default_schema_version_2[(schema_version = 1.0)]
  default_collection[(is_collection=false)]
  default_parent[(parent_pkg_id=empty_str)]
  default_catalog[(catalog_values=none)]
  hc_filter[(Source Config Filter)]
  hc_defaults[(Source Config Defaults)]
  hc_defaults_2[(Source Config Defaults)]
  new_pkg_id[(New package id)]
  HarvestObjectExtra[(Create Harvest Object)]
  new_pkg_title[(New package title)]

  %% Functons
  load_remote_catalog[[Load Remote Catalog]]
  make_upstream_content_hash[[Make Upstream Content Hash]]
  make_upstream_content_hash_2[[Make Upstream Content Hash]]
  load_config[[Load Harvest Source Config]]
  get_existing_datasets[[Get Existing Datasets]]
  get_source_hash[[Source Hash]]
  %% set_dataset_info[[Set Dataset Info]]
  for_each_dataset[[For Each Source Dataset START]]
  for_each_dataset_end[[For Each Source Dataset END]]
  for_each_existing[[For Each Existing Dataset START]]
  for_each_existing_end[[For Each Existing Dataset END]]
  update[[Update Dataset]]
  delete[[Delete Dataset]]
  do_nothing[[Nothing to do]]
  extract_extras[[Parse SchemaVersion, isCollection, CollectioPkgId, catalogValues]]
  federal_validation[[Federal Validation]]
  non_federal_validation[[Non-Federal Validation]]
  validate_dataset[[Validate Dataset]]
  get_owner_org[[Get Owner Organization]]
  assemble_basic_dataset_info[[Assemble Basic Dataset]]
  add_dataset_specific_info[[Add Unique Dataset Info]]
  tag_collection_parent[[Mark as Collection Parent]]
  tag_collection_child[[Mark as Collection Child]]
  tag_geospatial[[Mark as geospatial]]
  tag_catalog_values[[Track catalog values in dataset]]
  get_existing_pkg[[Get Existing Package Info]]
  create[[Create New Package]]
  avoid_resource_overwriting[[Preserve existing resources]]
  update_object_reference[[Make this package the Current Harvest Object]]


  %% Conditional Checks
  validate_conforms_to{conformsTo is supported schema?}
  check_schema_version{Does schema_version exist?}
  is_parent_{Is Parent?}
  is_parent_2{Is Parent?}
  is_parent_demoted{Is Parent Demoted?}
  is_parent_promoted{Is Dataset Promoted?}
  is_identifier_both{Is Identifier Parent AND Child?}
  dataset_contains_filter{dataset contains key-value specified in filter?}
  has_identifier{Does dataset have identifier?}
  multiple_identifier{Has the identifier been seen before?}
  unique_existing{Is the unique dataset an existing dataset?}
  hash_exists{Does the dataset have an existing hash?}
  check_hash{Is Hash the same?}
  is_active{Is Dataset Active?}
  is_deleted{Is Dataset Deleted?}
  empty_dataset{Is the dataset empty?}
  is_federal{Is validator schema federal or non-federal?}
  is_existing{Is it an existing dataset?}
  is_geospatial{Is the package geospatial?}
  is_collection{Is the package a collection?}
  is_existing{Does the dataset exist already?}
  has_title{Does the dataset have a title?}
  does_parent_exist{Does Parent exist?}
  is_title_valid{Is the title valid?}
```
