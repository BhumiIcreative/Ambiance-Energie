from odoo import fields, models


class Subscription(models.Model):
    _inherit = "sale.order"

    oci_point_of_sale = fields.Many2one("x_point_de_vente", string="Point of sale")
    payment_instrument_id = fields.Many2one(
        "sale_timeline.payment.instrument", string="Payment method"
    )

    def _prepare_invoice(self):
        """Inherit prepare invoice method for add POS ID and payment instrument ID if available"""
        res = super()._prepare_invoice()
        if self.oci_point_of_sale:
            res["oci_point_of_sale"] = self.oci_point_of_sale.id
        if self.payment_instrument_id:
            res["payment_instrument_id"] = self.payment_instrument_id.id
        return res

    def _create_recurring_invoice(self, automatic=False):
        """Generate remaining payment records for each invoice"""
        res = super()._create_recurring_invoice(automatic=automatic)
        for invoice in res:
            invoice._generate_invoice_rest_payments()
