from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    siret_contact = fields.Char(string="N°Name", copy=False)
    ape_contact = fields.Char(string="APE", copy=False)
    telephone3_contact = fields.Char(string="Phone 3 / Fax", copy=False)
    ancien_proprietaire_contact_id = fields.Many2one(
        "res.partner", string="Former owner name", copy=False, ondelete="set null"
    )
    nom_parrainage_contact_id = fields.Many2one(
        "res.partner",
        string="Sponsorship contact name",
        copy=False,
        ondelete="set null",
    )
    numero_serie_equipement_contact = fields.Char(string="Serial No.")
    modele_equipement_contact = fields.Char(string="Model")
    type_produit_contact_ids = fields.Many2many(
        "oci.type.produit.contact",
        "x_res_partner_x_oci_type_produit_contact_rel",
        string="Product Type",
        copy=False,
        ondelete="cascade",
    )
    provenance_contact_id = fields.Many2one(
        "oci.provenance.contact", string="Origin", copy=False, ondelete="set null"
    )
    commercial_contact_id = fields.Many2one(
        "hr.employee", string="Commercial", copy=False, ondelete="set null"
    )
    est_un_client = fields.Boolean(string="Is a customer", copy=False, store=True)
    est_un_fournisseur = fields.Boolean(string="Is a supplier", copy=False)
    date_de_pose_equipement_contact = fields.Char(string="Installation date")
    point_de_vente_id = fields.Many2one(
        "point.de.vente", string="Point of sale", copy=False, ondelete="set null"
    )
    autre_information_equipement_contact = fields.Char(string="Other Information")
    liste_de_prix = fields.Char(
        string="Price List-",
        copy=False,
        readonly=True,
        related="property_product_pricelist.display_name",
        store=True
    )
    facturation_ttc = fields.Boolean(string="Invoicing Including Tax", copy=False)
    region_id = fields.Many2one(
        "region", string="Regions", copy=False, ondelete="set null"
    )
    telephone2_contact = fields.Char(string="Phone 2", copy=False)
    mobile2 = fields.Char(string="Mobile 2", copy=False)
    mobile3 = fields.Char(string="Mobile 3", copy=False)
    oci_sms_granules = fields.Boolean(string="SMS GRANULES", copy=False)
    oci_sms_promo_entretien = fields.Boolean(string="SMS PROMO INTERVIEW", copy=False)
