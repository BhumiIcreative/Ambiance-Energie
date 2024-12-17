# coding: utf-8

from odoo import api, fields, models, _

import logging
log = logging.getLogger(__name__).info

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _margin_total_compute(self):
        for order in self:
            margin_total = sum(order.margin_order_line.mapped('margin_euro'))
            price_total = sum(order.margin_order_line.mapped('price_subtotal'))
            order.update({
                'margin_total': (margin_total / price_total if price_total !=0 else 0) * 100
                })

    margin_order_line = fields.One2many('sale.order.line', 'order_id', string=_('Lines with margin'))
    margin_total = fields.Float(_('Marge totale'), compute=_margin_total_compute)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

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
            if line_id.min_price < line_id.price_subtotal:
                is_greater_than_min = True
            line_id.update({
                'is_greater_than_min': is_greater_than_min,
            })

    min_price = fields.Monetary(_('Minimum Price'), readonly=True)
    is_greater_than_min = fields.Boolean(_('Is greater than minimum price'), compute=_is_valid)
    margin_euro = fields.Monetary(_('Margin Euro'), compute=_margins_compute)
    margin_percentage = fields.Float(_('Margin %'), compute=_margins_compute)
    article_cost = fields.Float(_('Unit cost'), related='product_id.standard_price')
    article_cost_subtotal = fields.Float(_('Cost'), compute=_cost_compute)

    @api.model_create_multi
    def create(self, values):
        res = super().create(values)
        for line in res:
            if line.product_id:
                line.min_price = line.product_id.min_price
        return res
