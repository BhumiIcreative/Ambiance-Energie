from odoo import api, fields, models



class PaymentInstrument(models.Model):
    _name = "sale_timeline.payment.instrument"
    _description = 'Payment instrument'

    name = fields.Char(string="Name")
