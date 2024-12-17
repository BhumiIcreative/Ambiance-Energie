# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import datetime

import logging
log = logging.getLogger(__name__).info


class Subscription(models.Model):
    _inherit = 'sale.order'

    oci_point_of_sale = fields.Many2one('x_point_de_vente', string=_('Point of sale'))
    payment_instrument_id = fields.Many2one('sale_timeline.payment.instrument', string=_('Payment method'))


    def _prepare_invoice_data(self):
        res = super()._prepare_invoice_data()
        if self.oci_point_of_sale :
            res['oci_point_of_sale'] = self.oci_point_of_sale.id
        if self.payment_instrument_id :
            res['payment_instrument_id'] = self.payment_instrument_id.id
        return res

    def _recurring_create_invoice(self, automatic=False):
        res = super()._recurring_create_invoice(automatic=automatic)
        for invoice in res :
            invoice._generate_invoice_rest_payments()