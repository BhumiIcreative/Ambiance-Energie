# coding: utf-8


from odoo import api, fields, models, tools, _

import logging
log = logging.getLogger(__name__).info

class PurchaseBillUnion(models.Model):
    _inherit = 'purchase.bill.union'

    stock_picking_bill_id = fields.Many2one('stock.picking', string=_('Stock picking'), readonly=True)
    purchase_order_line_id = fields.Many2one('purchase.order.line', string=_('PO line'))

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'purchase_bill_union')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW purchase_bill_union AS (
                SELECT
                    id, name, ref as reference, partner_id, date, amount_untaxed as amount, currency_id, company_id,
                    id as vendor_bill_id, NULL as purchase_order_id, CAST(NULL as integer) as stock_picking_bill_id, CAST(NULL as integer) as purchase_order_line_id
                FROM account_move
                WHERE
                    type='in_invoice' and state = 'posted'
            UNION
                SELECT
                    -id, name, partner_ref as reference, partner_id, date_order::date as date, amount_untaxed as amount, currency_id, company_id,
                    NULL as vendor_bill_id, id as purchase_order_id, CAST(NULL as integer) as stock_picking_bill_id, CAST(NULL as integer) as purchase_order_line_id
                FROM purchase_order
                WHERE
                    state in ('purchase', 'done') AND
                    invoice_status in ('to invoice', 'no')
            UNION
                SELECT
                    -a.id, a.external_ref as name, a.origin as reference, a.partner_id, a.date, SUM(c.price_subtotal) as amount, c.currency_id, a.company_id,
                    NULL as vendor_bill_id, NULL as purchase_order_id, a.id as stock_picking_bill_id, c.id as purchase_order_line_id
                FROM stock_picking a, stock_move b, purchase_order_line c
                WHERE
                    a.id = b.picking_id and b.purchase_line_id = c.id
                    and a.state in ('done')
                GROUP BY a.id, a.name, a.origin, a.partner_id, a.date, c.currency_id, a.company_id, a.id, c.id
            )""")
