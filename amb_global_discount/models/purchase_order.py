# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import datetime
from math import *

import logging
log = logging.getLogger(__name__).info


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'abstract.global.discount']

    def button_confirm(self):
        for purchase_id in self:
            purchase_id.global_discount_locked = True
        return super().button_confirm()

    def button_cancel(self):
        for purchase_id in self:
            purchase_id.global_discount_locked = False
        return super().button_cancel()

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res['global_discount'] = self.global_discount
        return res

