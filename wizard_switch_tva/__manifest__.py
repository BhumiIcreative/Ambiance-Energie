# -*- coding: utf-8 -*-
{
    'name':"Wizard switch TVA form",
    'summary': """ Wizard switch TVA form """,
    'description':  """
        Wizard switch TVA form to allow changing TVA taxes on Sale and Account.
    """,
    'author': 'Aktiv software / Groupe OCI',
    'website': "http://www.aktivsoftware.com / https://www.oci.fr",
    'category':    'Sales Management',
    'version':     '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends':     ['account', 'sale_management'],
    'data':        [
        'security/ir.model.access.csv',
        'wizard/switch_tva_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}


