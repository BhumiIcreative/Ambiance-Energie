{
    "name": "Amb account",
    "summary": "Amb account",
    "description": "Amb account",
    "version": "17.0.1.0.0",
    "author": "Aktiv software / Groupe OCI",
    "website": "https://www.aktivsoftware.com / https://www.oci.fr",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "account",
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "account",
        "account_followup",
        "amb_studio",
        'sale'
    ],
    # always loaded
    "data": [
        "data/ir_config_parameter.xml",
        "data/report_paperformat.xml",
        "report/custom_external_layout.xml",
        "views/account_move_views.xml",
        "report/custom_invoice_report.xml",
        "report/accounting_pieces.xml",
    ],
    "installable": True,
    "application": True,
}
