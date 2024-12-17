# coding: utf-8

from odoo import models, api, _
from odoo.fields import *

import os
import pysftp


class ScriptTools(models.TransientModel):
    _inherit = 'script.tools'

    def sftp_send_file_content(self, url, login, password, content, coding='utf-8', port=22, dest_path='', fname=''):
        fpath = self.content_to_tmp_file(content, coding=coding)
        return self.sftp_send_file(url, login, password, fpath, port=port, dest_path=dest_path, fname=fname)

    def sftp_get_connection(self, url, login, password, port=22):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        return pysftp.Connection(host=url, username=login, password=password, port=port, cnopts=cnopts)

    def sftp_send_file(self, url, login, password, local_path, port=22, dest_path='', fname=''):
        with self.sftp_get_connection(url, login, password, port=port) as sftp:
            with sftp.cd(dest_path or sftp.pwd):
                sftp.put(local_path, preserve_mtime=True)
            if fname:
                local_fname = os.path.split(local_path)[1]
                dest_fpath = os.path.join(dest_path, local_fname)
                final_dest_fpath = os.path.join(dest_path, fname)
                sftp.rename(dest_fpath, final_dest_fpath)
