# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
log = logging.getLogger().info

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    advance_payment_method = fields.Selection(default='delivered', readonly=False)
