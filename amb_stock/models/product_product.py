import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)
log = _logger.info


class ProductProduct(models.Model):
    _inherit = 'product.product'

    free_qty = fields.Float(string='Saleable quantity', compute='_cpt_free_qty', store=True, readonly=True)
    net_qty = fields.Float(string='Net quantity', compute='_cpt_net_qty', store=True, readonly=True)
    order_qty = fields.Float(string='Order Stock', compute='_cpt_order_qty', store=True, readonly=True)
    purchase_order_line_ids = fields.One2many('purchase.order.line', 'product_id', string='Purchase order lines')
    purchase_order_ids = fields.Many2many('purchase.order', string='Purchase order', compute='_cpt_purchase_order_ids',
                                          store=True)

    @api.depends(
        'qty_available',
        'product_variant_ids.stock_move_ids.product_uom_qty',
        'stock_move_ids.product_uom_qty',
        'stock_move_ids.state')
    def _cpt_free_qty(self):
        """ Computes the free quantity available for products """
        for product_id in self:
            customer_location_id = product_id.env.ref('stock.stock_location_customers').id
            reserved_move_line_not_done = product_id.env['stock.move.line'].search([
                ('product_id', '=', product_id.id),
                ('state', '=', 'assigned'),
                ('location_dest_id', '=', customer_location_id),
            ])
            reserved_qty_not_done = sum(reserved_move_line_not_done.move_id.mapped('product_uom_qty'))
            product_id.free_qty = product_id.qty_available - reserved_qty_not_done

    def action_view_stock_move_lines_free_qty(self):
        """ Opens a view for stock move lines related to free quantity """
        for art in self:
            action = art.env.ref('stock.stock_move_line_action').read()[0]
            action.update({
                'domain': [('product_id', '=', art.id)],
                'context': eval(action['context'])
            })
            action['context']['search_default_done'] = 0
            return action

    @api.depends(
        'purchase_order_line_ids',
        'purchase_order_line_ids.product_id',
        'purchase_order_line_ids.order_id',
        'purchase_order_ids',
        'purchase_order_ids.state'
    )
    def _cpt_order_qty(self):
        """ Computes the remaining order quantity for products """
        for product_id in self:
            line_ids = self.env['purchase.order.line'].search([
                ('id', 'in', product_id.purchase_order_line_ids.ids),
                ('order_id.state', 'in', ['purchase', 'done']),
            ]).filtered(lambda line: line.product_qty > line.qty_received)
            product_id.order_qty = sum(line_ids.mapped('product_qty')) - sum(line_ids.mapped('qty_received'))

    def action_view_ordered_stock(self):
        """ Opens a view for stock lines related to ordered but not yet received quantity """
        return self.env['script.tools'].open_records(
            self.purchase_order_line_ids.filtered(lambda line: line.product_qty > line.qty_received),
            name=_('Ordered quantity'))

    @api.depends(
        'purchase_order_line_ids',
        'purchase_order_line_ids.product_id',
        'purchase_order_line_ids.order_id',
        'purchase_order_ids',
        'purchase_order_ids.state'
    )
    def _cpt_net_qty(self):
        """ Computes the net quantity for products """
        for product_id in self:
            product_id.net_qty = product_id.qty_available + product_id.order_qty

    @api.depends('purchase_order_line_ids', 'purchase_order_line_ids.product_id', 'purchase_order_line_ids.order_id')
    def _cpt_purchase_order_ids(self):
        """ Computes the related purchase order IDs for the product """
        for product_id in self:
            product_id.purchase_order_ids = [(5, 0, 0)]
            line_ids = product_id.purchase_order_line_ids
            if line_ids:
                product_id.purchase_order_ids = [(6, 0, line_ids.mapped('order_id').ids)]

    def action_view_stock_move_lines_net_qty(self):
        """ Opens a view for stock move lines related to net quantity """
        return self.env['script.tools'].open_records(
            self.purchase_order_line_ids.filtered(lambda line: line.qty_received > 0), name=_('Received quantity'))
