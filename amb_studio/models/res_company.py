from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    fax_societe_oci = fields.Char(string="FAX", copy=False)
    field_oDhjr = fields.Char(string="New Text", copy=False)
    oci_conf_qualibois = fields.Char(string="Qualibois", copy=False)
    oci_conf_rib = fields.Char(string="RIB", copy=False)
    oci_conf_formejurid = fields.Char(string="Legal form and capital", copy=False)
    oci_conf_siren = fields.Char(string="SIREN", copy=False)
    oci_conf_juridique = fields.Char(string="Simplified Legal Form", copy=False)
    oci_conf_bic = fields.Char(string="BIC", copy=False)
    assurance = fields.Char(string="Civil Liability and Ten-Year Warranty", copy=False)
    second_partner_id = fields.Many2one("res.partner", string="Second Contact")

