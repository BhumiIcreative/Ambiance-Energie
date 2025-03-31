# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountFullReconcile(models.Model):
    _inherit = "account.full.reconcile"

    dernire_ecriture_comptable = fields.Many2one(
        "account.move.line",
        string="Last accounting entry",
        copy=False,
        readonly=True,
        ondelete="set null",
        compute="_compute_dernire_ecriture_comptable",
    )
    count_aml = fields.Integer(
        string="count_aml", copy=False, readonly=True, compute="_compute_count_aml"
    )

    @api.depends('reconciled_line_ids')
    def _compute_dernire_ecriture_comptable(self):
        for record in self:
            if record.reconciled_line_ids:
                last_aml = record.reconciled_line_ids[0]
                for aml in record.reconciled_line_ids:
                    if aml.date > last_aml.date:
                        last_aml = aml
                record["dernire_ecriture_comptable"] = last_aml

    @api.depends('reconciled_line_ids')
    def _compute_count_aml(self):
        for record in self:
            record["count_aml"] = len(record.reconciled_line_ids)
