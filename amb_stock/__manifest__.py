# coding: utf-8
{
    'name': "Amb stock",

    'summary': "Amb stock",

    'description': "Amb stock",

    'author': "Sirius-info",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock',
        'sale_stock',
        'script_tools',
    ],

    # always loaded
    'data':        [
        # 'views/product_view.xml',
        'views/stock_picking_views.xml',
        'views/inventory_views.xml',
        'report/custom_report_sale_stock.xml',
        'report/custom_report_stock_valuation_layer.xml',

    ],
}
