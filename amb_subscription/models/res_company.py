from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    mandatory_particular_invoice = fields.Text(string="Custom Comments On Invoice")
    mandatory_particular_saleorder = fields.Text(string="Custom Comments On Sale")
    edf_prime = fields.Monetary(string="EDF Prime")
    second_partner_id = fields.Many2one("res.partner", string="Second Contact")
