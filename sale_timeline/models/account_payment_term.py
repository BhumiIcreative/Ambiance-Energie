# coding: utf-8

from odoo import models, fields, _


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    move_id = fields.Many2one('account.move', string=_('Invoice'))
