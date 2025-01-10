# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _, fields


class ConfirmationWizard(models.TransientModel):
    _name = "confirmation.wizard"
    _description = _("Confirmation wizard")
    _inherit = "script.wizard"

    cancel_method = fields.Char(string=_("Cancel method"), readonly=True)
    cancel_string = fields.Char(
        string=_("Cancel string"), default=_("Cancel"), required=True, readonly=True
    )
    confirm_method = fields.Char(
        string=_("Confirmation method"), required=True, readonly=True
    )
    confirm_string = fields.Char(
        string=_("Confirmation string"),
        default=_("Confirm"),
        required=True,
        readonly=True,
    )
    description = fields.Text(
        string=_("Description"),
        default=_("Confirm action ?"),
        required=True,
        readonly=True,
    )
    global_run = fields.Boolean(
        string=_("Run method on every records at once"), default=True, readonly=True
    )
    name = fields.Char(
        string=_("Name"), default=_("Confirmation"), required=True, readonly=True
    )
    res_model = fields.Char(
        string=_("Model to apply method"), required=True, readonly=True
    )
    res_domain = fields.Char(
        string=_("Domain to apply method"), required=True, readonly=True
    )

    def _run_method(self, method_name):
        """Execute a specified method on records that match a given domain"""
        self.ensure_one()
        res_obj = self.env[self.res_model]
        domain = eval(self.res_domain)
        record_ids = res_obj.search(domain)
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
        return super().create_and_open(
            vals, name=kwargs.get("name") or self.name, **kwargs
        )
