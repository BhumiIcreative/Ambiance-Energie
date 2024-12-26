from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

class PaymentTimeLine(models.Model):
    _name = 'payment.timeline'
    _description = 'Payment timeline'
    _order = 'date'

    @api.model
    def _get_default_currency(self):
        """Return the default currency for account moves"""
        journal = self.env["account.move"]._search_default_journal()
        return journal.currency_id or journal.company_id.currency_id

    amount = fields.Monetary(string='Amount', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today())
    currency_id = fields.Many2one('res.currency', store=True, readonly=True,
                           required=True, string='Currency',
                           default=_get_default_currency)
    move_id = fields.Many2one('account.move', string='Move')
    sale_id = fields.Many2one('sale.order', string='Sale')
    payment_instrument_id = fields.Many2one('sale_timeline.payment.instrument',
                                     string='Payment method')
    advance = fields.Boolean(string='Deposit', default=False, readonly=True)

    def compute_payment_term_id(self):
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

        payment_term_id.line_ids = [(6, 0,
            self.generate_payment_term_line(
                                        move_id.invoice_date or Date.today(),
                                        payment_term_id).ids)]

    def generate_payment_term_line(self, invoice_date, payment_term_id):
        PaymentTermLine = self.env['account.payment.term.line']
        for timeline_id in self:
            if timeline_id.date <= invoice_date:
                # Cash is due right now
                days = 0
            else:
                delta = timeline_id.date - invoice_date
                days = delta.days
            PaymentTermLine |= PaymentTermLine.create({
                'value': 'fixed',
                'value_amount': timeline_id.amount,
                'option': 'day_after_invoice_date',
                'days': days,
                'payment_id': payment_term_id.id,
            })
        PaymentTermLine[-1].write({
            'value_amount': 0,
            'value': 'balance',
        })
        return PaymentTermLine

    def validate_amount(self, amount_target):
        amount = sum(self.mapped('amount'))
        if float_compare(amount,amount_target, precision_rounding=self.currency_id.rounding) or not self:
            raise UserError(_("Payments timeline sum have to be %s € (current is %s €)") % (amount_target, amount))

    @api.model
    def create(self, vals):
        res = super().create(vals)
        return res


    def write(self, values):
        res = super().write(values)
        if self.move_id:
            self.move_id.payment_timeline_ids.compute_payment_term_id()
        return res