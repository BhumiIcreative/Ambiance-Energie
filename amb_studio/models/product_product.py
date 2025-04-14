from odoo import fields, models


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
