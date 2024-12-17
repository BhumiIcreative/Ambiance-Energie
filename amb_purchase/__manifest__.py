# coding: utf-8
{
    'name': "Amb purchase",

    'summary': "Amb purchase",

    'description': "Amb purchase",

    'author': "Sirius-info",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchase',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'purchase',
        'account',
        'amb_account',
    ],

    # always loaded
    'data': [
        'datas/report_paperformat.xml',
        'report/custom_external_layout.xml',
        'report/custom_report_purchaseorder.xml',
        'report/custom_report_purchasequotation.xml',
        'views/purchase_views.xml'
    ],
}
