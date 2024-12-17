# coding: utf-8

from odoo import models, fields
from odoo.exceptions import UserError


class AbstractEdfPrimeInput(models.AbstractModel):
    _name = 'abstract.edf.prime.input'

    edf_prime = fields.Monetary(string='Prime EDF', readonly=True)
    edf_prime_locked = fields.Boolean('Prime EDF verrouillée', readonly=True, copy=False)

    currency_id = fields.Many2one('res.currency')

    def action_add_edf_prime(self):
        if self.edf_prime_locked:
            raise UserError("A cette étape il n'est plus possible de modifier la prime EDF ici.")
        return self.env['wizard.add.edf_prime'].create_and_open({
            'amount': self.edf_prime,
            'res_model': self._name,
            'res_id': self.id,
        }, name='Prime EDF')
