# -*- coding: utf-8 -*-

from odoo import models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order'

    def action_switch_tva(self):
        """ Opens the 'Switch TVA Wizard' form view with default taxes
            pre-filled from the order lines.
         """
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': _('switch tva wizard'),
            'view_mode': 'form',
            'res_model': 'switch.tva.wizard',
            'context': {'default_first_tva': self.order_line.mapped('tax_id').ids},
        }
