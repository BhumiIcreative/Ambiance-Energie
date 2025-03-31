# -*- coding: utf-8 -*-
from odoo import fields, models


class oci_provenance_contact(models.Model):
    _name = "oci_provenance_contact"
    _description = "OCi Provenance Contact"

    name = fields.Char(string="Name", copy=False)
