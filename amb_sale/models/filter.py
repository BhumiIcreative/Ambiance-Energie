from odoo import models, api, fields, _


class ProductFilter(models.Model):
    _inherit = 'product.template'

    supplier_id = fields.Many2one('res.partner', string=_('Supplier'),
                                  compute='_compute_supplierinfor', store=True)

    @api.depends('seller_ids')
    def _compute_supplierinfor(self):
        for product in self:
            if len(product.seller_ids) > 0:
                product.supplier_id = product.seller_ids[0].name.id
