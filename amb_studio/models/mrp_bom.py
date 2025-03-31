# -*- coding: utf-8 -*-
from odoo import fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    cot_unitaire = fields.Float(
        string="Unit cost",
        copy=False,
        readonly=True,
        help="In Standard Price & AVCO: value of the product (automatically computed in AVCO).\n        In FIFO: value of the last unit that left the stock (automatically computed).\n        Used to value the product when the purchase cost is not known (e.g. inventory adjustment).\n        Used to compute margins on sale orders.",
        related="product_tmpl_id.standard_price",
    )
    prix_de_vente_unitaire = fields.Float(
        string="Unit selling price",
        copy=False,
        readonly=True,
        help="Price at which the product is sold to customers.",
        related="product_tmpl_id.list_price",
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", copy=False, ondelete="set null"
    )
    cot_total = fields.Monetary(
        string="Coût total", copy=False, readonly=True, compute="_compute_cot_total"
    )
    prix_de_vente_total = fields.Monetary(
        string="Prix de vente total",
        copy=False,
        readonly=True,
        compute="_compute_prix_de_vente_total",
    )

    def _compute_cot_total(self):
        for record in self:
            record["cot_total"] = record.cot_unitaire * record.product_qty

    def _compute_prix_de_vente_total(self):
        for record in self:
            record["prix_de_vente_total"] = (
                record.prix_de_vente_unitaire * record.product_qty
            )
