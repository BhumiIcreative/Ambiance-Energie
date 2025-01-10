# script_tools

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* The `script_tools` module provides a form view to execute and manage scripts.

---

## Dependencies

### Odoo modules dependencies

| Module         | Technical Name | Why used?                                                                                        |
|----------------|----------------|--------------------------------------------------------------------------------------------------|
|File wizard     |file_wizard     | The `file_wizard` module allows users to open a form view for downloading files.                 |
---


### Python library dependenci

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Implemented `_run_method()` to dynamically execute a method on records based on a domain.
* Implemented `record_to_reference()` to convert a record to a reference string.
* Implemented `download_text()` to encode text in base64 and download it as a file.
* Implemented `download_b64()` to create a file wizard for downloading base64-encoded files.
* Implemented `encode_base64()` to encode a string into base64 format.
* Implemented `open_record()` to opens a single record in a window view.
* Implemented `open_records()` to opens a record or a set of records in a window view.
* Implemented `open_wizard()` to opens a wizard record in a new window.
* Implemented `create_and_open()` to creates a new record and opens its associated script tools wizard.
* Implemented `_get_reference_selection()` to generates a list of selectable model references.
* Implemented `_cpt_xml_id` to using the record's model name and ID for unique identification.
* Implemented `_cpt_field_ids` to computes and sets the field IDs for export based on the specified record ID.
* Implemented `find_external_id` to find the external ID for a given record ID.
* Implemented `exec_code` to execute custom code
* Implemented `export` Exports record fields to an XML file, handling various field types (e.g., `many2one`, `reference`, `one2many`,`html`)
- Encodes special characters in string fields and generates a downloadable XML file.

---
