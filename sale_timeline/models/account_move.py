# coding: utf-8

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_timeline_ids = fields.One2many('payment.timeline', 'move_id', string=_('Payment timeline'))
    is_timeline = fields.Boolean(_('Is Timeline ?'), compute='_compute_is_timeline', store=True, default=False)
    payment_instrument_id = fields.Many2one('sale_timeline.payment.instrument', string=_('Payment method'))
    amount_missing_from_timeline = fields.Monetary(string=_("Amount missing from payment timeline"),
                                                   compute="_compute_amount_missing_from_timeline")
    advance = fields.Monetary('Advance', digits=(14, 10))
    advance_payment_ids = fields.One2many('account.payment', 'ac_id', string="advance payments")

    @api.depends('invoice_payment_term_id')
    def _compute_is_timeline(self):
        for account_id in self:
            account_id.is_timeline = account_id.invoice_payment_term_id.name == "Echéancier de paiement"

    # @api.depends('amount_total', 'payment_timeline_ids')
    # def _compute_amount_missing_from_timeline(self):
    #     print('\n\n\n_compute_amount_missing_from_timeline', self)
    #     for move in self:
    #         if move.edf_prime:
    #             move.amount_missing_from_timeline = move.amount_total - move.edf_prime
    #         else:
    #             move.amount_missing_from_timeline = move.amount_total
    #         for payment_timeline in move.payment_timeline_ids:
    #             move.amount_missing_from_timeline -= payment_timeline.amount
