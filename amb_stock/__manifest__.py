{
    'name': "Amb Stock",
    'summary': "Amb stock",
    'description': "Amb stock",
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '17.0.1.0.0',
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    'depends': [
        'stock',
        'sale_stock',
        'script_tools',
        'purchase'
    ],
    # always loaded
    'data': [
        'views/stock_picking_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'report/custom_report_stock.xml',
    ],
    'application': False,
    'installable': True,
}
