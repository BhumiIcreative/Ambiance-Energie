# coding: utf-8

from odoo import models, _
from odoo.fields import *


class ConfirmationWizard(models.TransientModel):
    _name = 'confirmation.wizard'
    _description = _('Confirmation wizard')
    _inherit = 'script.wizard'

    cancel_method = Char(_('Cancel method'), readonly=True)
    cancel_string = Char(_('Cancel string'), default=_('Cancel'), required=True, readonly=True)
    confirm_method = Char(_('Confirmation method'), required=True, readonly=True)
    confirm_string = Char(_('Confirmation string'), default=_('Confirm'), required=True, readonly=True)
    description = Text(_('Description'), default=_('Confirm action ?'), required=True, readonly=True)
    global_run = Boolean(_('Run method on every records at once'), default=True, readonly=True)
    name = Char(_('Name'), default=_('Confirmation'), required=True, readonly=True)
    res_model = Char(_('Model to apply method'), required=True, readonly=True)
    res_domain = Char(_('Domain to apply method'), required=True, readonly=True)

    def _run_method(self, method_name):
        self.ensure_one()
        ResModel = self.env[self.res_model]
        domain = eval(self.res_domain)
        record_ids = ResModel.search(domain)
        if self.global_run:
            global_method = getattr(record_ids, method_name)
            return global_method()

        for record_id in record_ids:
            method = getattr(record_id, method_name)
            method()
        return True

    def confirm(self):
        return self._run_method(self.confirm_method)

    def cancel(self):
        if not self.cancel_method:
            return True
        return self._run_method(self.cancel_method)

    def create_and_open(self, vals, **kwargs):
        return super().create_and_open(vals, name=kwargs.get('name') or self.name, **kwargs)
