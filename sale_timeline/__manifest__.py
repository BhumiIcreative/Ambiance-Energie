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
        'account','sale',
    ],

    'data': [
        'datas/account_journal.xml',
        'datas/account_payment_term.xml',
        'security/ir.model.access.csv',
        'views/account_move_view.xml',
        'views/account_payment_view.xml',
        'views/sale_order_view.xml',
    ],
}
