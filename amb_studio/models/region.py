from odoo import fields, models


class region(models.Model):
    _name = "region"
    _description = "Region"

    name = fields.Char(string="Name", copy=False)
    code = fields.Char(string="Code", copy=False, required=True)
    pays_id = fields.Many2one("res.country", string="Pays", copy=False, required=True)
