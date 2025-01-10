# coding: utf-8
{
    "name": "Amb account",
    "summary": "Amb account",
    "description": "Amb account",
    "author": "Sirius-info",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "account",
    "version": "0.2",
    "application": True,
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "account",
        "account_followup",
        "oci_point_of_sale",
    ],
    # always loaded
    "data": [
        "data/account_journal.xml",
        "data/ir_config_parameter.xml",
        "data/report_paperformat.xml",
        'report/custom_external_layout.xml',
        "views/account_move_views.xml",
        'report/custom_invoice_report.xml',
        'report/accounting_pieces.xml',
    ],
}
