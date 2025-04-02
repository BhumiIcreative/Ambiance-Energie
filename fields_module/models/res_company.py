from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    second_partner_id = fields.Many2one("res.partner", string="Second Contact")
