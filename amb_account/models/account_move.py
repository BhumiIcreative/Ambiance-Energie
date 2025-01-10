# coding: utf-8

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
        for rec in self:
            rec.origin_so = rec.invoice_line_ids.mapped("sale_line_ids").order_id[:1]

    client_situation = fields.Monetary(
        string=_("Client situation"), related="partner_id.total_due"
    )
   
    package_count = fields.Integer(string=_("Package count"))
    weight = fields.Float(string=_("Weight"))
    volume = fields.Float(string=_("Volume"))
    port = fields.Float(string=_("Port"))
    shipped = fields.Float(string=_("Shipped"))
    comment = fields.Char(string=_("Comment"))
    commissioning_identification = fields.Char(string=_("Identification"))
    type_invoice = fields.Selection(
        [
            ("std", _("Standard")),
            ("gran", _("Granule")),
            ("serv", _("Service")),
            ("sto", _("Stove")),
        ],
        string=_("Type invoice"),
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
    oci_point_of_sale = fields.Many2one("oci.point.of.sale", string=_("Point of sale"))
    sent_by = fields.Many2one("res.partner", string=_("Sent by"))
    origin_so = fields.Many2one("sale.order", compute=_compute_origin_so)

    @api.constrains("oci_point_of_sale")
    def _check_point_of_sale(self):
        for r in self:
            if (
                r.move_type in ("out_refund", "out_invoice")
                and r.type_invoice == "std"
                and not r.oci_point_of_sale
            ):
                raise ValidationError("Point of sale is required on standard invoice")

    @api.model
    def create(self, vals):
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

    

    def generate_invoice_rest_payments(self):
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
        self.ensure_one()
        ####################
        # variables en dur #
        ####################
        if self.company_id.id == 1:  # société Ambiance Energie
            var_journal_id = 12
        if self.company_id.id == 2:  # société Ambiance Energie
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
        string=_("Point of sale"),
        related="move_id.oci_point_of_sale",
    )
    # Augmenter la précision de discount pour éviter les arrondis quand on travaille en remise fixe
    discount = fields.Float(digits=(14, 10))
    discount_fixed = fields.Float(
        string="Discount (Fixed)",
        digits="Product Price",
        default=0.00,
        help="Fixed amount discount.",
    )

    @api.onchange("discount")
    def _onchange_discount(self):
        self.discount_fixed = self.quantity * self.price_unit * self.discount / 100

    @api.onchange("discount_fixed", "quantity", "price_unit")
    def _onchange_discount_fixed(self):
        if self.price_unit == 0.00 or self.quantity == 0.00:
            self.discount = 0.00
        else:
            self.discount = (
                self.discount_fixed / (self.quantity * self.price_unit) * 100
            )
