{
    'name': "Sale Timeline",
    'summary': "Sale Timeline",
    'description': "Sale Timeline",
    'author': "Aktiv software / Groupe OCI",
    'website': "http://www.aktivsoftware.com / https://www.oci.fr",
    'category': 'sale',
    'version': '17.0.1.0.0',
    'application': True,
    'depends': [
        'account',
        'sale_management',
    ],
    'data': [
        'data/account_journal.xml',
        'data/account_payment_term.xml',
        'security/ir.model.access.csv',
        # 'views/account_move_views.xml',
        'views/account_payment_views.xml',
        # 'views/sale_order_views.xml',
    ],
    'license': 'LGPL-3',
}
