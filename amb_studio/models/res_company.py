from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    fax_societe_oci = fields.Char(string="FAX", copy=False)
    field_oDhjr = fields.Char(string="New Texte", copy=False)
    oci_conf_qualibois = fields.Char(string="Qualibois", copy=False)
    oci_conf_rib = fields.Char(string="RIB", copy=False)
    oci_conf_formejurid = fields.Char(string="Forme Juridique et capital", copy=False)
    oci_conf_siren = fields.Char(string="SIREN", copy=False)
    oci_conf_juridique = fields.Char(string="Forme Juridique Simplifiée", copy=False)
    oci_conf_bic = fields.Char(string="BIC", copy=False)
    assurance = fields.Char(string="Garantie RC et Décenale", copy=False)
