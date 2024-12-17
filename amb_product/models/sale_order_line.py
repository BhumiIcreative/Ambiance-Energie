from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    min_price = fields.Monetary(string='Minimum Price', readonly=True)
    is_greater_than_min = fields.Boolean(string='Is Greater than Minimum Price', compute='_is_valid')
    margin_euro = fields.Monetary(string='Margin Euro', compute='_margins_compute')
    margin_percentage = fields.Float(string='Margin %', compute='_margins_compute')
    article_cost = fields.Float(string='Unit Cost', related='product_id.standard_price')
    article_cost_subtotal = fields.Float(string='Cost', compute='_cost_compute')

    def _margins_compute(self):
        for line_id in self:
            margin_euro = line_id.price_subtotal - line_id.article_cost_subtotal
            margin_percentage = 0
            if line_id.price_subtotal != 0:
                margin_percentage = (margin_euro / line_id.price_subtotal) * 100
            line_id.update({
                'margin_euro': margin_euro,
                'margin_percentage': margin_percentage,
            })

    def _cost_compute(self):
        for line_id in self:
            article_cost_subtotal = line_id.article_cost * line_id.product_uom_qty
            line_id.update({
                'article_cost_subtotal': article_cost_subtotal
            })

    @api.depends('margin_euro')
    def _is_valid(self):
        for line_id in self:
            is_greater_than_min = False
            print('\n=======line_id.min_price',line_id.min_price)
            print('\n=======line_id.price_subtotal',line_id.price_subtotal)
            if line_id.min_price < line_id.price_subtotal:
                is_greater_than_min = True
            line_id.update({
                'is_greater_than_min': is_greater_than_min,
            })

    @api.model_create_multi
    def create(self, values):
        res = super().create(values)
        for line in res.filtered(lambda line: line.product_id):
            line.min_price = line.product_id.min_price
        return res
