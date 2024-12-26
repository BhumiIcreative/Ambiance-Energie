{
    "name": "Wizard switch TVA form",
    "summary": """ Wizard switch TVA form """,
    "description": """ Wizard switch TVA form """,
    "author": "Aktiv software / Groupe OCI",
    "website": "https://www.aktivsoftware.com / https://www.oci.fr",
    "category": "Wizard",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": ["account", "sale_management"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "wizard/switch_tva_wizard.xml",
        "views/sale_views.xml",
        "views/account_views.xml",
    ],
}
