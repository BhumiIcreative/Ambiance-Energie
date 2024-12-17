from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    mandatory_particular_invoice = fields.Text(string=_('Custom comments on invoice'))
    mandatory_particular_saleorder = fields.Text(string=_('Custom comments on sale'))
    edf_prime = fields.Monetary(string=_('EDF Prime'))

    second_partner_id = fields.Many2one('res.partner', string=_('Second contact'))
