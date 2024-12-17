{
    'name': 'OCI web_assets_backend_css',
    'version': '13.0.1.0.0',
    'author': 'OCI',
    'category': 'Extra Tools',
    'website': 'https://oci.fr',
    'sequence': 1,
    'summary': 'Fixed table headers in tree views and line background color, pure css.',
	  
    'description': """
This module adds some lines of css in the backend assets for :
- achieves fixed table headers for listviews in search results
- change line background color

============
Steps:
1-Install module
2-Restart odoo service - this is necessary to immediately rebuild the assets cache.
3-Clear browser cache and goto any odoo page with treeview and enough records to cause scrolling.
4-Scroll down and enjoy fixed table headers
    """,
    'depends': ['web'],
    'data': [
		'views/OCI_web_assets_backend_css.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
