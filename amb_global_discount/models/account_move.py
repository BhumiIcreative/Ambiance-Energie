# coding: utf-8

from odoo import api, fields, models, _
import logging
log = logging.getLogger(__name__).info


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'abstract.global.discount']


    def action_post(self):
        for sale_id in self:
            sale_id.global_discount_locked = True
        return super().action_post()

    def button_cancel(self):
        for sale_id in self:
            sale_id.global_discount_locked = False
        return super().button_cancel()

