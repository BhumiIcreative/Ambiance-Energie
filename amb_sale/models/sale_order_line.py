from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount = fields.Float(string="Discount")
    discount_fixed = fields.Float(
        string="Discount (Fixed)", default=0.00,
        help="Fixed amount discount.")

    @api.onchange('discount')
    def _onchange_discount(self):
        """
            Automatically calculates a fixed discount amount based on the
            percentage discount and updates it whenever the percentage
            discount changes.
        """
        self.discount_fixed = self.product_uom_qty * self.price_unit * self.discount / 100

    @api.onchange('price_subtotal')
    def _onchange_price_unit(self):
        """
            Warns the user if the total price is lower than the allowed
            minimum price for the product.
        """
        if self.price_subtotal < self.product_id.min_price:
            return {
                'warning':
                    {
                        'title': _('Warning'),
                        'message': _('Check the price on the line %s, minimum price %s' % (
                        self.product_id.name, self.product_id.min_price)),
                    },
            }

    @api.onchange('discount_fixed', 'product_uom_qty', 'price_unit')
    def _onchange_discount_fixed(self):
        """
            Automatically adjusts the percentage discount when the fixed
            discount, quantity, or price changes.
        """
        self.discount = 0.00 if self.price_unit == 0.00 or self.product_uom_qty == 0.00 else self.discount_fixed / (
                    self.product_uom_qty * self.price_unit) * 100

    def _prepare_invoice_line(self):
        """
            Adds the fixed discount to the invoice so it reflects correctly
            during billing.
        """
        res = super()._prepare_invoice_line()
        res['discount_fixed'] = self.discount_fixed
        return res
