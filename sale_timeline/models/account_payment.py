from odoo import models, fields, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_instrument_id = fields.Many2one('sale_timeline.payment.instrument')
    oci_point_of_sale = fields.Many2one('x_point_de_vente', string=_('Point of sale'))
