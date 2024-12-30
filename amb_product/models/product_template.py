from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    min_price = fields.Monetary(string="Minimum Price")
