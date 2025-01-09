from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    oci_point_of_sale = fields.Many2one('oci.point.of.sale', string='Point of sale')
    payment_instrument_id = fields.Many2one('sale_timeline.payment.instrument', string='Payment method')

    def _prepare_invoice(self):
        """ Prepare the invoice with additional custom fields """
        res = super()._prepare_invoice()
        if self.oci_point_of_sale:
            res['oci_point_of_sale'] = self.oci_point_of_sale.id
        if self.payment_instrument_id:
            res['payment_instrument_id'] = self.payment_instrument_id.id
        return res

    def _create_recurring_invoice(self):
        """ Create a recurring invoice and generate rest payments for each invoice """
        res = super()._create_recurring_invoice()
        for invoice in res:
            invoice._generate_invoice_rest_payments()
