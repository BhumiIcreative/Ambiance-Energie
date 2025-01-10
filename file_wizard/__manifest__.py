# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "File wizard",
    "version": "17.0.1.0.0",
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    "summary": "This module allow create a wizard from python that contains"
    " a binary fields",
    "description": """
This module allow create a wizard from python that contains a binary fields
How to use:

    file_wizard = self.env['file_wizard'].create({
        'name': _('Your new windows name (optional)'),
        'file_content': your_file_content_as_base_64,
        'file_name': "Your filename.txt"
    })
    return file_wizard.open_wizard()
""",
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "wizard/file_wizard.xml",
    ],
    "depends": ["base"],
    "application": False,
}
