from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    field_RFPir_id = fields.Many2one(
        "stock.warehouse", string="Warehouse", copy=False, ondelete="set null"
    )
    field_pkvcm_ids = fields.Many2many(
        "stock.location",
        "x_stock_location_stock_valuation_layer_rel",
        string="Inventory Locations",
        copy=False,
        ondelete="cascade",
    )
    magasin = fields.Char(
        string="Store", copy=False, readonly=True, compute="_compute_magasin"
    )

    @api.depends(
        "quantity",
        "stock_move_id.location_id.name",
        "stock_move_id.location_dest_id.name",
    )
    def _compute_magasin(self):
        for record in self:
            if record.quantity > 0:
                record["magasin"] = record.stock_move_id.location_dest_id.name
            else:
                record["magasin"] = record.stock_move_id.location_id.name
