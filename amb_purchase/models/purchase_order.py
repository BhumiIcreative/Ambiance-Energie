# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import datetime
from math import *

import logging
log = logging.getLogger('__name__').info


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    oci_point_of_sale = fields.Many2one('x_point_de_vente', string=_('Point of sale'))
