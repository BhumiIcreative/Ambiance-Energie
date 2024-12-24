import datetime
from odoo import api, fields, models, _


class SubscriptionWoodPellet(models.Model):
    _name = "subscription.wood.pellet"
    _description = "Subscription wood pellet"

    name = fields.Char(
        string="Subscription",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
        compute="_compute_name",
    )
    date_start = fields.Date(string="Date Start", required=True)
    date_end = fields.Date(string="Date End", required=True)
    price = fields.Float(string="Price")
    amount = fields.Float(string="Balance", readonly=True, compute="_modify_amount")
    renewable = fields.Boolean(string="Renewable", default=False)
    type_subscription = fields.Selection(
        [("a", "Standard"), ("b", "Not standard")],
        string="Type Subscription",
        default="a",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    def _modify_amount(self):
        """
            Update the subscription balance based on customer payments and reconciled invoices.
        """
        for subscription in self:
            account_payments = self.env["account.payment"].search(
                [
                    ("partner_id", "=", subscription.partner_id.id),
                    ("payment_type", "=", "inbound"),
                ]
            )

            amount = sum(account_payments.mapped("amount"))
            other_amount = sum(
                account_payments.mapped("reconciled_invoice_ids.amount_total")
            )

            new_amount = amount - other_amount
            if new_amount >= 0:
                subscription.amount += new_amount

    @api.onchange("date_start", "date_end", "partner_id")
    def _compute_name(self):
        """
            Automatically generates the subscription name based on partner
            name and date range.
        """
        for subscription_id in self:
            if (
                subscription_id.date_start
                and subscription_id.date_end
                and subscription_id.partner_id
            ):
                subscription_id.name = (
                    "SUB "
                    + str(subscription_id.partner_id.name)
                    + " from "
                    + str(subscription_id.date_start)
                    + " to "
                    + str(subscription_id.date_end)
                )

    def generate_payments(self):
        """
            Create customer payments for active subscriptions on a specific
            date through schedular.
        """
        if datetime.date.today().day == int(
            self.env["ir.config_parameter"].get_param("date_exec_payment")
        ):
            for subscription in self.search(
                [
                    ("date_start", "<", datetime.datetime.now()),
                    ("date_end", ">", datetime.datetime.now()),
                ]
            ):
                # generate payment
                self.env["account.payment"].create(
                    {
                        "amount": subscription.price,
                        "journal_id": self.env["account.journal"].search(
                            [("code", "=", "BNK1")], limit=1).id,
                        "date": datetime.datetime.now(),
                        "payment_type": "inbound",
                        "partner_type": "customer",
                        "payment_method_id": self.env["account.payment.method"]
                        .search(
                            [
                                ("code", "=", "electronic"),
                                ("payment_type", "=", "inbound"),
                            ]
                        )
                        .id,
                        "partner_id": subscription.partner_id.id,
                        "ref": self.name,
                    }
                ).move_id.action_register_payment()
        return True
