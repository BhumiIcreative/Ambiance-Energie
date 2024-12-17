# coding: utf-8
{
    'name': "Amb sale",

    'summary': "Amb sale",

    'description': "Amb sale",

    'author': "Sirius-info",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '0.2',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale_management',
        'amb_subscription',
        'account_followup',
        'sale_timeline',
    ],

    # always loaded
    'data':        [
        'datas/ir_config_parameter.xml',
        'datas/report_paperformat.xml',
        'views/sale_views.xml',
        'report/custom_external_layout.xml',
        'report/custom_report_saleorder.xml',
        'report/intervention_request_report.xml',
    ],
}
