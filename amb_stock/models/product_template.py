import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)
log = _logger.info


class productTemplate(models.Model):
    _inherit = 'product.template'

    free_qty = fields.Float(string='Saleable quantity', compute='_cpt_custom_qty', store=True, readonly=True)
    net_qty = fields.Float(string='Net quantity', compute='_cpt_custom_qty', store=True, readonly=True)
    order_qty = fields.Float(string='Order Stock', compute='_cpt_custom_qty', store=True, readonly=True)

    @api.depends(
        'product_variant_ids',
        'product_variant_ids.net_qty',
        'product_variant_ids.order_qty',
        'product_variant_ids.free_qty',
        'product_variant_ids.stock_move_ids.product_uom_qty',
        'product_variant_ids.stock_move_ids.state',
    )
    def _cpt_custom_qty(self):
        """ Calculate custom quantities for product templates from its variants """
        for template_id in self:
            template_id.update({
                'net_qty': sum(template_id.product_variant_ids.mapped('net_qty')),
                'order_qty': sum(template_id.product_variant_ids.mapped('order_qty')),
                'free_qty': sum(template_id.product_variant_ids.mapped('free_qty'))
            })

    def action_view_stock_move_lines_free_qty(self):
        """ Opens a view for stock move lines related to free quantity """
        for product_tmpl in self:
            action = product_tmpl.env.ref('stock.stock_move_line_action').read()[0]
            action.update({
                'domain': [('id', '=', product_tmpl.id)],
                'context': eval(action['context'])
            })
            log(action)
            action['context']['search_default_done'] = 0
            return action

    def action_view_stock_move_lines_net_qty(self):
        """ Opens a view for stock move lines related to net quantity """
        for product in self.product_variant_ids:
            lines = product.purchase_order_line_ids.filtered(lambda line: line.qty_received > 0)
        return self.env['script.tools'].open_records(lines, name=_('Received quantity'))

    def action_view_ordered_stock(self):
        """ Opens a view for stock lines related to ordered but not yet received quantity """
        for product in self.product_variant_ids:
            lines = product.purchase_order_line_ids.filtered(lambda line: line.product_qty > line.qty_received)
        return self.env['script.tools'].open_records(lines, name=_('Ordered quantity'))
