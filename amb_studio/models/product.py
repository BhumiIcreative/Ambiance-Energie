# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    field_zxHZP = fields.Many2many(
        "product.template.attribute.value",
        string="Valeur caratéristique du modèle produit",
        copy=False,
        ondelete="cascade",
    )
    frais_approche_article = fields.Char(string="Frais approche", copy=False)
    non_remisable_1 = fields.Boolean(string="Non remisable", copy=False)
    commandes_clients = fields.One2many(
        "sale.order.line",
        "product_template_id",
        string="Commandes clients",
        copy=False,
        domain=[("commande_en_cours", ">", 0)],
    )
    stocks = fields.One2many(
        "stock.quant",
        "product_tmpl_id",
        string="Stocks",
        copy=False,
        domain=[("location_id.usage", "=", "internal")],
    )
    rf_fournisseur = fields.Char(
        string="Réf fournisseur",
        copy=False,
        readonly=True,
        help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.",
        related="product_variant_id.seller_ids.product_code",
    )
    field_jPwOa = fields.One2many(
        "stock.move",
        "product_tmpl_id",
        string="Commandes en cours",
        copy=False,
        readonly=True,
        domain=[
            "&",
            "&",
            ("group_id.sale_id", "!=", False),
            ("state", "!=", "done"),
            ("state", "!=", "cancel"),
        ],
    )
    dernier_prix_dachat_fournisseur = fields.Float(
        string="Dernier prix d'achat fournisseur",
        copy=False,
        readonly=True,
        help="The price to purchase a product",
        related="product_variant_id.seller_ids.price",
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    field_VojtB = fields.Monetary(string="New Monétaire", copy=False)
    commandes_clients = fields.One2many(
        "sale.order.line",
        "product_id",
        string="Commandes clients",
        copy=False,
        domain=[("commande_en_cours", ">", 0)],
    )
    stocks_1 = fields.One2many(
        "stock.quant",
        "product_id",
        string="stocks",
        copy=False,
        domain=[("location_id.usage", "=", "internal")],
    )
    commandes_en_cours = fields.One2many(
        "stock.move",
        "product_id",
        string="Commandes en cours",
        copy=False,
        readonly=True,
        domain=[
            "&",
            "&",
            ("group_id.sale_id", "!=", False),
            ("state", "!=", "done"),
            ("state", "!=", "cancel"),
        ],
    )
