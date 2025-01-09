from odoo import fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    external_ref = fields.Char(string='Vendor')
