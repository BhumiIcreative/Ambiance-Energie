from odoo import models, fields


class WizardAddEdfPrime(models.TransientModel):
    _name = "wizard.add.edf_prime"
    _description = "Edf Prime Wizard"
    _inherit = "script.wizard"

    amount = fields.Float("Amount")
    res_model = fields.Char("Model")
    res_id = fields.Integer("Res id")

    def confirm(self):
        """
        Confirms and applies the EDF Prime amount to the associated record.

        This method retrieves the record specified by `res_model` and `res_id`,
        then updates its `edf_prime` field with the value provided in `amount`.
        The operation bypasses the timeline validation by using a specific context.

        Returns:
            bool: True if the operation is successful.
        """
        record_id = (
            self.env[self.res_model]
            .browse(self.res_id)
            .with_context(force_bypass_timeline=True)
        )
        record_id.edf_prime = self.amount
        return True
