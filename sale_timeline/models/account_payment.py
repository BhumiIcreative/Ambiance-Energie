from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    ac_id = fields.Many2one('account.move', string="Invoice")
    # Field commented as model is commented.
    # payment_instrument_id = fields.Many2one(
    #     'sale_timeline.payment.instrument',
    #     string='Payment Instrument')
    oci_point_of_sale = fields.Many2one(
        'x_point_de_vente',
        string='Point of sale')
