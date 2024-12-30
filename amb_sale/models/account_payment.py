from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    sale_id = fields.Many2one('sale.order', string="Sale Order")
