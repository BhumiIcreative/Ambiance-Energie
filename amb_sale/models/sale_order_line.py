from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Increase discount precision to avoid rounding when working with fixed discount
    discount = fields.Float(digits=(14,10))
    discount_fixed = fields.Float(string="Discount (Fixed)", digits="Product Price", default=0.00, help="Fixed amount discount.")

    @api.onchange('discount')
    def _onchange_discount(self):
        self.discount_fixed = self.product_uom_qty * self.price_unit * self.discount / 100

    @api.onchange('price_subtotal')
    def _onchange_price_unit(self):
        if self.price_subtotal < self.product_id.min_price:
            # 'message': (_('Vérifiez le prix sur la ligne %s, prix minimum %s') % (self.product_id.name,self.product_id.min_price)),
            return {
                'warning':
                    {
                        'title': 'Warning',
                        'message': ('Check the price on line %s, minimum price %s' % (self.product_id.name,self.product_id.min_price)),
                    },
            }

    @api.onchange('discount_fixed', 'product_uom_qty', 'price_unit')
    def _onchange_discount_fixed(self):
        if self.price_unit == 0.00 or self.product_uom_qty == 0.00:
            self.discount = 0.00
        else:
            self.discount = self.discount_fixed / (self.product_uom_qty * self.price_unit) * 100

    def _prepare_invoice_line(self):
        res = super()._prepare_invoice_line()
        print("\n\n\n ######### res: ", res)
        print("\n\n\n ######### discount_fixed: ", res['discount_fixed'])
        res['discount_fixed'] = self.discount_fixed
        return res