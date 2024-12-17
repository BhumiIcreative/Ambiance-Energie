{
    "name": "Amb product",
    "summary": "Amb product",
    "description": "Amb product",
    "license": "LGPL-3",
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "product",
    "version": "17.0.1.0.1",
    "application": True,
    "depends": ["product", "sale_management"],
    "data": [
        "views/product_views.xml",
        "views/sale_views.xml",
    ],
}
