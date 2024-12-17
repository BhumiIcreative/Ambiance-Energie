# coding: utf-8

from odoo import models, api, _
from odoo.fields import *


class ScriptTools(models.TransientModel):
    _inherit = 'script.tools'

    def create_mail_wizard(self, template_id, active_id, composition_mode='comment', context=dict()):
        wizard_id = self.env['mail.compose.message'].with_context(
            default_use_template=bool(template_id),
            default_template_id=template_id and template_id.id or False,
            default_model=active_id._name,
            active_model=active_id._name,
            active_ids=active_id.ids,
            active_id=active_id.ids[0],
            **context
        ).create({
            'composition_mode': composition_mode,
        })
        wizard_id.onchange_template_id_wrapper()
        return wizard_id

    def open_mail_wizard(self, *args, **kwargs):
        return self.open_wizard(self.create_mail_wizard(*args, **kwargs))
