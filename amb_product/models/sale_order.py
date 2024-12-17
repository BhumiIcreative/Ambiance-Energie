from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    margin_order_line = fields.One2many('sale.order.line', 'order_id', string='Lines with margin')
    margin_total = fields.Float(string='Margin Total', compute='_margin_total_compute')

    def _margin_total_compute(self):
        for order in self:
            price_total = sum(order.margin_order_line.mapped('price_subtotal'))
            order.update({
                'margin_total': (sum(order.margin_order_line.mapped(
                    'margin_euro')) / price_total if price_total != 0 else 0) * 100
            })
