# coding: utf-8

from odoo import models, api, _
from odoo.fields import *

import os
import ftplib

import logging
log = logging.getLogger().info


class ScriptTools(models.TransientModel):
    _inherit = 'script.tools'

    def ftp_send_file_content(self, url, login, password, content, coding='utf-8', port=21, dest_path='', fname=''):
        fpath = self.content_to_tmp_file(content, coding=coding)
        return self.ftp_send_file(url, login, password, fpath, port=port, dest_path=dest_path, fname=fname)

    def ftp_send_file(self, url, login, password, local_path, port=21, dest_path='', fname=''):
        ftp = ftplib.FTP()
        ftp.connect(url, port)
        ftp.login(login, password)
        ftp.cwd(dest_path or ftp.pwd())
        local_fname = os.path.split(local_path)[1]
        with open(local_path, 'rb') as file:
            ftp.storbinary('STOR %s' % (fname or local_fname), file)
        ftp.quit()
