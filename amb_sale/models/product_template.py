from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    supplier_id = fields.Many2one('res.partner', string='Supplier',
                                  compute='_compute_supplier_info', store=True)

    @api.depends('seller_ids')
    def _compute_supplier_info(self):
        for product in self.filtered(lambda x: x.seller_ids):
            product.supplier_id = product.seller_ids[0].id
