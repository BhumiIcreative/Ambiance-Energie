# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    color = fields.Integer(string="Color", copy=False)
