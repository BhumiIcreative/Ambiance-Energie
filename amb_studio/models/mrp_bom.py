from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    cot_unitaire = fields.Float(
        string="Unit Cost",
        copy=False,
        readonly=True,
        help="In Standard Price & AVCO: value of the product (automatically computed in AVCO).\n        In FIFO: value of the last unit that left the stock (automatically computed).\n        Used to value the product when the purchase cost is not known (e.g. inventory adjustment).\n        Used to compute margins on sale orders.",
        related="product_tmpl_id.standard_price",
    )
    prix_de_vente_unitaire = fields.Float(
        string="Unit Selling Price",
        copy=False,
        readonly=True,
        help="Price at which the product is sold to customers.",
        related="product_tmpl_id.list_price",
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", copy=False, ondelete="set null"
    )
    cot_total = fields.Monetary(
        string="Total Cost", copy=False, readonly=True, compute="_compute_cot_total"
    )
    prix_de_vente_total = fields.Monetary(
        string="Total Selling Price",
        copy=False,
        readonly=True,
        compute="_compute_prix_de_vente_total",
    )

    @api.depends("product_qty", "cot_unitaire")
    def _compute_cot_total(self):
        for record in self:
            record["cot_total"] = record.cot_unitaire * record.product_qty

    @api.depends("prix_de_vente_unitaire", "product_qty")
    def _compute_prix_de_vente_total(self):
        for record in self:
            record["prix_de_vente_total"] = (
                record.prix_de_vente_unitaire * record.product_qty
            )
