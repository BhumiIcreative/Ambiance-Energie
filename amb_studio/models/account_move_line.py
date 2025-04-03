from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # taxes_audit = fields.Char(
    #     string="taxes_audit", copy=False, readonly=True, compute="_compute_taxes_audit"
    # )
    date_de_lettrage = fields.Date(
        string="Matching Date",
        copy=False,
        readonly=True,
        help="Give the date of the most recent accounting entry in the reconciliation.",
        related="full_reconcile_id.dernire_ecriture_comptable_id.date",
    )

    # @api.depends('tax_audit')
    # def _compute_taxes_audit(self):
    #     for record in self:
    #         if record["tax_audit"]:
    #             split_str = (record["tax_audit"] or "").split(":")
    #             taxes_audit = split_str[0] if len(split_str) > 1 else ""
    #             record["taxes_audit"] = taxes_audit.replace(
    #                 "Base due intra", "Base intra"
    #             ).replace("Base déductible intra", "Base intra")
