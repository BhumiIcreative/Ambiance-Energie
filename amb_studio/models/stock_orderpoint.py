# -*- coding: utf-8 -*-
from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    oci_stock_fournisseur = fields.Char(
        string="Fournisseur",
        copy=False,
        readonly=True,
        related="product_id.seller_ids.display_name",
    )
