# coding: utf-8
{
    'name':        "Wizard switch TVA form",

    'summary':
                   """
                   Wizard switch TVA form
                   """,

    'description': """
        Wizard switch TVA form ...
    """,

    'author':      "Sirius-info, Group OCI",
    'website':     "",

    'category':    'Wizard',
    'version':     '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends':     ['base', 'account', 'sale'],

    # always loaded
    'data':        [
        'wizard/switch_tva_wizard.xml',
        'views/sale_views.xml',
        'views/account_views.xml',
    ],
    # only loaded in demonstration mode
    'demo':        [],
}
