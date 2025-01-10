from odoo import models, fields

class OCIPointOFSale(models.Model):
    _name = 'oci.point.of.sale'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'OCI Point of Sale'

    name = fields.Char(string='Name', required=True)
    qrcode_payment = fields.Binary(string='QR Code Payment')
    active = fields.Boolean(string='Archive', default=True)
    oci_contact_pof_societe = fields.Many2one('res.company',string='Company',ondelete='set null')
    entrepot = fields.Many2one('stock.warehouse',string='Entrepot',ondelete='set null')