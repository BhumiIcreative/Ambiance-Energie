from odoo import models, fields
from odoo.exceptions import UserError


class AbstractEdfPrimeInput(models.AbstractModel):
    _name = "abstract.edf.prime.input"
    _description = "EDF Prime Input"

    edf_prime = fields.Monetary(string="Prime EDF", readonly=True)
    edf_prime_locked = fields.Boolean(
        "Prime EDF locked", readonly=True, copy=False
    )

    currency_id = fields.Many2one("res.currency")

    def action_add_edf_prime(self):
        """
        Triggers the process to add or modify the EDF Prime.

        This method ensures that the EDF Prime can only be modified if it
        is not locked. If the EDF Prime is locked, a UserError is raised
        to prevent further modifications. If the prime is not locked,
        the method creates and opens a wizard for adding or modifying
        the EDF Prime.

        Returns:
            dict: Action for opening the `wizard.add.edf_prime`.

        Raises:
            UserError: If the EDF Prime is locked and cannot be modified.
        """
        if self.edf_prime_locked:
            raise UserError(
                "At this stage it is no longer possible to "
                "modify the EDF bonus here."
            )
        return self.env["wizard.add.edf_prime"].create_and_open(
            {
                "amount": self.edf_prime,
                "res_model": self._name,
                "res_id": self.id,
            },
            name="Prime EDF",
        )
