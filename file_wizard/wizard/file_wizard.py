# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, _

import logging

_logger = logging.getLogger(__name__)
log = _logger.info


class FileWizard(models.TransientModel):
    _name = "file_wizard"
    _description = _("File wizard")

    file_content = fields.Binary(_("File"), required=True)
    file_name = fields.Char(_("File name"), required=True)
    name = fields.Char(_("Name"))

    def open_wizard(self):
        """Opens a form view for the file wizard to allow file download"""
        self.ensure_one()
        return {
            "name": self.name or _("Download file"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "file_wizard",
            "res_id": self.id,
            "view_id": self.env.ref("file_wizard.file_wizard_form").id,
            "target": "new",
            "flags": {"initial_mode": "view"},
        }
