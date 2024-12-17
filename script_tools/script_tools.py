# coding: utf-8

from odoo import models, api, _
from odoo.fields import *

import datetime

import logging
log = logging.getLogger().info


CODE_PLACEHOLDER = """
# The model script.tools provide some generic function so we can easily make script.
# Available vars:
#   - self: used like any other self in odoo function
#   - Script: return a void recordset of script.tools (so you can use it's function)
#   - log: Will display output in odoo's log
#   - datetime: got the datetime package, so you can use datetime.datetime.now() or other


"""


class ScriptTools(models.TransientModel):
    _name = 'script.tools'
    _description = _('Script Tools')

    code = Text(_('Code'), default=CODE_PLACEHOLDER)

    def exec_code(self):
        exec_env = {
            'self': self,
            'Script': self.env['script.tools'],
            'log': log,
            'datetime': datetime,
        }
        exec(self.code, exec_env)

    def log(self, o):
        log(o)
