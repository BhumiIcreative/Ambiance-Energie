# -*- coding: utf-8 -*-
{
    'name': "Disable Export, Import",

    'summary': """
        Disable export, import permissions of Odoo users for data security
""",

    # 'description': """
    #     Long description of module's purpose
    # """,

    'author': "Magenest",
    'website': "http://magenest.com/",
    'images': ['static/description/background.png'],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extension',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'demo/demo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'OPL-1',
}