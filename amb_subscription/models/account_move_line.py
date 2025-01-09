from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    commissioning_identification = fields.Char(string="Identification")
