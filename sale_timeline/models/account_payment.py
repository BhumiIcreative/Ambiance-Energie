# coding: utf-8

from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    ac_id = fields.Many2one('account.move')
