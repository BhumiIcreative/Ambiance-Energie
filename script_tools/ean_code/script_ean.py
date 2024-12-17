# coding: utf-8

from odoo import api, fields, models, _

import logging
log = logging.getLogger().info

def parse_ean_base(code):
    valid_char = '0123456789'
    res = ''
    for c in code:
        if c in valid_char:
            res += c
    return res


class EanWizard(models.TransientModel):
    _name = 'script.ean'
    _inherit = 'script.wizard'
    _description = 'EAN base calculator'

    current_code = fields.Char('Current code')
    computed_key = fields.Integer('Computed key', compute='_cpt_final_code', store=True, readonly=True)
    final_code = fields.Char('Final code', compute='_cpt_final_code', store=True, readonly=True)

    @api.depends('current_code')
    def _cpt_final_code(self):
        for ean_id in self:
            ean_base = parse_ean_base(ean_id.current_code)
            ean_id.computed_key = ean_id.get_computed_key(ean_base)
            ean_id.final_code = ''
            if ean_id.computed_key != -1:
                ean_id.final_code = '%s%s' % (ean_base, ean_id.computed_key)

    def button_compute_key(self):
        self._cpt_final_code()
        return self.open_wizard()

    def get_computed_key(self, ean_base):
        self.ensure_one()
        return -1
