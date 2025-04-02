from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    field_zxHZP_ids = fields.Many2many(
        "product.template.attribute.value",
        "x_product_template_product_template_attribute_value_rel",
        string="Characteristic value of the product model",
        copy=False,
        ondelete="cascade",
    )

    frais_approche_article = fields.Char(string="Fresh Approach", copy=False)
    non_remisable_1 = fields.Boolean(string="Non-Refundable", copy=False)
    commandes_clients_ids = fields.One2many(
        "sale.order.line",
        "product_template_id",
        string="Customer orders",
        copy=False,
        domain=[("commande_en_cours", ">", 0)],
    )
    stocks_ids = fields.One2many(
        "stock.quant",
        "product_tmpl_id",
        string="Stocks",
        copy=False,
        domain=[("location_id.usage", "=", "internal")],
    )
    rf_fournisseur = fields.Char(
        string="Supplier Ref",
        copy=False,
        readonly=True,
        help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.",
        related="product_variant_id.seller_ids.product_code",
    )
    field_jPwOa_ids = fields.One2many(
        "stock.move",
        "product_tmpl_id",
        string="Current Orders",
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
        string="Dernier Prix D'achat Fournisseur",
        copy=False,
        readonly=True,
        help="The price to purchase a product",
        related="product_variant_id.seller_ids.price",
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    field_VojtB = fields.Monetary(string="New Monetary", copy=False)
    commandes_clients_ids = fields.One2many(
        "sale.order.line",
        "product_id",
        string="Customer Orders",
        copy=False,
        domain=[("commande_en_cours", ">", 0)],
    )
    stocks_1_ids = fields.One2many(
        "stock.quant",
        "product_id",
        string="Stocks",
        copy=False,
        domain=[("location_id.usage", "=", "internal")],
    )
    commandes_en_cours_ids = fields.One2many(
        "stock.move",
        "product_id",
        string="Current Orders",
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
