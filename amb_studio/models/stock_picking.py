from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    facture_ids = fields.Many2many(
        "account.move",
        "x_account_move_stock_picking_rel",
        string="Bill",
        copy=False,
        ondelete="cascade",
    )
