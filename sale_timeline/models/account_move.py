from odoo import models, fields, api
from odoo.exceptions import UserError



class AccountMove(models.Model):
    _inherit = 'account.move'

    def _valid_field_parameter(self, field, name):
        return name == 'digits' or super()._valid_field_parameter(field, name)

    payment_timeline_ids = fields.One2many(
        'payment.timeline', 'move_id', string='Payment Timeline')
    is_timeline = fields.Boolean('Is Timeline ?',
                                 compute='_compute_is_timeline', store=True, default=False)
    payment_instrument_id = fields.Many2one(
        'sale_timeline.payment.instrument', string='Payment Method')
    amount_missing_from_timeline = fields.Monetary(string="Amount Missing from Payment Timeline",
                                                   compute="_compute_amount_missing_from_timeline")
    advance = fields.Monetary('Advance', digits=(14, 10))
    advance_payment_ids = fields.One2many(
        'account.payment', 'ac_id', string="Advance Payments")

    @api.depends('amount_total', 'payment_timeline_ids')
    def _compute_amount_missing_from_timeline(self):
        for move in self:
            move.amount_missing_from_timeline = move.amount_total - move.edf_prime if move.edf_prime else move.amount_total
            for payment_timeline in move.payment_timeline_ids:
                move.amount_missing_from_timeline -= payment_timeline.amount

    @api.depends('invoice_payment_term_id')
    def _compute_is_timeline(self):
        for move in self:
            move.is_timeline = move.invoice_payment_term_id.name == "Echéancier de paiement"

    @api.model
    def create(self, vals):
        if vals.get("invoice_origin"):
            sale = self.env["sale.order"].search(
                [("name", "=", vals["invoice_origin"])]
            )
            if sale:
                vals.update(
                    {
                        "payment_instrument_id": sale.payment_instrument_id.id,
                    }
                )
        return super().create(vals)

    def write(self, values):
        res = super().write(values)
        self._process_timeline(validate_timeline=False)
        return res

    def _create_advance_to_timeline(self):
        timelines = self.env['payment.timeline']
        for payment in self.advance_payment_ids:
            timelines.create({
                'amount': payment.amount,
                'date': payment.payment_date,
                'currency_id': payment.currency_id.id,
                'move_id': self.id,
                'payment_instrument_id': payment.payment_instrument_id.id,
                'advance': True,
            })
        return timelines

    def _process_timeline(self, validate_timeline=False):
        timeline_term_id = self.env.ref("sale_timeline.timeline_payment")
        if not self._context.get('force_bypass_timeline', False):
            if self.payment_timeline_ids and not self.invoice_payment_term_id:
                self.invoice_payment_term_id = timeline_term_id
            if self.invoice_payment_term_id.name == "Echéancier de paiement" and not self.payment_timeline_ids:
                amount = (self.advance if self.advance > 0 else 0) + (
                    self.edf_prime if self.edf_prime else 0)
                self.payment_timeline_ids = [(0, 0, {
                    'amount': self.amount_total - amount,
                    'date': fields.date.today(),
                    'currency_id': self.currency_id.id,
                    'move_id': self.id,
                    'payment_instrument_id': False,
                })]
                if self.advance > 0 and self.advance_payment_ids:
                    self._create_advance_to_timeline()
            if self.invoice_payment_term_id.move_id or self.invoice_payment_term_id == timeline_term_id:
                if validate_timeline:
                    self.validate_timeline()
                self.payment_timeline_ids.compute_payment_term_id()

    def _get_amount_validate_timeline(self):
        return self.amount_total - self.edf_prime if self.edf_prime else self.amount_total

    def validate_timeline(self):
        self.payment_timeline_ids.validate_amount(self._get_amount_validate_timeline())

    def action_post(self):
        self._process_timeline(validate_timeline=True)
        res = super().action_post()
        if self.move_type in ['out_invoice',
                              'out_refund'] and self.type_invoice != 'gran':
            ####################
            # variables en dur #
            ####################
            if self.company_id.id == 1:  # société Ambiance Energie
                var_journal_id = 12
            if self.company_id.id == 2:  # société Ambiance Energie
                var_journal_id = 40
            # FIN VARIABLES EN DUR #
            ########################

            # payment_type according to invoice type
            if self.move_type == 'out_invoice':  # facture client
                var_payment_type = 'inbound'  # encaissement
                amount = self.amount_total - (
                    self.edf_prime if self.edf_prime else 0)
            elif self.move_type == 'out_refund':  # avoir client
                var_payment_type = 'outbound'  # décaissement
                amount = self.amount_total - (
                    self.edf_prime if self.edf_prime else 0)
            if self.is_timeline:
                for payment_timeline_id in self.payment_timeline_ids.filtered(
                        lambda x: x.advance != True):
                    if (not payment_timeline_id.payment_instrument_id):
                        raise UserError(
                            "Please add a payment instrument on all the payment timelines")
                    payment_method_line_id = self.env['account.payment.method.line'].search(
                        [('payment_method_id', '=', self.env.ref(
                            'account.account_payment_method_manual_in').id),
                         ('journal_id', '=', var_journal_id)], limit=1)
                    self.env['account.payment'].create({
                        'payment_type': var_payment_type,
                        'partner_type': 'customer',
                        'state': 'draft',
                        'reconciled_invoice_ids': [(6, 0, self.ids)],
                        'partner_id': self.partner_id.id,
                        'amount': payment_timeline_id.amount,
                        'date': payment_timeline_id.date,
                        'journal_id': var_journal_id,
                        'payment_method_line_id': payment_method_line_id.id,
                        'ref': self.name + ' / ' + payment_timeline_id.payment_instrument_id.name,
                        'company_id': self.company_id.id,
                        'oci_point_of_sale': self.oci_point_of_sale.id,
                        'payment_instrument_id': payment_timeline_id.payment_instrument_id.id,
                    })
            else:
                payment_method_line_id = self.env['account.payment.method.line'].search(
                    [('payment_method_id', '=', self.env.ref(
                        'account.account_payment_method_manual_in').id),
                     ('journal_id', '=', var_journal_id)], limit=1)
                self.env['account.payment'].create({
                    'payment_type': var_payment_type,
                    'partner_type': 'customer',
                    'state': 'draft',
                    'reconciled_invoice_ids': [(6, 0, self.ids)],
                    'partner_id': self.partner_id.id,
                    'amount': amount,
                    'date': self.invoice_date,
                    'journal_id': var_journal_id,
                    'payment_method_line_id': payment_method_line_id.id,
                    'ref': self.name + ' / ' + (
                        self.payment_instrument_id.name if self.payment_instrument_id else ''),
                    'company_id': self.company_id.id,
                    'oci_point_of_sale': self.oci_point_of_sale.id,
                    'payment_instrument_id': self.payment_instrument_id.id,
                })
        return res
