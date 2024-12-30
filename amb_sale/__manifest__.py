{
    'name': "Amb sale",
    'summary': "Amb sale",
    'description': "Amb sale",
    'author': "Aktiv software / Groupe OCI",
    'website': "http://www.aktivsoftware.com / https://www.oci.fr",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '17.0.1.0.0',
    'application': True,
    # any module necessary for this one to work correctly
    'depends': [
        'amb_product',
        'amb_subscription',
        # 'sale_timeline',
        'sale_management',
        'account_followup',
        'stock',
    ],
    # always loaded
    'data': [
        'data/ir_config_parameter.xml',
        'data/report_paperformat.xml',
        'views/sale_views.xml',
        'views/res_partner_views.xml',
        'report/custom_external_layout.xml',
        'report/custom_report_saleorder.xml',
        'report/intervention_request_report.xml',
    ],
    'license': 'LGPL-3',
}
