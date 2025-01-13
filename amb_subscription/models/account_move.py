 # coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

import datetime

import logging

log = logging.getLogger(__name__).info


class AccountMove(models.Model):
    _inherit = "account.move"
    
    current_subscription = fields.Many2one(
            "subscription.wood.pellet", string=_("Current subscription wood pellet")
        )


    @api.model
    def create(self, vals):
        if vals.get("invoice_origin"):
            sale = self.env["sale.order"].search(
                [("name", "=", vals["invoice_origin"])]
            )
            if sale:
                vals.update(
                    {
                        "current_subscription": sale.current_subscription.id,
                    }
                )
        invoice = super(AccountMove, self).create(vals)
        return invoice

    def action_post(self):
        if (
            self.type_invoice == "gran"
            and self.amount_total > self.current_subscription.amount
        ):
            raise UserError(
                _(
                    "You can't confirm the quotation, amount in subscription is not sufficient"
                )
            )
        res = super(AccountMove, self).action_post()

        if self.type_invoice == "gran":
            # register payment
            subscription = self.env["subscription.wood.pellet"].search(
                [
                    ("partner_id", "=", self.partner_id.id),
                    ("date_start", "<", datetime.datetime.now()),
                    ("date_end", ">", datetime.datetime.now()),
                ]
            )
            if subscription:
                if subscription.amount < self.amount_total:
                    raise ValidationError(
                        _("Invoice amount is greater than balance subscription.")
                    )
                else:
                    vals = {
                        "amount": self.amount_total,
                        "journal_id": self.env["account.journal"]
                        .search([("code", "=", "BNK1")])
                        .id,
                        "payment_date": datetime.datetime.now(),
                        "payment_type": "inbound",
                        "partner_type": "customer",
                        "payment_method_id": self.env["account.payment.method"]
                        .search(
                            [("code", "=", "manual"), ("payment_type", "=", "inbound")]
                        )
                        .id,
                        "partner_id": self.partner_id.id,
                        "communication": self.name,
                        "invoice_ids": [(6, 0, [self.id])],
                        "company_id": self.company_id.id,
                    }
                    payment = self.env["account.payment"].create(vals)
                    payment.action_register_payment()
        return res

    def create_payment_vals_dict(self):
        res = super().create_payment_vals_dict()
        res["payment_instrument_id"] = self.payment_instrument_id.id
        return res
