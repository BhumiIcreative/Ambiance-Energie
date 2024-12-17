# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import odoo.addons.decimal_precision as dp
from odoo import api, fields, models, _
import logging
log = logging.getLogger(__name__).info

class stock_location_product(models.Model):
    _name = 'stock.location.product'

    @api.depends('on_hand_qty', 'out_qty')
    def _compute_free_qty(self):
        for rec in self:
            rec['free_qty'] = rec.on_hand_qty - rec.out_qty

    @api.depends('custom_template_id.outgoing_qty',
                 'custom_template_id.categ_id',
                 'custom_template_id.seller_ids')
    def _compute_custom_fields(self):
        for rec in self:
            rec.outgoing_total = rec.custom_template_id.outgoing_qty if rec.custom_template_id else 0
            rec.category = rec.custom_template_id.categ_id.complete_name or ''
            rec.supplier = rec.custom_template_id.seller_ids.mapped('display_name')

    stock_location_id = fields.Many2one('stock.location', string="Location")
    on_hand_qty = fields.Float('On hand Quantity')
    custom_product_id = fields.Many2one('product.product')
    custom_template_id = fields.Many2one('product.template')
    forcasted_qty = fields.Float('Forcasted Quantity')
    incoming_qty = fields.Float('Incoming Quantity')
    out_qty = fields.Float('Out Quantity')

    outgoing_total = fields.Float('outgoing total', compute=_compute_custom_fields, store=True)
    free_qty = fields.Float('Dispo à la vente', compute=_compute_free_qty)
    supplier = fields.Char('Fournisseur',compute=_compute_custom_fields, store=True)
    category = fields.Char('Categorie', compute=_compute_custom_fields, store=True)


    def stock_by_location_action(self):

        products_to_update = self.env['product.template'].search([])

        for product in products_to_update:
            product.upate_compute_stock_location()

        products = self.env['stock.location.product'].search([
                ('custom_template_id', '!=', False)
            ])
        return {
                'name': _("Stock by location"),
                'type': 'ir.actions.act_window',
                'res_model': 'stock.location.product',
                'view_mode': 'tree',
                'view_type': 'form',
                'domain': [('id', 'in', products.ids)],
                'view_id': self.env.ref('stock_by_location.stock_by_location_tree_view').id,
                'context': {'group_by': ['category','custom_template_id']},
                'target': 'current',
            }

class product(models.Model):
    _inherit = 'product.product'

    stock_location = fields.One2many('stock.location.product', 'custom_product_id', string="Stock Location")

    def remove_filter(self):
        dict_pro = self._product_available()
        product_details = dict_pro.get(self.id)

        loc = self.env['stock.location'].search([('usage', '=', 'internal')])
        result = []
        created_ids = []
        for pro in self:
            for a in loc:

                domain_quant = [('product_id', '=', pro.id), ('location_id', '=', a.id)]
                domain_move_in = [('product_id', '=', pro.id), ('location_dest_id', '=', a.id)]
                domain_move_out = [('product_id', '=', pro.id), ('location_id', '=', a.id)]
                Move = self.env['stock.move']
                Quant = self.env['stock.quant']
                domain_move_in_todo = [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_move_in
                domain_move_out_todo = [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_move_out

                incoming = dict((item['product_id'][0], item['product_qty']) for item in
                                Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id']))
                outgoing = dict((item['product_id'][0], item['product_qty']) for item in
                                Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id']))
                on_hand = dict((item['product_id'][0], item['quantity']) for item in
                               Quant.read_group(domain_quant, ['product_id', 'quantity'], ['product_id']))

                on_hand_qty = product_details.get('qty_available') or 0.0
                in_hand_qty = product_details.get('incoming_qty') or 0.0
                out_going_qty = product_details.get('outgoing_qty') or 0.0

                vals = {
                    'stock_location_id': a.id,
                    'on_hand_qty': on_hand.get(pro.id, 0.0),
                    'incoming_qty': incoming.get(pro.id, 0.0),
                    'out_qty': outgoing.get(pro.id, 0.0),
                    'custom_product_id': pro.id,
                    'forcasted_qty': (on_hand.get(pro.id, 0.0)) + (
                                incoming.get(pro.id, 0.0) - outgoing.get(pro.id, 0.0)),
                }

                search_record = self.env['stock.location.product'].search(
                    [('custom_product_id', '=', pro.id), ('stock_location_id', '=', a.id)])
                if search_record:
                    search_record = search_record[0]
                    search_record.write(vals)

                else:
                    res = self.env['stock.location.product'].create(vals)

    def update_the_stock_by_date(self):
        dict_pro = self._product_available()
        product_details = dict_pro.get(self.id)

        loc = self.env['stock.location'].search([('usage', '=', 'internal')])
        result = []
        created_ids = []
        for pro in self:
            for a in loc:

                domain_quant = [('product_id', '=', pro.id), ('location_id', '=', a.id)]
                domain_move_in = [('product_id', '=', pro.id), ('location_dest_id', '=', a.id)]
                domain_move_out = [('product_id', '=', pro.id), ('location_id', '=', a.id)]
                Move = self.env['stock.move']
                Quant = self.env['stock.quant']
                domain_move_in_todo = [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_move_in
                domain_move_out_todo = [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_move_out

                incoming = dict((item['product_id'][0], item['product_qty']) for item in
                                Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id']))
                outgoing = dict((item['product_id'][0], item['product_qty']) for item in
                                Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id']))
                on_hand = dict((item['product_id'][0], item['quantity']) for item in
                               Quant.read_group(domain_quant, ['product_id', 'quantity'], ['product_id']))

                on_hand_qty = product_details.get('qty_available') or 0.0
                in_hand_qty = product_details.get('incoming_qty') or 0.0
                out_going_qty = product_details.get('outgoing_qty') or 0.0

                vals = {
                    'stock_location_id': a.id,
                    'on_hand_qty': on_hand.get(pro.id, 0.0),
                    'incoming_qty': incoming.get(pro.id, 0.0),
                    'out_qty': outgoing.get(pro.id, 0.0),
                    'custom_product_id': pro.id,
                    'forcasted_qty': (on_hand.get(pro.id, 0.0)) + (
                                incoming.get(pro.id, 0.0) - outgoing.get(pro.id, 0.0)),
                }

                search_record = self.env['stock.location.product'].search(
                    [('custom_product_id', '=', pro.id), ('stock_location_id', '=', a.id)])
                if search_record:
                    search_record = search_record[0]
                    search_record.write(vals)

                else:
                    res = self.env['stock.location.product'].create(vals)


class Template(models.Model):
    _inherit = 'product.template'

    stock_location_template = fields.One2many('stock.location.product', 'custom_template_id', string="Stock Location", )

    def upate_compute_stock_location(self):

        loc = self.env['stock.location'].search([('usage', '=', 'internal')])
        for product_tmpl in self:
            variant_ids = []
            for product in product_tmpl.product_variant_ids:
                product.remove_filter()
                variant_ids.append(product.id)

            for l in loc:

                search_product_records = self.env['stock.location.product'].search(
                    [('custom_product_id', 'in', variant_ids), ('stock_location_id', '=', l.id)])
                total_on_hand_qty = 0.0
                total_forcasted_qty = 0.0
                total_incoming_qty = 0.0
                total_out_qty = 0.0
                for location_product in search_product_records:
                    total_on_hand_qty = total_on_hand_qty + location_product.on_hand_qty
                    total_forcasted_qty = total_forcasted_qty + location_product.forcasted_qty
                    total_incoming_qty = total_incoming_qty + location_product.incoming_qty
                    total_out_qty = total_out_qty + location_product.out_qty

                vals = {
                    'stock_location_id': l.id,
                    'on_hand_qty': total_on_hand_qty,
                    'incoming_qty': total_incoming_qty,
                    'out_qty': total_out_qty,
                    'custom_template_id': product_tmpl.id,
                    'forcasted_qty': total_forcasted_qty,

                }

                search_product_records = self.env['stock.location.product'].search(
                    [('custom_template_id', '=', product_tmpl.id), ('stock_location_id', '=', l.id)])
                if search_product_records:
                    search_product_records = search_product_records[0]
                    search_product_records.write(vals)
                else:
                    res = self.env['stock.location.product'].create(vals)
