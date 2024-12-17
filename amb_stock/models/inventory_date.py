import logging
from odoo import api, fields, models, _
from odoo.tools.misc import format_datetime

log = logging.getLogger(__name__).info

class StockValuationLayerReport(models.AbstractModel):
    _name = 'report.amb_stock.report_stock_valuation_layer'
    _description = 'Stock valuation layer report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.valuation.layer'].browse(docids)
        last_inventory_date = self.env['stock.quantity.history'].search([])[-1]
        inventory_datetime = last_inventory_date.inventory_datetime

        return {
            'doc_model': 'stock.valuation.layer',
            'docs': docs,
            'inventory_datetime': inventory_datetime
        }
