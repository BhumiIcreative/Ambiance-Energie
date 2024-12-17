# coding: utf-8
{
    'name': "Amb EDF Prime",

    'summary': "Amb EDF Prime",

    'description': "Amb EDF Prime",

    'author': "Sirius-info",

    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': [
        'amb_sale',
        'amb_account',
        'script_tools',
    ],

    # always loaded
    'data': [
        'datas/product_template.xml',

        'views/account_move_view.xml',
        'views/sale_views.xml',

        'wizard/wizard_add_edf_prime_view.xml',
    ],
}
