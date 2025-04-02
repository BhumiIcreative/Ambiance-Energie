from odoo import fields, models


class technicien(models.Model):
    _name = "technicien"
    _description = "Technicien"

    name = fields.Char(string="Name", copy=False)
