{
    "name": "Amb EDF Prime",
    "summary": "Amb EDF Prime",
    "description": "Amb EDF Prime",
    "version": "17.0.1.0.0",
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": [
        "amb_sale",
        "amb_account",
        "script_tools",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/product_template.xml",
        "views/account_move_view.xml",
        "views/sale_views.xml",
        "wizard/wizard_add_edf_prime_view.xml",
    ],
    "application": False,
    "installable": True,
}
