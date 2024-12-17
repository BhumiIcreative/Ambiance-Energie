# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

import datetime

import logging
log = logging.getLogger(__name__).info


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _autopost_draft_entries_asc(self):
        ''' This method is called from a cron job.
        It is used to post entries such as those created by the module
        account_asset.
        '''
        records = self.search([
            ('state', '=', 'draft'),
            ('date', '<=', fields.Date.context_today(self)),
            ('auto_post', '=', True),
        ], order='id asc')
        for ids in self._cr.split_for_in_conditions(records.ids, size=1000):
            self.browse(ids).post()
            if not self.env.registry.in_test_mode():
                self._cr.commit()

    # @api.onchange('purchase_vendor_bill_id', 'purchase_id', 'purchase_stock_picking_bill_id')
    # def _onchange_purchase_auto_complete(self):
    #     if self.purchase_vendor_bill_id.stock_picking_bill_id:
    #         self.purchase_stock_picking_bill_id = self.purchase_vendor_bill_id.stock_picking_bill_id.id
    #         po_lines = self.purchase_stock_picking_bill_id.move_ids_without_package
    #         new_lines = self.env['account.move.line']
    #         for line in po_lines:
    #             log(line.quantity_done)
    #             if line.quantity_done != 0 :
    #                 new_line = new_lines.new(line.purchase_line_id._prepare_account_move_line(self))
    #                 new_line.quantity = line.quantity_done
    #                 new_line.account_id = new_line._get_computed_account()
    #                 new_line._onchange_price_subtotal()
    #                 new_lines += new_line
    #         new_lines._onchange_mark_recompute_taxes()
    #         self._onchange_currency()
    #     super(AccountMove, self)._onchange_purchase_auto_complete()
    #     for invoice_line in self.invoice_line_ids:
    #         if invoice_line.quantity == 0:
    #             self.invoice_line_ids = [(2, invoice_line.id)]

    def _compute_origin_so(self):
        for rec in self:
            rec.origin_so = rec.invoice_line_ids.mapped('sale_line_ids').order_id[:1]

    client_situation = fields.Monetary(string=_('Client situation'), related='partner_id.total_due')
    current_subscription = fields.Many2one('subscription.wood.pellet', string=_('Current subscription wood pellet'))
    package_count = fields.Integer(string=_('Package count'))
    weight = fields.Float(string=_('Weight'))
    volume = fields.Float(string=_('Volume'))
    port = fields.Float(string=_('Port'))
    shipped = fields.Float(string=_('Shipped'))
    comment = fields.Char(string=_('Comment'))
    commissioning_identification = fields.Char(string=_('Identification'))
    type_invoice = fields.Selection([
        ('std',_('Standard')),
        ('gran',_('Granule')),
        ('serv',_('Service')),
        ('sto',_('Stove'))
    ], string=_('Type invoice'), default='std')
    purchase_stock_picking_bill_id = fields.Many2one('stock.picking',
        store=False,
        readonly=True,
        states={'draft': [('readonly', False)]},
        string='Stock picking',
        help="Auto-complete from a Stock picking.")
    oci_point_of_sale = fields.Many2one('x_point_de_vente', string=_('Point of sale'))
    sent_by = fields.Many2one('res.partner', string=_('Sent by'))
    origin_so = fields.Many2one('sale.order', compute=_compute_origin_so)

    @api.constrains('oci_point_of_sale')
    def _check_point_of_sale(self):
        for r in self:
            if r.type in ('out_refund','out_invoice') and r.type_invoice == 'std' and not r.oci_point_of_sale:
                raise ValidationError("Point of sale is required on standard invoice")

    @api.model
    def create(self, vals):
        if vals.get('invoice_origin'):
            sale = self.env['sale.order'].search([('name','=',vals['invoice_origin'])])
            if sale:
                vals.update({
                    'type_invoice': sale.type_order,
                    # 'advance': sale.advance,
                    'current_subscription': sale.current_subscription.id,
                    'oci_point_of_sale': sale.oci_point_of_sale.id,
                    'payment_instrument_id': sale.payment_instrument_id.id
                })
        invoice = super(AccountMove, self).create(vals)
        return invoice

    def action_post(self):
        if self.type_invoice == 'gran' and self.amount_total > self.current_subscription.amount:
            raise UserError(_('You can\'t confirm the quotation, amount in subscription is not sufficient'))
        res = super(AccountMove, self).action_post()

        if self.type_invoice == 'gran':
            # register payment
            subscription = self.env['subscription.wood.pellet'].search([('partner_id','=',self.partner_id.id),
                                                                           ('date_start', '<', datetime.datetime.now()),
                                                                           ('date_end', '>', datetime.datetime.now()),
            ])
            if subscription:
                if subscription.amount < self.amount_total:
                    raise ValidationError(_("Invoice amount is greater than balance subscription."))
                else:
                    vals = {
                        'amount': self.amount_total,
                        'journal_id': self.env['account.journal'].search([('code','=','BNK1')]).id,
                        'payment_date': datetime.datetime.now(),
                        'payment_type': 'inbound',
                        'partner_type': 'customer',
                        'payment_method_id': self.env['account.payment.method'].search([('code','=','manual'),('payment_type','=','inbound')]).id,
                        'partner_id': self.partner_id.id,
                        'communication': self.name,
                        'invoice_ids': [(6, 0, [self.id])],
                        'company_id': self.company_id.id,
                    }
                    payment = self.env['account.payment'].create(vals)
                    payment.action_register_payment()
        return res

    def generate_invoice_rest_payments(self):

        in_need_of_action = self.env['account.move'].search([
            ('state', 'in', ['posted']),
            ('amount_residual', '!=', 0),
            ('type', 'in',['out_invoice'])
            ])

        for move in in_need_of_action:
            try:
                move._generate_invoice_rest_payments()
            except UserError as e:
                log.exception(e)

    def _generate_invoice_rest_payments(self):
        self.ensure_one()
        ####################
        # variables en dur #
        ####################
        if self.company_id.id == 1:  # société Ambiance Energie
            var_journal_id = 12
        if self.company_id.id == 2:  # société Ambiance Energie
            var_journal_id = 40

        payment_res = {
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'state': 'draft',
            'invoice_ids': [(6, 0, self.ids)],
            'partner_id': self.partner_id.id,
            'amount': self.amount_residual,
            'payment_date': self.invoice_date,
            'journal_id': var_journal_id,
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            'communication': self.name + ' / reste à payer',
            'company_id': self.company_id.id,
            'oci_point_of_sale': self.oci_point_of_sale.id,
            'payment_instrument_id': self.payment_instrument_id.id,
        }

        self._cr.execute('''
            SELECT SUM(amount)
            FROM account_payment
            WHERE id IN (
                SELECT payment_id FROM account_invoice_payment_rel WHERE invoice_id = %s
            )
        ''', [self.id])
        query_res = self._cr.fetchone()
        sum = query_res and query_res[0] or 0.0

        if sum < self.amount_total:
            res = self.env['account.payment'].create(payment_res)
            log('created %s',res)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    oci_point_of_sale = fields.Many2one('x_point_de_vente', string=_('Point of sale'), related='move_id.oci_point_of_sale')
    # Augmenter la précision de discount pour éviter les arrondis quand on travaille en remise fixe
    discount = fields.Float(digits=(14,10))
    discount_fixed = fields.Float(string="Discount (Fixed)", digits="Product Price", default=0.00, help="Fixed amount discount.")

    @api.onchange('discount')
    def _onchange_discount(self):
        self.discount_fixed = self.quantity * self.price_unit * self.discount / 100

    @api.onchange('discount_fixed', 'quantity', 'price_unit')
    def _onchange_discount_fixed(self):
        if self.price_unit == 0.00 or self.quantity == 0.00:
            self.discount = 0.00
        else:
            self.discount = self.discount_fixed / (self.quantity * self.price_unit) * 100
