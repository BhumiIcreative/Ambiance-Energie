from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    ac_id = fields.Many2one('account.move', string="Invoice")
    payment_instrument_id = fields.Many2one(
        'sale_timeline.payment.instrument',
        string='Payment Instrument')
    oci_point_of_sale = fields.Many2one(
        'oci.point.of.sale',
        string='Point of sale')
