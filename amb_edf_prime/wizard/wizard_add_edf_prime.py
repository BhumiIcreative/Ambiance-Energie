from odoo import models, fields
from odoo.exceptions import UserError


class WizardAddEdfPrime(models.TransientModel):
    _name = 'wizard.add.edf_prime'
    _inherit = 'script.wizard'

    amount = fields.Float('Amount')
    res_model = fields.Char('Model')
    res_id = fields.Integer('Res id')

    def confirm(self):
        record_id = self.env[self.res_model].browse(self.res_id).with_context(force_bypass_timeline=True)
        record_id.edf_prime = self.amount
        return True
