# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError, Warning
import datetime
from math import *

import logging
log = logging.getLogger(__name__).info


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('amount_total', 'advance')
    def _compute_amount_left_to_pay(self):
        for sale_id in self :
            sale_id.amount_left_to_pay = sale_id.amount_total - sale_id.advance

    @api.depends('partner_id', 'partner_id.total_due')
    def _compute_client_situation(self):
        for sale_id in self:
            sale_id.client_situation = -sale_id.partner_id.total_due

    @api.depends('type_order', 'partner_id')
    def _get_subscription(self):
        for sale_id in self:
            sale_id.current_subscription = self.env['subscription.wood.pellet'].search([
                ('partner_id', '=', sale_id.partner_id.id),
                ('date_start', '<', datetime.datetime.now()),
                ('date_end', '>', datetime.datetime.now()),
        ])

    client_situation = fields.Monetary(string=_('Client situation'), compute='_compute_client_situation')
    current_subscription = fields.Many2one('subscription.wood.pellet', string=_('Current subscription wood pellet'), compute='_get_subscription')
    amount_left_to_pay = fields.Monetary(string=_('Amount left to pay'), compute='_compute_amount_left_to_pay', store=True)
    counter_sale = fields.Boolean(string=_("Counter sale"), default=True)
    type_order = fields.Selection([
        ('std',_('Standard')),
        ('gran',_('Granule')),
        ('serv',_('Service')),
        ('sto',_('Stove')),
    ], string=_('Type order'), default='std')
    sponsorship = fields.Char(_('Sponsorship'))
    oci_point_of_sale = fields.Many2one('x_point_de_vente', string=_('Point of sale'))
    advance = fields.Monetary(_('Advance'), track_visibility='always', digits=(14, 10), copy=False)
    advance_payment_instrument_id = fields.Many2one('sale_timeline.payment.instrument', string=_('Advance payment method'), copy=False)
    advance_state = fields.Selection([
        ('not_confirmed', 'Not Confirmed'),
        ('confirmed', 'Confirmed')
    ] , default='not_confirmed', copy=False)
    advance_payment_ids = fields.One2many('account.payment', 'sale_id', string="advance payments", copy=False)

    @api.depends('amount_total', 'payment_timeline_ids', 'advance')
    def _compute_amount_missing_from_timeline(self):
        super()._compute_amount_missing_from_timeline()
        for sale in self:
            sale.amount_missing_from_timeline -= sale.advance

    @api.onchange('type_order','partner_id')
    def granule_product_proposal(self):
        article_granule = self.env['product.product'].search([
            ('default_code', '=', 'GRANULE'),
        ])
        if self.type_order == 'gran' and article_granule not in self.order_line.mapped('product_id').ids:
            sub = self.current_subscription
            if sub:
                price_article = sub.price
                vat = self.env['account.tax'].search([
                    ('name', '=','TVA collectée (vente) 10,0%')
                ])

                nb_granule = floor(sub.amount / (price_article + vat.amount / 100 * price_article))

                fiscal_position = self.fiscal_position_id
                accounts = article_granule.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)

                vals = {
                    'product_id': article_granule.id,
                    'product_uom': article_granule.uom_id.id,
                    'name': article_granule.display_name,
                    'product_uom_qty': nb_granule,
                    'price_unit': price_article
                }
                vals = self.env['sale.order.line']._add_missing_default_values(vals)
                self.order_line = [(0, 0, vals)]

    @api.onchange('oci_point_of_sale')
    def onchange_pos(self):
        values = {}
        if self.oci_point_of_sale:
            values['warehouse_id'] = self.oci_point_of_sale.x_studio_entrepot
            self.update(values)
 
    def _create_invoices(self, grouped=False, final=False, date=None):
        to_validate_pickings = self.picking_ids.filtered(lambda x: x.state not in ('cancel', 'done'))
        if to_validate_pickings:
            for picking in to_validate_pickings:
                try:
                    picking.button_validate()
                    if picking.state != 'done':
                        picking.process()
                except Exception as e:
                    for line in picking.move_ids_without_package:
                        line.reserved_availability = line.product_uom_qty
                        line.quantity_done = line.product_uom_qty
                    picking.button_validate()
                    if picking.state != 'done':
                        picking.process()
        invoice = super(SaleOrder, self)._create_invoices()
        if self.advance_payment_ids:
            for payment in self.advance_payment_ids:
                payment.invoice_ids = [(4, invoice.id)]

    def counter_sale_confirm(self):
        super(SaleOrder, self).action_confirm()
        if self.counter_sale:
            for picking in self.picking_ids:
                try:
                    picking.button_validate()
                    if picking.state != 'done':
                        picking.process()
                except Exception as e:
                    for line in picking.move_ids_without_package:
                        line.reserved_availability = line.product_uom_qty
                        line.quantity_done = line.product_uom_qty
                    picking.button_validate()
                    if picking.state != 'done':
                        picking.process()

                    invoice = super(SaleOrder, self)._create_invoices()
                    if self.advance_payment_ids:
                        for payment in self.advance_payment_ids:
                            payment.invoice_ids = [(4, invoice.id)]
        return self.action_view_invoice()

    def action_confirm(self):
        if self.type_order == 'gran' and self.amount_left_to_pay > self.current_subscription.amount:
            raise UserError(_('You can\'t confirm the quotation, amount in subscription is not sufficient'))
        return self.counter_sale_confirm()

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        payment_term = self.env['account.payment.term'].search([
                    ('name', 'ilike', 'Echéancier de paiement')
                ],order='create_date desc', limit=1)
        if self.advance > 0 and payment_term:
            res['invoice_payment_term_id'] = payment_term.id
            res['advance'] = self.advance
            res['advance_payment_ids'] = self.advance_payment_ids
        return res

    def _prepare_payment(self):

        company = self.company_id
        journal = self.env['account.journal'].search([
                ('code', '=', 'ECH'),('company_id', '=', company.id)
        ],limit=1)
        if not journal:
            raise UserError(_('no journal found'))
        payment_res = {'payment_type': 'inbound',
                       'partner_id': self.partner_id.id,
                       'partner_type': 'customer',
                       'journal_id': journal.id,
                       'company_id': company.id,
                       'currency_id': self.currency_id.id,
                       'payment_date': self.date_order,
                       'amount': self.advance,
                       'sale_id': self.id,
                       'payment_instrument_id': self.advance_payment_instrument_id.id,
                       'oci_point_of_sale': self.oci_point_of_sale.id,
                       'communication': _("Acompte sur devis ") + self.name,
                       'payment_method_id': self.env.
                           ref('account.account_payment_method_manual_in').id
                       }
        return payment_res

    def create_payment(self):
        payment = self._prepare_payment()
        payment_id = self.env['account.payment'].create(payment)
        self.advance_payment_ids = [(4, payment_id.id)]

    def action_sale_confirm_advance(self):
        if self.advance_state == 'not_confirmed':
            self.create_payment()
            self.advance_state = 'confirmed'

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Augmenter la précision de discount pour éviter les arrondis quand on travaille en remise fixe
    discount = fields.Float(digits=(14,10))
    discount_fixed = fields.Float(string="Discount (Fixed)", digits="Product Price", default=0.00, help="Fixed amount discount.")

    @api.onchange('discount')
    def _onchange_discount(self):
        self.discount_fixed = self.product_uom_qty * self.price_unit * self.discount / 100

    @api.onchange('price_subtotal')
    def _onchange_price_unit(self):
        if self.price_subtotal < self.product_id.min_price:
            return {
                'warning':
                    {
                        'title': _('Warning'),
                        'message': (_('Vérifiez le prix sur la ligne %s, prix minimum %s') % (self.product_id.name,self.product_id.min_price)),
                    },
            }

    @api.onchange('discount_fixed', 'product_uom_qty', 'price_unit')
    def _onchange_discount_fixed(self):
        if self.price_unit == 0.00 or self.product_uom_qty == 0.00:
            self.discount = 0.00
        else:
            self.discount = self.discount_fixed / (self.product_uom_qty * self.price_unit) * 100

    def _prepare_invoice_line(self):
        res = super()._prepare_invoice_line()
        res['discount_fixed'] = self.discount_fixed
        return res

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    sale_id = fields.Many2one('sale.order')
