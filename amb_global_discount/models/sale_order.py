# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import datetime
from math import *

import logging
log = logging.getLogger(__name__).info


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'abstract.global.discount']

    def action_confirm(self):
        for sale_id in self:
            sale_id.global_discount_locked = True
        return super().action_confirm()

    def action_cancel(self):
        for sale_id in self:
            sale_id.global_discount_locked = False
        return super().action_cancel()

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res['global_discount'] = self.global_discount
        return res

