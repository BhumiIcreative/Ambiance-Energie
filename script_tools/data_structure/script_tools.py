# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models

from odoo.addons.script_tools.tools.group import groupby


class ScriptTools(models.TransientModel):
    _inherit = "script.tools"

    def groupby(self, recordset, keys):
        """Groups a recordset by the specified keys."""
        return groupby(recordset, keys)
