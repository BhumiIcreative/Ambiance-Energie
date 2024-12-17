# coding: utf-8
{
    'name': "Amb product",

    'summary': "Amb product",

    'description': "Amb product",

    'author': "Sirius-info",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'product',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product',
        'sale',
    ],

    # always loaded
    'data':        [
        'views/product_views.xml',
        'views/sale_views.xml',
    ],
}
