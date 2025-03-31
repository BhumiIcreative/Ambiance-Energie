# -*- coding: utf-8 -*-
from odoo import fields, models


class PointDeVente(models.Model):
    _name = "point_de_vente"
    _description = "Point de Vente"

    name = fields.Char(string="Name", copy=False)
    pos_archive = fields.Boolean(string="Archivé", copy=False)
    oci_contact_pof_societe = fields.Many2one(
        "res.company", string="Sociétés", copy=False, ondelete="set null"
    )
    entrepot = fields.Many2one(
        "stock.warehouse", string="Entrepot", copy=False, ondelete="set null"
    )
    qrcode_payment = fields.Binary(string="QR Code Paiement", copy=False)
