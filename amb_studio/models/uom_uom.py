# -*- coding: utf-8 -*-
from odoo import fields, models


class UomUom(models.Model):
    _inherit = "uom.uom"

    uom_id__product_template_count = fields.Integer(
        string="Unit of Measure count",
        copy=False,
        compute="_compute_uom_id__product_template_count",
    )

    def _compute_uom_id__product_template_count(self):
        results = self.env["product.template"].read_group(
            [("uom_id", "in", self.ids)], ["uom_id"], ["uom_id"]
        )
        dic = {}
        for x in results:
            dic[x["uom_id"][0]] = x["uom_id_count"]
        for record in self:
            record["uom_id__product_template_count"] = dic.get(record.id, 0)
