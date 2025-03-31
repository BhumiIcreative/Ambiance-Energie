# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    cde_frns_en_cours = fields.Float(
        string="cde frns en cours",
        copy=False,
        readonly=True,
        compute="_compute_cde_frns_en_cours",
    )

    def _compute_cde_frns_en_cours(self):
        for record in self:
            if record.state == "done" or record.state == "purchase":
                record["cde_frns_en_cours"] = (
                    record.product_uom_qty
                    - record.qty_received
                    - record.qty_received_manual
                )
            else:
                record["cde_frns_en_cours"] = 0
