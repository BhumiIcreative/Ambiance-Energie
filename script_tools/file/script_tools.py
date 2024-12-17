# coding: utf-8

from odoo import models, api, _
from odoo.exceptions import UserError
from odoo.fields import *

import base64
import tempfile


class ScriptTools(models.TransientModel):
    _inherit = 'script.tools'

    file = Binary(_('File'))
    fname = Char(_('File name'))

    def download_text(self, text, fname, name=''):
        return self.download_b64(self.encode_base64(text), fname, name=name)

    def download_b64(self, b64, fname, name=''):
        file_wizard = self.env['file_wizard'].create({
            'name': name or fname,
            'file_content': b64,
            'file_name': fname,
        })
        return file_wizard.open_wizard()

    def decode_base64(self, string):
        return base64.b64decode(string)

    def encode_base64(self, string, coding='utf-8'):
        try:
            return base64.b64encode(string)
        except:
            return base64.b64encode(string.encode(coding))

    def get_file_content(self, force_string=True):
        if not self.file:
            raise UserError(_('No file provided !'))

        base64_decoded = self.decode_base64(self.file)
        if force_string:
            return self.to_string(base64_decoded)
        return base64_decoded

    def content_to_tmp_file(self, content, coding='utf-8', suffix='', prefix='', text=False):
        fid, fname = tempfile.mkstemp(suffix=suffix, prefix=prefix, text=text)

        with open(fname, 'wb') as file:
            file.write(self.to_byte(content, coding=coding))
        return fname

    def to_byte(self, value, coding='utf-8'):
        if type(value) is str:
            return value.encode(coding)
        return self.to_byte(self.to_string(value))

    def to_string(self, value, coding='utf-8'):
        if type(value) is bytes:
            return value.decode(coding)
        return self.to_string(str(value).encode(coding))
