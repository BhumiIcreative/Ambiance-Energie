# coding: utf-8

from odoo import api, fields, models, _

import logging
log = logging.getLogger(__name__).info


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    min_price = fields.Monetary(_('Minimum Price'))
