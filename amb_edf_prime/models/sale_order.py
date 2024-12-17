# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import datetime
from math import *

import logging
log = logging.getLogger(__name__).info


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'abstract.edf.prime.input']

    @api.depends('amount_total', 'type_order', 'edf_prime')
    def _compute_amount_left_to_pay(self):
        super()._compute_amount_left_to_pay()
        for sale_id in self:
            sale_id.amount_left_to_pay = sale_id.amount_left_to_pay
            if sale_id.type_order == 'sto':
                sale_id.amount_left_to_pay -= sale_id.edf_prime

    @api.depends('amount_total', 'payment_timeline_ids', 'advance', 'edf_prime')
    def _compute_amount_missing_from_timeline(self):
        super()._compute_amount_missing_from_timeline()
        for sale in self:
            if sale.type_order == 'sto':
                sale.amount_missing_from_timeline -= sale.edf_prime

    def action_confirm(self):
        for sale_id in self:
            sale_id.edf_prime_locked = True
        return super().action_confirm()

    def action_cancel(self):
        for sale_id in self:
            sale_id.edf_prime_locked = False
        return super().action_cancel()

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        if self.type_order == 'sto':
            res['edf_prime'] = self.edf_prime
        return res

