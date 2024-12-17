# coding: utf-8

from odoo import fields, models

import logging
log = logging.getLogger().info


class EanWizard(models.TransientModel):
    _name = 'script.ean.8'
    _inherit = 'script.ean'
    _description = 'script.ean.8'

    def get_computed_key(self, ean_base):
        k = super().get_computed_key(ean_base)
        if len(ean_base) != 7:
            return k
        key = 0
        weight = [3, 1] * 4
        for c, i in zip(ean_base, range(len(ean_base))):
            key += int(c) * weight[i]
        key = (10 - (key % 10)) % 10
        return key
