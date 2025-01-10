# coding: utf-8

from odoo import models
from odoo.addons.script_tools.tools.sirius_xml import dict_to_xml


class ScriptTools(models.TransientModel):
    _inherit = "script.tools"

    def dict_to_xml(self, datas, root="root"):
        return dict_to_xml(datas, root=root)
