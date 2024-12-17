# coding: utf-8
{
    'name': 'Script tools',
    'version': '1.0',
    'category': 'Dev',
    'license': 'AGPL-3',
    'summary': 'Script tools. Provide developpement features',
    'depends': [
        'base',
    ],
    'author': 'Sirius-Info <Sirfanas>',
    'data': [
        'file/file_wizard.xml',
        'wizard/script_tools_view.xml',

        'ean_code/views/ean_view.xml',

        'confirmation/confirmation_wizard_view.xml',

        'xml_export/export_record_to_xml_view.xml',
    ],
    'installable': True,
    'application': False,
    'external_dependencies': {
        'python': [
            'pysftp',
        ]
    }
}
