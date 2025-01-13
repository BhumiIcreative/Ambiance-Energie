from odoo import models, fields, api, _


class SaleOrder(models.Model): 
    _inherit = 'sale.order'

    payment_timeline_ids = fields.One2many(
        'payment.timeline', 'sale_id', string='Payment Timeline')
    is_timeline = fields.Boolean('Is Timeline ?',
            compute="_compute_is_timeline", store=True, default=False)
    payment_instrument_id = fields.Many2one(
        'sale_timeline.payment.instrument', 'Payment Method')
    amount_missing_from_timeline = fields.Monetary(
        "Amount Out of Payment Timeline", compute="_compute_amount_missing_from_timeline")
    advance_payment_instrument_id = fields.Many2one(
        'sale_timeline.payment.instrument',
        string='Advance Payment Method',
        copy=False)

    @api.depends('payment_term_id')
    def _compute_is_timeline(self):
        for order in self:
            order.is_timeline = order.payment_term_id == self.env.ref(
                "sale_timeline.timeline_payment")

    @api.depends('amount_total', 'payment_timeline_ids')
    def _compute_amount_missing_from_timeline(self):
        for order in self:
            order.amount_missing_from_timeline = order.amount_total
            for payment_timeline in order.payment_timeline_ids:
                order.amount_missing_from_timeline -= payment_timeline.amount

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        vals['payment_instrument_id'] = self.payment_instrument_id.id
        if self.payment_timeline_ids:
            vals['payment_timeline_ids'] = [
                (6, 0, self.payment_timeline_ids.ids)]
        return vals

    def prepare_custom_account_payment_vals(self):
        res = super().prepare_custom_account_payment_vals()
        res['payment_instrument_id'] = self.advance_payment_instrument_id.id
        return res

    def write(self, values):
        res = super().write(values)
        if self.state != 'draft' and self.payment_term_id == self.env.ref('sale_timeline.timeline_payment'):
            self.payment_timeline_ids.validate_amount(self.amount_left_to_pay)
            if self.type_order == 'sto':
                self.payment_timeline_ids.validate_amount(self.amount_left_to_pay - self.edf_prime)
        return res
