from odoo import fields, models


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    move_id = fields.Many2one('account.move', string='Invoice')
