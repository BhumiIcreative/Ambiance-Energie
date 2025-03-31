# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    pos_vendeur = fields.Many2one(
        "point_de_vente",
        string="pos_vendeur",
        copy=False,
        readonly=True,
        ondelete="set null",
        related="user_id.point_de_vente",
    )
    oci_saleorder_yourref = fields.Char(string="Votre référence", copy=False)
    oci_saleorder_refcustomer = fields.Char(
        string="Référence client", copy=False, readonly=True, related="partner_id.ref"
    )
    field_pMXi2 = fields.Many2one(
        "hr.employee", string="Employé", copy=False, ondelete="set null"
    )
    field_xAmex = fields.Many2many(
        "hr.employee", string="Employé", copy=False, ondelete="cascade"
    )
    oci_saleorder_technicien = fields.Many2one(
        "hr.employee", string="Technicien", copy=False, ondelete="set null"
    )
    adresse = fields.Char(
        string="Adresse",
        copy=False,
        readonly=True,
        related="partner_id.contact_address",
    )
    modle_de_poele = fields.Char(
        string="Modèle de poele",
        copy=False,
        readonly=True,
        related="partner_id.modele_equipement_contact",
    )
    no_invoiced = fields.Monetary(
        string="Non facturé",
        copy=False,
        readonly=True,
        help="Différence TTC entre la commande et les factures",
        compute="_compute_no_invoiced",
    )

    @api.depends('invoice_ids')
    def _compute_no_invoiced(self):
        for record in self:
            record["no_invoiced"] = record.amount_total - sum(
                record.invoice_ids.mapped(lambda x: x.amount_total_signed)
            )
