from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    client = fields.Char(
        string="Client",
        copy=False,
        readonly=True,
        related="group_id.sale_id.partner_id.name",
    )
    point_de_vente = fields.Char(
        string="Point de Vente",
        copy=False,
        readonly=True,
        related="warehouse_id.display_name",
    )
    client_1 = fields.Char(
        string="Client",
        copy=False,
        readonly=True,
        related="group_id.sale_id.partner_id.display_name",
    )
    point_de_vente_1 = fields.Char(
        string="Point de Vente",
        copy=False,
        readonly=True,
        related="warehouse_id.display_name",
    )
    field_P710Y = fields.Char(
        string="New Champ Lié",
        copy=False,
        readonly=True,
        related="location_id.parent_path",
    )
    point_de_vente_2 = fields.Char(
        string="Point de Vente", copy=False, readonly=True, related="location_id.name"
    )
