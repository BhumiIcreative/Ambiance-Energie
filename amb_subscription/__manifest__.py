{
    "name": "Subscription form",
    "summary": "Subscription form",
    "description": "Manage subscriptions",
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "subscription",
    "version": "17.0.1.0.0",
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    "depends": [
        "sale_management",
        "account",
        "l10n_fr",
        'sale_timeline'
    ],
    # always loaded
    "data": [
        "data/ir_cron.xml",
        "data/ir_config_parameter.xml",
        "security/ir.model.access.csv",
        "views/subscription_views.xml",
        "views/res_company_views.xml",
        "views/account_move_line_views.xml",
        "report/commissioning_report.xml",
        "report/custom_external_layout.xml",
        "report/custom_external_layout_commissioning.xml",
    ],
    "application": False,
    'installable': True

}
