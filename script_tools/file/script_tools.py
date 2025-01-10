# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _, fields

import base64


class ScriptTools(models.TransientModel):
    _inherit = "script.tools"

    file = fields.Binary(_("File"))
    fname = fields.Char(_("File name"))

    def download_text(self, text, fname, name=""):
        """Encodes text to base64 and downloads it as a file."""
        return self.download_b64(self.encode_base64(text), fname, name=name)

    def download_b64(self, b64, fname, name=""):
        """Creates a file wizard to download a base64-encoded file."""
        file_wizard = self.env["file_wizard"].create(
            {
                "name": name or fname,
                "file_content": b64,
                "file_name": fname,
            }
        )
        return file_wizard.open_wizard()

    def encode_base64(self, string, coding="utf-8"):
        """Encodes a string to base64 format."""
        try:
            return base64.b64encode(string)
        except Exception as e:
            return base64.b64encode(string.encode(coding))
