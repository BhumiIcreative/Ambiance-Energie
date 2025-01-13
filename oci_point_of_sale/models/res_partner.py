from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    oci_point_of_sale = fields.Many2one(
        "oci.point.of.sale",
        string="Point of sale",
    )
