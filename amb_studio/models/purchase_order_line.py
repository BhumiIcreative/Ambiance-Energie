from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    cde_frns_en_cours = fields.Float(
        string="Order of French in Progress",
        copy=False,
        readonly=True,
        compute="_compute_cde_frns_en_cours",
    )

    @api.depends("product_uom_qty", "qty_received", "qty_received_manual", "state")
    def _compute_cde_frns_en_cours(self):
        for record in self.filtered(lambda x: x.state in ["done", "purchase"]):
            if record.state == "done" or record.state == "purchase":
                record["cde_frns_en_cours"] = (
                    record.product_uom_qty
                    - record.qty_received
                    - record.qty_received_manual
                )
            else:
                record["cde_frns_en_cours"] = 0
