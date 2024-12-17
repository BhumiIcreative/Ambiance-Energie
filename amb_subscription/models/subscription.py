# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import datetime

import logging
log = logging.getLogger(__name__).info


class SubscriptionWoodPellet(models.Model):
    _name = 'subscription.wood.pellet'
    _description = 'Subscription wood pellet'

    @api.depends('amount')
    def _modif_amount(self):
        for s in self:
            account_payments = self.env['account.payment'].search([
                ('partner_id', '=', s.partner_id.id),
                ('payment_type', '=', 'inbound'),
            ])
            amount = 0
            other_amount = 0
            for account_payment in account_payments:
                amount += account_payment.amount
                other_account_payments = account_payment.reconciled_invoice_ids
                for other_account_payment in other_account_payments:
                    other_amount += other_account_payment.amount_total
                #prendre le champ reconciled_invoice_ids de la classe account_payment du bouton button_invoices
                # et ensuite se déplacer avec un for pour recup le montant des autres factures
                # pour ensuite soustraire le amount départ avec le amount des ces factures ci
                # et faut faire une vérif avec un si >0 alors ok t modif amount client sinon erreur

            new_amount = amount - other_amount
            if new_amount >= 0:
                s.amount += new_amount
            # else:
            #     raise ValidationError(_("Value under 0"))

    @api.onchange('date_start', 'date_end', 'partner_id')
    def _cpt_name(self):
        for subscription_id in self:
            subscription_id.name = ("SUB " + str(subscription_id.partner_id.name) +
            " from " + str(subscription_id.date_start) + " to " +
            str(subscription_id.date_end))

    name = fields.Char(string=_('Subscription'), required=True,
     copy=False, readonly=True, index=True, default=lambda self: _('New'),
     compute='_cpt_name')
    date_start = fields.Date(string=_('Date start'), required=True)
    date_end = fields.Date(string=_('Date end'), required=True)
    price = fields.Float(string=_('Price'))
    amount = fields.Float(string=_('Balance'), readonly=True, compute='_modif_amount')
    renewable = fields.Boolean(string=_('Renewable'), default=False)
    type_subscription = fields.Selection([
        ('a', _('Standard')),
        ('b', _('Not standard')),
    ], string=_('Type subscription'), default='a')
    partner_id = fields.Many2one('res.partner', string=_('Partner'), required=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('subscription.wood.pellet') or _('Sub')
        return super(SubscriptionWoodPellet, self).create(vals)

    def generate_payments(self):
        if datetime.date.today().day == int(self.env['ir.config_parameter'].get_param('date_exec_payment')):
            for subscription in self.search([('date_start', '<', datetime.datetime.now()),
                ('date_end', '>', datetime.datetime.now())]):
                # generate payment
                vals = {
                    'amount': subscription.price,
                    'journal_id': self.env['account.journal'].search([('code','=','BNK1')]).id,
                    'payment_date': datetime.datetime.now(),
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'payment_method_id': self.env['account.payment.method'].search([
                        ('code', '=', 'electronic'),
                        ('payment_type','=','inbound'),
                    ]).id,
                    'partner_id': subscription.partner_id.id,
                    'communication': self.name,
                }
                payment = self.env['account.payment'].create(vals)
                payment.action_register_payment()

        return True
