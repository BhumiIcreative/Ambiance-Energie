# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class ScriptTools(models.TransientModel):
    _inherit = "script.tools"

    def record_to_reference(self, record_id):
        """
        Convert a record to a reference string
        param:
            record_id: Model object instance (eg: account.move(4))
        return:
            string: reference string (eg: 'account.move,4')
        """
        if type(record_id) is not str:
            record_id = "%s,%s" % (record_id._name, record_id.id)
        return record_id
