# -*- coding: utf-8 -*-

{
    'name': "Inventory Adjustment Backdated",
    'category': 'Inventory',
    'version': '14.0.1.0',
    'author': 'Equick ERP, Group OCI',
    'description': """
        This Module allows user to do adjustments in back dated-force dated.
        * Allow user to do adjustments in back dated-force dated..
        * Update the date in stock moves and product moves.
        * Update the date in journal entries if product have automated valuation method.
    """,
    'summary': """inventory adjustment date | inventory adjustment force date | force date inventory adjustment | back dated inventory adjustment | date inventory adjustment | back dated inventory | force date inventory.""",
    'depends': ['stock_account'],
    'website': "",
    'data': [
        'views/stock_view.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

