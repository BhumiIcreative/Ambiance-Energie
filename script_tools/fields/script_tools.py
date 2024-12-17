# coding: utf-8

from odoo import models, api, _


class ScriptTools(models.TransientModel):
    _inherit = 'script.tools'

    def record_to_reference(self, record_id):
        """
            Convert a record to a reference string
            param:
                record_id: Model object instance (eg: account.move(4))
            return:
                string: reference string (eg: 'account.move,4')
        """
        if type(record_id) is not str:
            record_id = '%s,%s' % (record_id._name, record_id.id)
        return record_id

    def reference_to_record(self, reference):
        """
            Convert reference to record
            param:
                string: reference string (eg: 'account.move,4')
            return:
                record_id: Model object instance (eg: account.move(4))
        """
        if type(reference) is str:
            model_name, record_id = reference.split(',')
        return self.env[model_name].browse(int(record_id))

    def get_all_reference(self):
        model_ids = self.env['ir.model'].search([])
        res = []
        for model_id in model_ids:
            res.append((model_id.model, model_id.name))
        return res
