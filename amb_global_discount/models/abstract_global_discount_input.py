# coding: utf-8

from odoo import models, fields
from odoo.exceptions import UserError


class AbstractGlobalDiscount(models.AbstractModel):
    _name = 'abstract.global.discount'

    global_discount = fields.Float(string='Remise Globale %', readonly=True)
    global_discount_locked = fields.Boolean('Remise Globale verrouillée', readonly=True, copy=False)

    def action_global_discount(self):
        if self.global_discount_locked:
            raise UserError("A cette étape il n'est plus possible de modifier la remise globale ici.")
        return self.env['wizard.global.discount'].create_and_open({
            'global_discount': self.global_discount,
            'res_model': self._name,
            'res_id': self.id,
        }, name='Remise Globale')
