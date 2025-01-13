import datetime
from math import *

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


current_subscription = fields.Many2one(
    'subscription.wood.pellet',
    string='Current Subscription Wood Pellet',
    compute='_get_subscription',
    store=True)


@api.depends('type_order', 'partner_id')


def _get_subscription(self):
    """
        Finds the customer's current subscription for wood pellets, if any.
    """
    for sale_id in self:
        sale_id.current_subscription = self.env[
            'subscription.wood.pellet'].search([
            ('partner_id', '=', sale_id.partner_id.id),
            ('date_start', '<', datetime.datetime.now()),
            ('date_end', '>', datetime.datetime.now()),
        ])


def action_confirm(self):
    """
        Confirms the order, ensuring subscription rules and payment
        conditions are met.
    """
    if self.type_order == 'gran' and self.amount_left_to_pay > self.current_subscription.amount:
        raise UserError(
            _('You can\'t confirm the quotation, amount in subscription is not sufficient'))
    return self.counter_sale_confirm()


@api.onchange('type_order', 'partner_id')


def granule_product_proposal(self):
    """
        Proposes a granule product to the order if the order type is
        'granule'. This function automatically adds a granule product to
        the order if it's not already present. The granule product is
        based on the current subscription of the customer.
    """
    article_granule = self.env['product.product'].search([
        ('default_code', '=', 'GRANULE'),
    ], limit=1)
    # Check if the order type is 'gran' (granule) and if the granule
    # product is not already in the order
    if (article_granule and self.type_order == 'gran' and
            article_granule.id not in self.order_line.mapped('product_id').ids):
        sub = self.current_subscription
        if sub:
            price_article = sub.price or 0
            vat = self.env['account.tax'].search([
                ('name', '=', 'TVA collectée (vente) 10,0%')
            ], limit=1)
            vat_amount = vat.amount or 0
            nb_granule = 0

            # Calculate the number of granules based on the subscription
            # amount and the price of the granule
            denominator = price_article + vat_amount / 100 * price_article
            if denominator > 0:
                nb_granule = floor(sub.amount / denominator)
            else:
                nb_granule = 0

            fiscal_position = self.fiscal_position_id
            if article_granule:
                # Get the product account for the granule product based
                # on fiscal position
                article_granule.product_tmpl_id.get_product_accounts(
                    fiscal_pos=fiscal_position)
                vals = {
                    'product_id': article_granule.id,
                    'product_uom': article_granule.uom_id.id,
                    'name': article_granule.display_name,
                    'product_uom_qty': nb_granule,
                    'price_unit': price_article
                }

                # Add default values for the new order line
                vals = self.env['sale.order.line']._add_missing_default_values(
                    vals)
                self.order_line = [(0, 0, vals)]
    else:
        raise UserError(_("There are no product named 'GRANULE' "))
