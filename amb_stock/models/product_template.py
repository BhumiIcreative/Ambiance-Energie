# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)
log = _logger.info


class productTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends(
        'product_variant_ids',
        'product_variant_ids.net_qty',
        'product_variant_ids.order_qty',
        'product_variant_ids.free_qty',
        'product_variant_ids.stock_move_ids.product_uom_qty',
        'product_variant_ids.stock_move_ids.state',
    )
    def _cpt_custom_qty(self):
        for template_id in self:
            product_ids = self.env['product.product'].search([
                ('product_tmpl_id', '=', template_id.id),
            ])
            template_id.net_qty = sum(product_ids.mapped('net_qty'))
            template_id.order_qty = sum(product_ids.mapped('order_qty'))
            template_id.free_qty = sum(product_ids.mapped('free_qty'))


    free_qty = fields.Float('Quantité vendable', compute='_cpt_custom_qty', store=True, readonly=True)
    net_qty = fields.Float('Quantité nette', compute='_cpt_custom_qty', store=True, readonly=True)
    order_qty = fields.Float(_('Order Stock'),  compute='_cpt_custom_qty', store=True, readonly=True)

    def action_view_stock_move_lines_free_qty(self):
        for art in self:
            action = art.env.ref('stock.stock_move_line_action').read()[0]
            action['domain'] = [('product_id.product_tmpl_id', 'in', art.ids)]
            log(action)
            action['context'] = eval(action['context'])
            action['context']['search_default_done'] = 0
            return action

    def action_view_stock_move_lines_net_qty(self):
        Script = self.env['script.tools']
        for art in self:
            for product in art.product_variant_ids:
                lines = product.purchase_order_line_ids.filtered(lambda line: line.qty_received > 0)
        return Script.open_records(lines, name=_('Received quantity'))

    def action_view_ordered_stock(self):
        Script = self.env['script.tools']
        for art in self:
            for product in art.product_variant_ids:
                lines = product.purchase_order_line_ids.filtered(lambda line: line.product_qty > line.qty_received)
        return Script.open_records(lines, name=_('Ordered quantity'))
