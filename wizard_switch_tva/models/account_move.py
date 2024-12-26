# -*- coding: utf-8 -*-

from odoo import models, _


class SaleOrderLine(models.Model):
    _inherit = 'account.move'

    def action_switch_tva(self):
        """Opens the 'Switch TVA Wizard' form view with default taxes
           pre-filled from invoice lines.
        """
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': _('switch tva wizard'),
            'view_mode': 'form',
            'res_model': 'switch.tva.wizard',
            'context': {'default_first_tva': self.invoice_line_ids.mapped('tax_ids').ids},
        }
