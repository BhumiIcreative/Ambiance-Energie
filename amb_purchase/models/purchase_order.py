from odoo import fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    oci_point_of_sale = fields.Many2one("point.de.vente", string="Point of Sale")
