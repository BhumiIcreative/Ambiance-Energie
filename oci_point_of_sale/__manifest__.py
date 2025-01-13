{
    'name': "OCI Point Of Sale",
    'summary': "OCI Point Of Sale",
    'description': "OCI Point Of Sale",
    'author': "Aktiv software / Groupe OCI",
    'website': "http://www.aktivsoftware.com / https://www.oci.fr",
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base_automation', 'stock', 'mail', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/oci_point_of_sale_views.xml',
        'views/res_partner.xml',
        'data/point_of_sale_automation.xml',
    ],
    'application': False,
}
