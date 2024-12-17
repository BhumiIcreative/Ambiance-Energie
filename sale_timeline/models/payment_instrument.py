# coding: utf-8

from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.fields import *

import logging
log = logging.getLogger(__name__).info


class PaymentInstrument(models.Model):
    _name = 'sale_timeline.payment.instrument'
    _description = _('Payment instrument')

    name = Char(_('Name'))
