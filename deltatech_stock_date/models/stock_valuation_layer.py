# ©  2015-2021 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"
    _order = "date, id"

    date = fields.Datetime(related="stock_move_id.date", store=True, string="Move Date")

    def create(self, vals_list):
        res = super(StockValuationLayer, self).create(vals_list)
        if self._context.get('force_period_date'):
            for each_rec in res:
                self.env.cr.execute("update stock_valuation_layer set create_date = %s where id = %s", (self._context.get('force_period_date'), each_rec.id))
        return res
