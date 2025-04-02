from . import models


def post_init_function(env):
    fields = {
        'x_name': 'name',
        'x_studio_qrcode_payment': 'qrcode_payment',
        'x_studio_pos_archive': 'active',
        'x_studio_oci_contact_pof_societe': 'oci_contact_pof_societe',
        'x_studio_entrepot': 'entrepot'
    }
    values = {}
#     print('\n======================\n\n\n\nn\n\n\n\n\n\n\n',env['x_point_de_vente'].search([]))
#     for record in env['x_point_de_vente'].search([]):
#         for key, value in fields.items():
#             field_value = getattr(record, key, None)
#             print('\n=======field_value',field_value,record,key)
#             if key == 'x_name':
#                 values.update({'name': field_value})
#             if key == 'x_studio_qrcode_payment':
#                 values.update({'qrcode_payment': field_value})
#             if key == 'x_studio_oci_contact_pof_societe':
#                 values.update({'oci_contact_pof_societe': field_value.id})
#             if key == 'x_studio_entrepot':
#                 values.update({'entrepot': field_value.id})
#         print('\n\nn\n\n',values)
#         env['oci.point.of.sale'].create(values)