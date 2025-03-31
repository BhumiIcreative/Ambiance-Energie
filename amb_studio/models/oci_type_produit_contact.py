# -*- coding: utf-8 -*-
from odoo import fields, models


class oci_type_produit_contact(models.Model):
    _name = "oci_type_produit_contact"
    _description = "Oci Type produit Contact"

    name = fields.Char(string="Name", copy=False)
