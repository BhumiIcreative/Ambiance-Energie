from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    min_price = fields.Monetary(string="Minimum Price", readonly=True)
    is_greater_than_min = fields.Boolean(
        string="Is Greater than Minimum Price", compute="_is_valid"
    )
    margin_euro = fields.Monetary(string="Margin Euro", compute="_margins_compute")
    margin_percentage = fields.Float(string="Margin %", compute="_margins_compute")
    article_cost = fields.Float(string="Unit Cost", related="product_id.standard_price")
    article_cost_subtotal = fields.Float(
        string="Cost", compute="_margins_compute", store=True
    )

    def _margins_compute(self):
        """Compute and update the margin for each line based on the price and cost values
        Calculates margin in euros and percentage"""
        for line_id in self:
            margin_euro = line_id.price_subtotal - line_id.article_cost_subtotal
            line_id.update(
                {
                    "margin_euro": margin_euro,
                    "margin_percentage": (
                        (margin_euro / line_id.price_subtotal) * 100
                        if line_id.price_subtotal != 0
                        else 0
                    ),
                    "article_cost_subtotal": line_id.article_cost
                    * line_id.product_uom_qty,
                }
            )

    @api.depends("margin_euro")
    def _is_valid(self):
        """Update the 'is_greater_than_min' field for each line based on whether the price subtotal is greater than the minimum price"""
        for line_id in self:
            line_id.update(
                {
                    "is_greater_than_min": line_id.min_price < line_id.price_subtotal,
                }
            )

    @api.model_create_multi
    def create(self, values):
        """Override the create method to set 'min_price' for each newly created line based on the product's 'min_price' when multiple records are created."""
        res = super().create(values)
        for line in res.filtered(lambda line: line.product_id):
            line.min_price = line.product_id.min_price
        return res
