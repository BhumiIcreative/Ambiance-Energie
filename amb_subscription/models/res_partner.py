from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    customer_history = fields.Text(string="Customer History")
