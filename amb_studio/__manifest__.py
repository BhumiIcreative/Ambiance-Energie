{
    "name": "Amb Studio",
    "summary": "Amb Studio",
    "description": "Amb Studio",
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Studio",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": [
        "account",
        "mrp",
        "product",
        "purchase",
        "sale",
        "sale_stock",
        "stock",
        "hr_expense",
        "amb_stock",
    'mass_mailing'
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/account_tax_view.xml",
        "views/product_views.xml",
        "views/stock_picking_views.xml",
        "views/account_batch_payment_views.xml",
        "views/account_payment_view.xml",
        "views/account_full_reconcile_views.xml",
        "views/mailing_contact_views.xml",
        "views/res_group_views.xml",
        "views/sale_order_views.xml",
        "views/stock_oderpoint_views.xml",
        "views/stock_quant_views.xml",
        "views/stock_valuation_layer_views.xml",
        "views/uom_uom_views.xml",
        "views/account_move_views.xml",
        "views/product_template_views.xml"
    ],
    "application": False,
    "installable": True,
    "auto_install": False,

}
