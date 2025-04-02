from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    field_gmEvU = fields.Integer(string="Field gmEvU", copy=False)
    le_poele_a_granule_est_un_chauffage_d_appoint = fields.Char(
        string="The Pellet Stove Is a Supplemental Heater", copy=False
    )
