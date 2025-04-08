from odoo import fields, models


class PointDeVente(models.Model):
    _name = "point.de.vente"
    _description = "Point de Vente"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Name", copy=False)
    pos_archive = fields.Boolean(string="Active", copy=False)
    oci_contact_pof_societe_id = fields.Many2one(
        "res.company", string="Company", copy=False, ondelete="set null"
    )
    entrepot_id = fields.Many2one(
        "stock.warehouse", string="Warehouse", copy=False, ondelete="set null"
    )
    qrcode_payment = fields.Binary(string="QR Code Payment", copy=False)
    active = fields.Boolean(string='Active', default=True)
    
