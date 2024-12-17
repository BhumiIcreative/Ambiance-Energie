# coding: utf-8
{
    'name': "Amb global discount",

    'summary': "Amb global discount",

    'author': "Groupe OCI",

    'version': '13.0.0.1',

    'depends': [
        'amb_sale',
        'amb_account',
        'script_tools',
    ],

    'data': [
        'views/account_move_view.xml',
        'views/sale_views.xml',
        'views/purchase_views.xml',
        'wizard/wizard_global_discount_view.xml',
    ],
}
