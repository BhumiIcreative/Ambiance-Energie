# coding: utf-8

from odoo import models, api, _
from odoo.fields import *


class ScriptTools(models.TransientModel):
    _inherit = 'script.tools'

    def open_record(self, record_id, name='', target='current', context=dict()):
        if len(record_id) != 1:
            return self.open_records(record_id, name=name, target=target, context=context)
        return {
            'type': 'ir.actions.act_window',
            'name': name or record_id._name,
            'res_model': record_id._name,
            'views': [(False, 'form')],
            'res_id': record_id.id,
            'target': target,
            'context': context,
        }

    def open_records(self, record_ids, name='', target='current', context=dict(), views=['tree', 'form'], domain=[], force_multi=False):
        if len(record_ids) == 1 and not force_multi:
            return self.open_record(record_ids, name=name, target=target, context=context)
        return {
            'type': 'ir.actions.act_window',
            'name': name or record_ids._name,
            'res_model': record_ids._name,
            'views': [(False, x) for x in views],
            'domain': domain or [('id', 'in', record_ids.ids)],
            'target': target,
            'context': context,
        }

    def open_wizard(self, wizard_id, name='', target='new', context=dict()):
        return self.open_record(wizard_id, name=name, target=target, context=context)
