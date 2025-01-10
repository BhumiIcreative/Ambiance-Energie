# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _


class ScriptWizard(models.TransientModel):
    _name = "script.wizard"
    _description = _("Script wizard")

    def open_wizard(self, name="", target="new", context=dict()):
        # Opens the script tools wizard with specified parameters.
        return self.env["script.tools"].open_wizard(
            self,
            name=name or self._description,
            target=target,
            context=context,
        )

    def create_and_open(self, vals, name="", target="new", context=dict()):
        """Creates a new record and opens its associated script tools wizard."""
        return self.create(vals).open_wizard(
            name=name or self._description, target=target, context=context
        )
