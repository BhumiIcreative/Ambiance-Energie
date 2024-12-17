# coding: utf-8

from odoo import models, api, _
from odoo.fields import *

from odoo.addons.script_tools.tools.group import groupby


class ScriptTools(models.TransientModel):
    _inherit = 'script.tools'

    def groupby(self, recordset, keys):
        return groupby(recordset, keys)

    def replace_all(self, string, replacements):
        """
            input:
                string: "Some\ttext to ;eplace thin@gs"
                replacements: [
                    ('\t', ' '),
                    (';', 'r'),
                    ('@', ''),
                ]
            output: "Some text to replace things"
        """
        for replacement in replacements:
            string = string.replace(replacement[0], replacement[1])
        return string

    def remove_all(self, string, to_remove):
        """
            string: str to remove things of
            to_remove: list of char to remove

            input: "Remo!ve? stupi4d thin5g"
            output: "Remove stupid thing"
        """
        return self.replace_all(string, [
            (x, '') for x in to_remove
        ])
