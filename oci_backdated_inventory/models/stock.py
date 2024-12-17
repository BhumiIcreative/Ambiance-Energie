# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import models, fields, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)

class Stock_Move(models.Model):
    _inherit = 'stock.move'

    def _action_done(self,cancel_backorder=False):
        res = super(Stock_Move, self)._action_done(cancel_backorder)
        for each_move in res:
            if each_move.inventory_id and each_move.inventory_id.is_backdated_inv:
                each_move.write(
                    {'date':each_move.inventory_id.inv_backdated or fields.Datetime.now(),
                    # 'date_deadline':each_move.inventory_id.inv_backdated or fields.Datetime.now(),
                    'note':each_move.inventory_id.backdated_remark, 'origin':each_move.inventory_id.backdated_remark})
                each_move.move_line_ids.write(
                    {'date':each_move.inventory_id.inv_backdated or fields.Datetime.now(),
                    'origin':each_move.inventory_id.backdated_remark})
        return res


class stock_inventory(models.Model):
    _inherit = 'stock.inventory'

    is_backdated_inv = fields.Boolean(string="Is Backdated Inventory?",copy=False)
    inv_backdated = fields.Date(string="Inventory Backdate",copy=False)
    backdated_remark = fields.Char(string="Notes", copy=False)
    prefill_counted_quantity = fields.Selection(string='Counted Quantities',
        help="Allows to start with a pre-filled counted quantity for each lines or "
        "with all counted quantities set to zero.", default='at_date',
        selection=[('counted', 'Default to stock on hand'), ('zero', 'Default to zero'), ('at_date', 'Default to stock at date')])

    def post_inventory(self):
        for inventory in self:
            date = inventory.accounting_date or inventory.date
            if inventory.is_backdated_inv:
                date = inventory.inv_backdated
        return super(stock_inventory, inventory.with_context(force_period_date=date)).post_inventory()

    def _get_quantities(self):

        res = super()._get_quantities()
        if self.prefill_counted_quantity == 'at_date':
            #dict with qty to date
            qty_to_date = {}
            for product in self.product_ids:
                qty_to_date[product.id] = product.with_context({'to_date': self.inv_backdated}).qty_available
            #update return dict with qty to date
            for quant in res:
                res[quant] = qty_to_date[quant[0]]
        return res

class stock_valuation_layer(models.Model):
    _inherit = 'stock.valuation.layer'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(stock_valuation_layer, self).create(vals_list)
        if self._context.get('force_period_date'):
            for each_rec in res:
                self.env.cr.execute("update stock_valuation_layer set create_date = %s where id = %s", (self._context.get('force_period_date'), each_rec.id))
        return res
