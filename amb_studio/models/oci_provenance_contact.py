from odoo import fields, models


class oci_provenance_contact(models.Model):
    _name = "oci.provenance.contact"
    _description = "OCi Provenance Contact"

    name = fields.Char(string="Name", copy=False)
