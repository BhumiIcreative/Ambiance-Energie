# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Script tools",
    "version": "17.0.1.0.0",
    "category": "Dev",
    "license": "LGPL-3",
    "summary": "Script tools. Provide development features",
    "depends": ["base", "file_wizard"],
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    "data": [
        "security/ir.model.access.csv",
        "wizard/script_tools_view.xml",
        "confirmation/confirmation_wizard_view.xml",
        "xml_export/export_record_to_xml_view.xml",
    ],
    "installable": True,
    "application": False,
}
