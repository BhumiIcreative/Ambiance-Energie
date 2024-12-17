# coding: utf-8

from odoo import models, api, _


class ScriptWizard(models.TransientModel):
    _name = 'script.wizard'
    _description = _('Script wizard')

    def open_wizard(self, name='', target='new', context=dict()):
        return self.env['script.tools'].open_wizard(self, name=name or self._description, target=target, context=context)

    def create_and_open(self, vals, name='', target='new', context=dict()):
        return self.create(vals).open_wizard(name=name or self._description, target=target, context=context)

    def get_wizard_from_dict(self, res):
        WizardModel = self.env[res['res_model']]
        if 'res_id' in res:
            return WizardModel.browse([res['res_id']])
        return WizardModel.with_context(res.get('context', dict())).create({})
