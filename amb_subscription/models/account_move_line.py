from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    commissioning_identification = fields.Char(string="Identification")
