# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    facture = fields.Many2many(
        "account.move", string="Facture", copy=False, ondelete="cascade"
    )
