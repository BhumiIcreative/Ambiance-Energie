import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from math import *


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    client_situation = fields.Monetary(string='Client situation',
                                       compute='_compute_client_situation',
                                       store=True)
    current_subscription = fields.Many2one('subscription.wood.pellet',
                                           string='Current Subscription Wood Pellet',
                                           compute='_get_subscription',
                                           store=True)
    amount_left_to_pay = fields.Monetary(string='Amount Left To Pay',
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
    oci_point_of_sale = fields.Many2one('x_point_de_vente',
                                        string='Point of sale')
    advance = fields.Monetary(string='Advance', tracking=True, copy=False)
    advance_payment_instrument_id = fields.Many2one(
        'sale_timeline.payment.instrument',
        string='Advance payment method',
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
            Compute amount_left_to_pay
        """
        for sale_id in self :
            sale_id.amount_left_to_pay = sale_id.amount_total - sale_id.advance

    @api.depends('partner_id', 'partner_id.total_due')
    def _compute_client_situation(self):
        """
            Compute client_situation
        """
        for sale_id in self:
            sale_id.client_situation = -sale_id.partner_id.total_due

    @api.depends('type_order', 'partner_id')
    def _get_subscription(self):
        """
            Compute current_subscription
        """
        for sale_id in self:
            sale_id.current_subscription = self.env['subscription.wood.pellet'].search([
                ('partner_id', '=', sale_id.partner_id.id),
                ('date_start', '<', datetime.datetime.now()),
                ('date_end', '>', datetime.datetime.now()),
        ])
    #
    @api.depends('amount_total', 'payment_timeline_ids', 'advance')
    def _compute_amount_missing_from_timeline(self):
        super()._compute_amount_missing_from_timeline()
        for sale in self:
            sale.amount_missing_from_timeline -= sale.advance

    @api.onchange('type_order','partner_id')
    def granule_product_proposal(self):
        """
            Automatically adds a granule product to the order if:

            1. The order type is 'gran'.
            2. The granule product is not already in the order.

            It calculates how many granules the customer can buy based on their
            subscription and the price of the granules, and then adds the
            product to the order with the appropriate details (price,
            quantity, etc.).
        """
        # Search for the product with default code 'GRANULE'
        article_granule = self.env['product.product'].search([
            ('default_code', '=', 'GRANULE'),
        ]).id
        # Check if the 'type_order' is 'gran' and the product is not already in the order lines
        if self.type_order == 'gran' and article_granule not in self.order_line.mapped('product_id').ids:
            sub = self.current_subscription # Get the current subscription
            if sub:
                price_article = sub.price # Extract price from subscription
                # Search for a specific tax by its name
                vat = self.env['account.tax'].search([
                    ('name', '=','TVA collectée (vente) 10,0%')
                ])

                # Calculate the number of granules the customer can purchase
                nb_granule = floor(sub.amount / (price_article + vat.amount / 100 * price_article))

                fiscal_position = self.fiscal_position_id
                article_granule.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)

                # Prepare values for adding a new order line
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
        """
            Automatically validates pending pickings and creates invoices for
            a sale order.

            1. Checks for pickings (deliveries or shipments) related to the
                sale order that are not yet completed or canceled.
            2. Validates these pickings to ensure all items are marked as
                delivered.
                - If validation fails, it attempts to force-validate the
                    pickings by marking all items as fully delivered.
            3. Create invoices using standard process (base).
            4. Links any advance payments made by the customer to the newly
                created invoice.
        """
        to_validate_pickings = self.picking_ids.filtered(lambda x: x.state not in ('cancel', 'done'))
        # Gather all pickings that are not canceled or completed
        if to_validate_pickings:
            # Validate each pending picking
            for picking in to_validate_pickings:
                try:
                    # Attempt to validate the picking
                    picking.button_validate()
                    if picking.state != 'done':
                        # Process the picking if it remains incomplete
                        picking.process()
                except Exception:
                    # Force validation for any pickings that fail validation
                    for line in picking.move_ids_without_package:
                        # Ensure the reserved quantity matches the product quantity
                        line.reserved_availability = line.product_uom_qty
                        line.quantity_done = line.product_uom_qty
                    # Attempt validation again
                    picking.button_validate()
                    if picking.state != 'done':
                        picking.process()
        # Call the default behavior for creating invoices
        invoice = super(SaleOrder, self)._create_invoices()
        # Link advance payments to the newly created invoice
        if self.advance_payment_ids:
            for payment in self.advance_payment_ids:
                payment.invoice_ids = [(4, invoice.id)]

    def counter_sale_confirm(self):
        """
            Confirms the sale order, validates related stock pickings, and
            creates invoices.

            1. Confirms the sale order using the standard confirmation process.
            2. If the sale order is marked as a counter sale:
               - Validates all related stock pickings.
               - If validation fails, forces validation by marking items as
                fully delivered.
            3. Creates invoices for the sale order.
            4. Links any advance payments to the created invoices.
            5. Returns the view of the created invoices for further actions.
        """
        super(SaleOrder, self).action_confirm()
        if self.counter_sale:
            for picking in self.picking_ids:
                try:
                    picking.button_validate()
                    if picking.state != 'done':
                        picking.process()
                except Exception:
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
        """
            Confirms the order after checking the subscription amount.

            - If the order type is 'gran', ensures the subscription has enough
            funds.
           - If not, it shows an error and stops the process.
           - If everything is fine, it confirms the order and processes it as
           a counter sale.

           Returns:
               The result of confirming and processing the order.
       """
        if self.type_order == 'gran' and self.amount_left_to_pay > self.current_subscription.amount:
            raise UserError(_('You can\'t confirm the quotation, amount in subscription is not sufficient'))
        return self.counter_sale_confirm()

    def _prepare_invoice(self):
        """
            Prepares invoice data with additional fields for advance payments.

            - Calls the base method to get the default invoice values.
            - Checks if an advance payment is defined and a specific payment
            term exists.
            - Adds the payment term, advance amount, and related payment IDs
            to the invoice.

            Returns:
                dict: Prepared invoice data with additional advance payment
                details.
        """
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
        journal = self.env['account.journal'].search([
                ('code', '=', 'ECH'),('company_id', '=', self.company_id.id)
        ],limit=1)
        if not journal:
            raise UserError(_('no journal found'))
        payment_res = {
            'payment_type': 'inbound',
            'partner_id': self.partner_id.id,
            'partner_type': 'customer',
            'journal_id': journal.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'payment_date': self.date_order,
            'amount': self.advance,
            'sale_id': self.id,
            'payment_instrument_id': self.advance_payment_instrument_id.id,
            'oci_point_of_sale': self.oci_point_of_sale.id,
            'ref': "Acompte sur devis " + self.name,
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id
        }
        print("\n\n\n ########### _prepare_payment payment_res: ", payment_res)
        return payment_res

    def create_payment(self):
        payment = self._prepare_payment()
        print("\n\n\n ########### create_payment payment: ", payment)
        payment_id = self.env['account.payment'].create(payment)
        self.advance_payment_ids = [(4, payment_id.id)]

    def action_sale_confirm_advance(self):
        if self.advance_state == 'not_confirmed':
            self.create_payment()
            self.advance_state = 'confirmed'
