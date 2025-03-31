# -*- coding: utf-8 -*-
from odoo import fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    field_RFPir = fields.Many2one(
        "stock.warehouse", string="Entrepôt", copy=False, ondelete="set null"
    )
    field_pkvcm = fields.Many2many(
        "stock.location", string="Emplacements de stock", copy=False, ondelete="cascade"
    )
    magasin = fields.Char(
        string="Magasin", copy=False, readonly=True, compute="_compute_magasin"
    )

    def _compute_magasin(self):
        for record in self:
            if record.quantity > 0:
                record["magasin"] = record.stock_move_id.location_dest_id.name
            else:
                record["magasin"] = record.stock_move_id.location_id.name
