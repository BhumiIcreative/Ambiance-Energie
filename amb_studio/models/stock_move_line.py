from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    field_RucZV = fields.Char(
        string="New Field Linked", copy=False, readonly=True, related="owner_id.name"
    )
    oci_description_achat = fields.Text(
        string="Description Purchase",
        copy=False,
        readonly=True,
        related="move_id.purchase_line_id.name",
    )
