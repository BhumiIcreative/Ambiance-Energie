# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    non_remisable = fields.Boolean(
        string="Non remisable",
        copy=False,
        readonly=True,
        related="product_id.non_remisable_1",
    )
    commande_en_cours = fields.Float(
        string="Commande en cours",
        copy=False,
        readonly=True,
        compute="_compute_commande_en_cours",
    )
    point_de_vente = fields.Char(
        string="Point de vente",
        copy=False,
        readonly=True,
        related="order_id.warehouse_id.display_name",
    )
    point_de_vente_1 = fields.Char(
        string="Point de vente",
        copy=False,
        readonly=True,
        related="order_id.warehouse_id.display_name",
    )

    def _compute_commande_en_cours(self):
        for record in self:
            if not record.invoice_status == "invoiced":
                if record.state == "done" or record.state == "sale":
                    record["commande_en_cours"] = (
                        record.product_uom_qty
                        - record.qty_delivered
                        - record.qty_delivered_manual
                    )
                else:
                    record["commande_en_cours"] = 0
            else:
                record["commande_en_cours"] = 0
