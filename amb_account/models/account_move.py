from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

import datetime

import logging

log = logging.getLogger(__name__).info


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _autopost_draft_entries_asc(self):
        """This method is called from a cron job.
        It is used to post entries such as those created by the module
        account_asset.
        """
        records = self.search(
            [
                ("state", "=", "draft"),
                ("date", "<=", fields.Date.context_today(self)),
                ("auto_post", "=", True),
            ],
            order="id asc",
        )
        for ids in self._cr.split_for_in_conditions(records.ids, size=1000):
            self.browse(ids).post()
            if not self.env.registry.in_test_mode():
                self._cr.commit()

    def _compute_origin_so(self):
        """
        Computes and sets the originating sale order for the record
        based on the linked invoice lines and their sale order lines.
        """
        for rec in self:
            rec.origin_so = rec.invoice_line_ids.mapped(
                "sale_line_ids"
            ).order_id[:1]

    client_situation = fields.Monetary(
        string="Client situation", related="partner_id.total_due"
    )
    current_subscription = fields.Many2one(
        "subscription.wood.pellet", string="Current subscription wood pellet"
    )
    package_count = fields.Integer(string="Package count")
    weight = fields.Float(string="Weight")
    volume = fields.Float(string="Volume")
    port = fields.Float(string="Port")
    shipped = fields.Float(string="Shipped")
    comment = fields.Char(string="Comment")
    commissioning_identification = fields.Char(string="Identification")
    type_invoice = fields.Selection(
        [
            ("std", "Standard"),
            ("gran", "Granule"),
            ("serv", "Service"),
            ("sto", "Stove"),
        ],
        string="Type invoice",
        default="std",
    )
    purchase_stock_picking_bill_id = fields.Many2one(
        "stock.picking",
        store=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
        string="Stock picking",
        help="Auto-complete from a Stock picking.",
    )
    oci_point_of_sale = fields.Many2one(
        "oci.point.of.sale", string="Point of sale"
    )
    sent_by = fields.Many2one("res.partner", string="Sent by")
    origin_so = fields.Many2one("sale.order", compute=_compute_origin_so)

    @api.constrains("oci_point_of_sale")
    def _check_point_of_sale(self):
        """
        Validates that the 'oci_point_of_sale' is provided for standard invoices
        and refunds. Raises a ValidationError if the field is missing.
        """
        for r in self:
            if (
                r.move_type in ("out_refund", "out_invoice")
                and r.type_invoice == "std"
                and not r.oci_point_of_sale
            ):
                raise ValidationError(
                    "Point of sale is required on standard invoice"
                )

    @api.model
    def create(self, vals):
        """
        Creates an invoice and updates related fields from the sale order
        if 'invoice_origin' is provided.
        """
        if vals.get("invoice_origin"):
            sale = self.env["sale.order"].search(
                [("name", "=", vals["invoice_origin"])]
            )
            if sale:
                vals.update(
                    {
                        "type_invoice": sale.type_order,
                        "oci_point_of_sale": sale.oci_point_of_sale.id,
                        "payment_instrument_id": sale.payment_instrument_id.id,
                    }
                )
        invoice = super(AccountMove, self).create(vals)
        return invoice

    def action_post(self):
        """
        Posts the invoice and checks for sufficient subscription balance before
        confirming the quotation. If the invoice is of type "gran", it also
        registers a payment linked to the current subscription.
        """
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
                        _(
                            "Invoice amount is greater than balance subscription."
                        )
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
                            [
                                ("code", "=", "manual"),
                                ("payment_type", "=", "inbound"),
                            ]
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

    def generate_invoice_rest_payments(self):
        """
        Searches for posted customer invoices with outstanding balances and
        attempts to generate the remaining payments. Logs any UserError exceptions.
        """
        in_need_of_action = self.env["account.move"].search(
            [
                ("state", "in", ["posted"]),
                ("amount_residual", "!=", 0),
                ("move_type", "in", ["out_invoice"]),
            ]
        )

        for move in in_need_of_action:
            try:
                move._generate_invoice_rest_payments()
            except UserError as e:
                log.exception(e)

    def _generate_invoice_rest_payments(self):
        """
        Generates a payment for the remaining invoice amount based on the company
        and associates it with the invoice. Creates a new payment if the total
        amount is greater than the sum of existing payments.
        """
        self.ensure_one()
        if self.company_id.id == 1:
            var_journal_id = 12
        if self.company_id.id == 2:
            var_journal_id = 40

        payment_res = {
            "payment_type": "inbound",
            "partner_type": "customer",
            "state": "draft",
            "invoice_ids": [(6, 0, self.ids)],
            "partner_id": self.partner_id.id,
            "amount": self.amount_residual,
            "payment_date": self.invoice_date,
            "journal_id": var_journal_id,
            "payment_method_id": self.env.ref(
                "account.account_payment_method_manual_in"
            ).id,
            "communication": self.name + " / reste à payer",
            "company_id": self.company_id.id,
            "oci_point_of_sale": self.oci_point_of_sale.id,
            "payment_instrument_id": self.payment_instrument_id.id,
        }

        self._cr.execute(
            """
            SELECT SUM(amount)
            FROM account_payment
            WHERE id IN (
                SELECT payment_id FROM account_invoice_payment_rel WHERE invoice_id = %s
            )
        """,
            [self.id],
        )
        query_res = self._cr.fetchone()
        sum = query_res and query_res[0] or 0.0

        if sum < self.amount_total:
            res = self.env["account.payment"].create(payment_res)
            log("created %s", res)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    oci_point_of_sale = fields.Many2one(
        "oci.point.of.sale",
        string="Point of sale",
        related="move_id.oci_point_of_sale",
    )
