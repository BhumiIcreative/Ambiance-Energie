from odoo import models, fields


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    move_id = fields.Many2one('account.move', string='Invoice')
