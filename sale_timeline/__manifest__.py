# coding: utf-8

{
    'name': "Sale Timeline",

    'summary': "Sale Timeline",

    'description': "Sale Timeline",

    'author': "Sirius Info",
    'category': 'sale',

    'version': '1.0',
    'application': True,

    'depends': [
    'sale',
        'account',
    ],

    'data': [
        'security/ir.model.access.csv',
        'datas/account_journal.xml',
        'datas/account_payment_term.xml',
        'views/account_move_view.xml',
        'views/account_payment_view.xml',
        'views/sale_order_view.xml',
    ],
}
