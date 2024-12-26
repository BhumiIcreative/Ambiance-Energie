# coding: utf-8

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_timeline_ids = fields.One2many('payment.timeline', 'sale_id', string=_('Payment timeline'))
    is_timeline = fields.Boolean(_('Is Timeline ?'), compute="_compute_is_timeline", store=True, default=False)
    payment_instrument_id = fields.Many2one('sale_timeline.payment.instrument', string=_('Payment method'))
    amount_missing_from_timeline = fields.Monetary(string=_("Amount out of payment timeline"),compute="_compute_amount_missing_from_timeline")

    @api.depends('payment_term_id')
    def _compute_is_timeline(self):
        for order in self:
            order.is_timeline = order.payment_term_id == self.env.ref('sale_timeline.timeline_payment')

    @api.depends('amount_total', 'payment_timeline_ids')
    def _compute_amount_missing_from_timeline(self):
        print('\n\n\nself_compute_amount_missing_from_timeline',self)
        for order in self:
            order.amount_missing_from_timeline = order.amount_total
            for payment_timeline in order.payment_timeline_ids:
                order.amount_missing_from_timeline -= payment_timeline.amount

    def _prepare_invoice(self):
        print('\n\n\nself _prepare_invoice',self)
        vals = super()._prepare_invoice()
        vals['payment_instrument_id'] = self.payment_instrument_id
        print('\n\n\nvals',vals)
        if self.payment_timeline_ids:
            vals['payment_timeline_ids'] = [(6, 0, self.payment_timeline_ids.ids)]
        return vals

