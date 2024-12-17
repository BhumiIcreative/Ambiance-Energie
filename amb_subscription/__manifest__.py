# coding: utf-8
{
    'name': "Subscription form",

    'summary': "Subscription form",

    'description': "Manage subscriptions",

    'author': "Sirius-info",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'subscription',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale_management',
        'account',
        'sale_timeline',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'datas/ir_config_parameter.xml',
        'datas/ir_cron.xml',
        'datas/subscription_sequence.xml',
        'views/subscription_views.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/menu_views.xml',
        'report/commissioning_report.xml',
        'report/custom_external_layout.xml',
        'report/custom_external_layout_commissioning.xml',
    ],
}
