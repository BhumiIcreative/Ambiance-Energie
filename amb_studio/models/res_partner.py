# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    siret_contact = fields.Char(string="N°Siret", copy=False)
    ape_contact = fields.Char(string="APE", copy=False)
    telephone3_contact = fields.Char(string="Téléphone 3 / Fax", copy=False)
    ancien_proprietaire_contact = fields.Many2one(
        "res.partner", string="Nom ancien propriétaire", copy=False, ondelete="set null"
    )
    nom_parrainage_contact = fields.Many2one(
        "res.partner", string="Nom contact parrainage", copy=False, ondelete="set null"
    )
    numero_serie_equipement_contact = fields.Char(string="N°Série")
    modele_equipement_contact = fields.Char(string="Modèle")
    type_produit_contact = fields.Many2many(
        "oci_type_produit_contact",
        string="Type produit",
        copy=False,
        ondelete="cascade",
    )
    provenance_contact = fields.Many2one(
        "oci_provenance_contact", string="Provenance", copy=False, ondelete="set null"
    )
    commercial_contact = fields.Many2one(
        "hr.employee", string="Commercial", copy=False, ondelete="set null"
    )
    est_un_client = fields.Boolean(string="Est un client", copy=False)
    est_un_fournisseur = fields.Boolean(string="Est un fournisseur", copy=False)
    date_de_pose_equipement_contact = fields.Char(string="Date de pose")
    point_de_vente = fields.Many2one(
        "point_de_vente", string="Point de vente", copy=False, ondelete="set null"
    )
    autre_information_equipement_contact = fields.Char(string="Autre information")
    liste_de_prix = fields.Char(
        string="Liste de Prix-",
        copy=False,
        readonly=True,
        related="property_product_pricelist.display_name",
    )
    facturation_ttc = fields.Boolean(string="Facturation TTC", copy=False)
    region = fields.Many2one("region", string="Région", copy=False, ondelete="set null")
    telephone2_contact = fields.Char(string="Téléphone 2", copy=False)
    mobile2 = fields.Char(string="Mobile 2", copy=False)
    mobile3 = fields.Char(string="Mobile 3", copy=False)
    oci_sms_granules = fields.Boolean(string="SMS GRANULES", copy=False)
    oci_sms_promo_entretien = fields.Boolean(string="SMS PROMO ENTRETIEN", copy=False)
