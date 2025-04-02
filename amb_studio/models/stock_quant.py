from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    rserv = fields.Float(
        string="Réservé", copy=False, readonly=True, compute="_compute_rserv"
    )
    dispo_la_vente = fields.Float(
        string="Dispo à la Vente",
        copy=False,
        readonly=True,
        compute="_compute_dispo_la_vente",
    )
    commandes_fournisseurs_en_cours = fields.Float(
        string="Commandes Fournisseurs en Cours",
        copy=False,
        readonly=True,
        compute="_compute_commandes_fournisseurs_en_cours",
    )
    quantit_terme = fields.Float(
        string="Quantité à Terme",
        copy=False,
        readonly=True,
        compute="_compute_quantit_terme",
    )
    type_article = fields.Selection(
        string="Type Article",
        copy=False,
        readonly=True,
        tracking="100",
        help="A storable product is a product for which you manage stock. The Inventory app has to be installed.\nA consumable product is a product for which stock is not managed.\nA service is a non-material product you provide.",
        related="product_tmpl_id.type",
    )

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

    def _compute_dispo_la_vente(self):
        for record in self:
            record["dispo_la_vente"] = record.quantity - record.rserv

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

    def _compute_quantit_terme(self):
        for record in self:
            record["quantit_terme"] = (
                record.quantity - record.rserv + record.commandes_fournisseurs_en_cours
            )
