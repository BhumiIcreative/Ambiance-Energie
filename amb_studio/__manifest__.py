{
    "name": "Amb Studio",
    "summary": "Amb Studio",
    "description": "Amb Studio",
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Studio",
    "version": "17.0.1.0.0",
    "application": False,
    "installable": True,
    # any module necessary for this one to work correctly
    "depends": [
        "account",
        "mrp",
        "product",
        "purchase",
        "sale",
        "sale_stock",
        "stock",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
    ],
    "license": "LGPL-3",
}
