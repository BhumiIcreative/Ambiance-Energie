# coding: utf-8

from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.fields import *

import logging
log = logging.getLogger(__name__).info


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    move_id = Many2one('account.move', string=_('Invoice'))
