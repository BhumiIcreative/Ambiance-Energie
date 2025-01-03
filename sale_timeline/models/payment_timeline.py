from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class PaymentTimeLine(models.Model):
    """
    creating payment terms dynamically based on specific timelines
    """
    _name = 'payment.timeline'
    _description = 'Payment timeline'
    _order = 'date'

    def _get_default_currency(self):
        return self.env['account.move']._compute_currency_id()

    date = fields.Date(string='Date', required=True,
                       default=fields.Date.today())
    amount = fields.Monetary(string='Amount', required=True)
    currency_id = fields.Many2one('res.currency', store=True, readonly=True,
                                  required=True, string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    move_id = fields.Many2one('account.move', string='Move')
    sale_id = fields.Many2one('sale.order', string='Sale')
    payment_instrument_id = fields.Many2one('sale_timeline.payment.instrument',
                                            string='Payment method')
    advance = fields.Boolean(string='Deposit', default=False, readonly=True)

    def compute_payment_term_id(self):
        """
            - Dynamically computes and/or updates the payment term for a
            related account.move (e.g., an invoice).
            - Creates or updates a record in the account.payment.term model
            for tracking payment terms related to the invoice.
            - Links the payment term with payment.term.line entries,
            representing each payment line in the term.
        """
        if not self:
            return
        move_id = self[0].move_id

        payment_term_id = move_id.invoice_payment_term_id
        payment_term_name = move_id.name
        PaymentTerm = self.env['account.payment.term']
        vals = {
            'name': '%s' % (payment_term_id.name),
            'company_id': payment_term_id.company_id.id,
            'note': payment_term_id.note,
            'move_id': move_id.id,
        }
        if not payment_term_id.move_id:
            # We aren't on a copy of timeline payment term
            payment_term_id = PaymentTerm.create(vals)
            move_id.invoice_payment_term_id = payment_term_id
        else:
            payment_term_id.write(vals)

    def generate_payment_term_line(self, invoice_date, payment_term_id):
        # Unvisited Method
        """

        :param invoice_date: Current date if not invoice date.
        :param payment_term_id: account.payment.term
        :return:
        """
        PaymentTermLine = self.env['account.payment.term.line']
        for timeline_id in self:
            if timeline_id.date <= invoice_date:
                # Cash is due right now
                days = 0
            else:
                delta = timeline_id.date - invoice_date
                days = delta.days
            PaymentTermLine |= PaymentTermLine.create({
                'value': 'percent',
                'value_amount': 100,
                'delay_type': 'days_after',
                'nb_days': days,
                'payment_id': payment_term_id.id,
            })
        PaymentTermLine[-1].write({
            'value_amount': 100,
            'value': 'percent',
        })
        return PaymentTermLine

    def validate_amount(self, amount_target):
        amount = sum(self.mapped('amount'))
        currency_id = self.currency_id or self.env.company.currency_id
        if float_compare(amount, amount_target, precision_rounding=currency_id.rounding) or not self:
            raise UserError("Payments timeline sum have to be %s € (current is %s €)" % (
                amount_target, amount))

    def write(self, values):
        """
            Overrides the write method to dynamically recompute payment terms
            whenever payment timeline entries are updated.
        """
        res = super().write(values)
        if self.move_id:
            self.move_id.payment_timeline_ids.compute_payment_term_id()
        return res
