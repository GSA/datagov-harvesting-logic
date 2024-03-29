```mermaid
flowchart TD
  %% Operations
  sc([SOURCE CREATION])
  extract([Extract Faceted Catalog Source])
  compare([Compare Source Catalog to Data.gov Catalog])
  load([Load into Data.gov Catalog])
  validate([Validate Dataset])
  transform([Transform Schema of Dataset])
  completed([End])

  %% Conditions
  nochanges{No Changes?}
  deletions{Datasets to Delete?}
  updates{Datasets to Add or Update?}
  manual{Manual Trigger}
  scheduled{Scheduled Trigger}

  sc --> manual
  sc --> scheduled
  manual --> extract
  scheduled --> extract
  extract --> compare
  compare --> deletions
  compare --> updates
  deletions --> load
  updates --> validate
  validate --> transform
  transform --> validate
  validate --> load
  load --> completed
  compare --> nochanges
  nochanges --> completed
```
