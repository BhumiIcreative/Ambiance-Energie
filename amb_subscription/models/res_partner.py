from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class ResPartnery(models.Model):
    _inherit = 'res.partner'

    customer_history = fields.Text(string=_('Customer history'))
