import datetime
from math import *

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    client_situation = fields.Monetary(
        string='Client Situation',
        compute='_compute_client_situation',
        store=True)
   
    amount_left_to_pay = fields.Monetary(
        string='Amount Left To Pay',
        compute='_compute_amount_left_to_pay',
        store=True)
    counter_sale = fields.Boolean(string="Counter Sale", default=True)
    type_order = fields.Selection([
        ('std', 'Standard'),
        ('gran', 'Granule'),
        ('serv', 'Service'),
        ('sto', 'Stove'),
    ], string='Type Order', default='std')
    sponsorship = fields.Char(string='Sponsorship')
    oci_point_of_sale = fields.Many2one('oci.point.of.sale',
                                        string='Point of Sale')
    advance = fields.Monetary(string='Advance', tracking=True, copy=False)
    advance_payment_instrument_id = fields.Many2one(
        'sale_timeline.payment.instrument',
        string='Advance Payment Method',
        copy=False)
    advance_state = fields.Selection([
        ('not_confirmed', 'Not Confirmed'),
        ('confirmed', 'Confirmed')
    ], string='Advance State', default='not_confirmed', copy=False)
    advance_payment_ids = fields.One2many('account.payment',
                                          'sale_id',
                                          string="Advance Payments",
                                          copy=False)

    @api.depends('amount_total', 'advance')
    def _compute_amount_left_to_pay(self):
        """
            Calculates how much money the customer still owes after
            considering their advance payment.
        """
        for sale_id in self:
            sale_id.amount_left_to_pay = sale_id.amount_total - sale_id.advance

    @api.depends('partner_id', 'partner_id.total_due')
    def _compute_client_situation(self):
        """
            Shows the customer's financial situation, like how much they owe.
        """
        for sale_id in self:
            sale_id.client_situation = -sale_id.partner_id.total_due

   
    @api.depends('amount_total', 'payment_timeline_ids', 'advance')
    def _compute_amount_missing_from_timeline(self):
        """
            Adjusts payment schedules by taking into account any advance
            payments made.
        """
        super()._compute_amount_missing_from_timeline()
        for sale in self:
            sale.amount_missing_from_timeline -= sale.advance

    

    @api.onchange('oci_point_of_sale')
    def onchange_pos(self):
        """
            Updates the warehouse details based on the selected point of sale.
        """
        values = {}
        if self.oci_point_of_sale:
            values['warehouse_id'] = self.oci_point_of_sale.entrepot
            self.update(values)

    def _create_invoices(self, grouped=False, final=False, date=None):
        """
            Automatically processes delivery orders linked to the sale and
            generates invoices. If advance payments exist, links them to the
            generated invoice.
        """
        # Filter delivery orders (pickings) that are not canceled or completed
        to_validate_pickings = self.picking_ids.filtered(
            lambda x: x.state not in ('cancel', 'done'))
        if to_validate_pickings:
            for picking in to_validate_pickings:
                try:
                    # Try to validate the delivery (process the picking)
                    picking.button_validate()
                    if picking.state != 'done':
                        picking._action_done()

                except Exception:
                    # Handle any errors that occur during validation
                    for line in picking.move_ids_without_package:
                        # Ensure all move lines have quantities marked as done
                        line.quantity = line.product_uom_qty

                    # Retry validation and processing
                    picking.button_validate()
                    if picking.state != 'done':
                        picking._action_done()

        invoice = super(SaleOrder, self)._create_invoices()

        # If there are any advance payments, link them to the generated invoice
        if self.advance_payment_ids:
            for payment in self.advance_payment_ids:
                payment.ac_id = invoice.id

    def counter_sale_confirm(self):
        """
            Confirms counter sales, processes related deliveries,
            generates invoices, and links advance payments to the invoice
            if applicable.
        """
        super(SaleOrder, self).action_confirm()
        if self.counter_sale:
            for picking in self.picking_ids:
                try:
                    # Try to validate the delivery order (this ensures items are ready for shipment)
                    picking.button_validate()
                    if picking.state != 'done':
                        picking._action_done()

                except Exception:
                    # Handle any exceptions that occur during the validation process
                    for line in picking.move_ids_without_package:
                        # Make sure all delivery lines have their quantities set correctly
                        line.quantity = line.product_uom_qty

                    # Retry validating and processing the picking
                    picking.button_validate()
                    if picking.state != 'done':
                        picking._action_done()

                    invoice = super(SaleOrder, self)._create_invoices()

                    # If advance payments were made, link them to the generated invoice
                    if self.advance_payment_ids:
                        for payment in self.advance_payment_ids:
                            payment.ac_id = invoice.id

        # Return to the invoice view after processing counter sale
        return self.action_view_invoice()

    
    def _prepare_invoice(self):
        """
            Prepares the invoice with specific payment terms and advance
            details.
        """
        res = super()._prepare_invoice()
        payment_term = self.env['account.payment.term'].search([
            ('name', 'ilike', 'Echéancier de paiement')
        ], order='create_date desc', limit=1)
        if self.advance > 0 and payment_term:
            res.update({
                'invoice_payment_term_id': payment_term.id,
                'advance': self.advance,
                'advance_payment_ids': self.advance_payment_ids
            })
        return res

    def create_payment(self):
        """
            Creates a payment record for the advance amount in the order.
        """
        journal = self.env['account.journal'].search([
            ('code', '=', 'ECH'), ('company_id', '=', self.company_id.id)
        ], limit=1)
        if not journal:
            raise UserError(_('No Journal Found.'))

        self.update({
            'advance_payment_ids':
                [(4, self.env['account.payment'].create({
                    'payment_type': 'inbound',
                    'partner_id': self.partner_id.id,
                    'partner_type': 'customer',
                    'journal_id': journal.id,
                    'company_id': self.company_id.id,
                    'currency_id': self.currency_id.id,
                    'date': self.date_order,
                    'amount': self.advance,
                    'sale_id': self.id,
                    'payment_instrument_id': self.advance_payment_instrument_id.id,
                    'oci_point_of_sale': self.oci_point_of_sale.id,
                    'ref': "Acompte sur devis " + self.name,
                    'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id}).id)],
            'advance_state': 'confirmed'
        })

    def action_sale_confirm_advance(self):
        """
            Confirms the sale only after the advance payment has been recorded.
        """
        if self.advance_state == 'not_confirmed':
            self.create_payment()
