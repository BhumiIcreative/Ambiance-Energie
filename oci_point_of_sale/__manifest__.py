{
    'name': "OCI Point Of Sale",
    'summary': "OCI Point Of Sale",
    'description': "OCI Point Of Sale",
    'author': "Aktiv software / Groupe OCI",
    'website': "http://www.aktivsoftware.com / https://www.oci.fr",
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['stock','mail','contacts'],
    'data': [
        'views/oci_point_of_sale_views.xml',
        'security/ir.model.access.csv'
    ],
    'application': False,
}
