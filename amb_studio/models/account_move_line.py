from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"


    date_de_lettrage = fields.Date(
        string="Matching Date",
        copy=False,
        readonly=True,
        help="Give the date of the most recent accounting entry in the reconciliation.",
        related="full_reconcile_id.dernire_ecriture_comptable_id.date",
    )