# coding: utf-8

from odoo import fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    oci_point_of_sale = fields.Many2one("oci.point.of.sale", string=_("Point of sale"))
