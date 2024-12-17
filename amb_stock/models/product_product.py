# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)
log = _logger.info


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.depends(
        'qty_available',
        'product_variant_ids.stock_move_ids.product_uom_qty',
        'stock_move_ids.product_uom_qty',
        'stock_move_ids.state')
    def _cpt_free_qty(self):
        for art in self:
            StockMoveLine = art.env['stock.move.line']
            customer_location_id = art.env.ref('stock.stock_location_customers').id
            reserved_move_line_not_done = StockMoveLine.search([
                ('product_id', '=', art.id),
                ('state', '=', 'assigned'),
                ('location_dest_id', '=', customer_location_id),
            ])
            reserved_qty_not_done = sum(reserved_move_line_not_done.mapped('product_uom_qty'))
            art.free_qty = art.qty_available - reserved_qty_not_done

    @api.depends(
        'purchase_order_line_ids',
        'purchase_order_line_ids.product_id',
        'purchase_order_line_ids.order_id',
        'purchase_order_ids',
        'purchase_order_ids.state'
    )
    def _cpt_net_qty(self):
        for art in self:
            art.net_qty = art.qty_available + art.order_qty

    @api.depends(
        'purchase_order_line_ids',
        'purchase_order_line_ids.product_id',
        'purchase_order_line_ids.order_id',
        'purchase_order_ids',
        'purchase_order_ids.state'
    )
    def _cpt_order_qty(self):
        for product_id in self:
            line_ids = self.env['purchase.order.line'].search([
                ('id', 'in', product_id.purchase_order_line_ids.ids),
                ('order_id.state', 'in', ['purchase', 'done']),
            ]).filtered(lambda line: line.product_qty > line.qty_received)
            ordered_qty = sum(line_ids.mapped('product_qty'))
            received_qty = sum(line_ids.mapped('qty_received'))
            product_id.order_qty = ordered_qty - received_qty

    @api.depends('purchase_order_line_ids', 'purchase_order_line_ids.product_id', 'purchase_order_line_ids.order_id')
    def _cpt_purchase_order_ids(self):
        for product_id in self:
            product_id.purchase_order_ids = [(5, 0, 0)]
            line_ids = product_id.purchase_order_line_ids
            if line_ids:
                product_id.purchase_order_ids = [(6, 0, line_ids.mapped('order_id').ids)]

    free_qty = fields.Float(_('Sellable'), compute=_cpt_free_qty, store=True, readonly=True)
    net_qty = fields.Float('Quantité nette', compute=_cpt_net_qty, store=True, readonly=True)
    order_qty = fields.Float(_('Order Stock'),  compute=_cpt_order_qty, store=True, readonly=True)

    purchase_order_line_ids = fields.One2many('purchase.order.line', 'product_id', string=_('Purchase order lines'))
    purchase_order_ids = fields.Many2many('purchase.order', string=_('Purchase order'), compute=_cpt_purchase_order_ids, store=True)

    def action_view_stock_move_lines_free_qty(self):
        for art in self:
            action = art.env.ref('stock.stock_move_line_action').read()[0]
            action['domain'] = [('product_id', '=', art.id)]
            log(action)
            action['context'] = eval(action['context'])
            action['context']['search_default_done'] = 0
            return action

    def action_view_stock_move_lines_net_qty(self):
        Script = self.env['script.tools']
        orders = self.purchase_order_line_ids.filtered(lambda line: line.qty_received > 0)
        return Script.open_records(orders, name=_('Received quantity'))



    def action_view_ordered_stock(self):
        Script = self.env['script.tools']
        orders = self.purchase_order_line_ids.filtered(lambda line: line.product_qty > line.qty_received)
        return Script.open_records(orders, name=_('Ordered quantity'))
