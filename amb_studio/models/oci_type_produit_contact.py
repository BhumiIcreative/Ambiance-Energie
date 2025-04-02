from odoo import fields, models


class oci_type_produit_contact(models.Model):
    _name = "oci.type.produit.contact"
    _description = "Oci Type produit Contact"

    name = fields.Char(string="Name", copy=False)
