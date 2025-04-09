from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    rserv = fields.Float(
        string="Reserve", copy=False, readonly=True, compute="_compute_rserv"
    )
    dispo_la_vente = fields.Float(
        string="Available for sale",
        copy=False,
        readonly=True,
        compute="_compute_dispo_la_vente",
    )
    commandes_fournisseurs_en_cours = fields.Float(
        string="Current Supplier Orders",
        copy=False,
        readonly=True,
        compute="_compute_commandes_fournisseurs_en_cours",
    )
    quantit_terme = fields.Float(
        string="Forward quantity",
        copy=False,
        readonly=True,
        compute="_compute_quantit_terme",
    )
    type_article = fields.Selection(
        string="Type Item",
        copy=False,
        readonly=True,
        tracking="100",
        help="A storable product is a product for which you manage stock. The Inventory app has to be installed.\nA consumable product is a product for which stock is not managed.\nA service is a non-material product you provide.",
        related="product_tmpl_id.type",
    )
    rfrence_fournisseur = fields.Char(
        string="Supplier reference",
        copy=False,
        readonly=True,
        help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.",
        related="product_id.seller_ids.product_code",
    )
    rfrence_fournisseur_1 = fields.Char(
        string="Supplier reference",
        copy=False,
        readonly=True,
        help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.",
        related="product_id.seller_ids.product_code",
    )
    fournisseur = fields.Char(
        string="Supplier",
        copy=False,
        readonly=True,
        related="product_id.seller_ids.display_name",
    )

    # @api.depends("product_id.commandes_clients_ids.commande_en_cours")
    def _compute_rserv(self):
        for record in self:
            id_sale = self.env["sale.order.line"].search(
                [
                    "&",
                    ("product_id.id", "=", record.product_id.id),
                    (
                        "order_id.warehouse_id.lot_stock_id.id",
                        "=",
                        record.location_id.id,
                    ),
                ]
            )
            qty = sum(id_sale.mapped("commande_en_cours"))
            record["rserv"] = qty

    @api.depends("quantity", "rserv")
    def _compute_dispo_la_vente(self):
        for record in self:
            record["dispo_la_vente"] = record.quantity - record.rserv

    # @api.depends("product_id.purchase_order_line_ids.cde_frns_en_cours")
    def _compute_commandes_fournisseurs_en_cours(self):
        for record in self:
            id_sale = self.env["purchase.order.line"].search(
                [
                    "&",
                    ("product_id.id", "=", record.product_id.id),
                    (
                        "order_id.picking_type_id.warehouse_id.lot_stock_id.id",
                        "=",
                        record.location_id.id,
                    ),
                ]
            )
            qty = sum(id_sale.mapped("cde_frns_en_cours"))
            record["commandes_fournisseurs_en_cours"] = qty

    @api.depends("quantity", "rserv", "commandes_fournisseurs_en_cours")
    def _compute_quantit_terme(self):
        for record in self:
            record["quantit_terme"] = (
                record.quantity - record.rserv + record.commandes_fournisseurs_en_cours
            )
