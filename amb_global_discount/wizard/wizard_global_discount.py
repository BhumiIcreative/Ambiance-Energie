# coding: utf-8

from odoo import models, fields
from odoo.exceptions import UserError
import logging
log = logging.getLogger(__name__).info



class WizardGlobalDiscount(models.TransientModel):
    _name = 'wizard.global.discount'
    _inherit = 'script.wizard'

    global_discount = fields.Float('Remise %')
    res_model = fields.Char('Model')
    res_id = fields.Integer('Res id')

    def confirm(self):
        record_id = self.env[self.res_model].browse(self.res_id)
        if self.res_model == 'sale.order' or self.res_model =='purchase.order':
            for line in record_id.order_line:
                line.discount = self.global_discount
        if self.res_model =='account.move':
            for line in record_id.invoice_line_ids:
                line.with_context(check_move_validity=False).write({'discount': self.global_discount})
            record_id.invoice_line_ids.with_context(check_move_validity=False)._onchange_price_subtotal()
            record_id.invoice_line_ids.with_context(check_move_validity=False)._onchange_mark_recompute_taxes()
            record_id.invoice_line_ids.with_context(check_move_validity=False).move_id._recompute_dynamic_lines(True)
        record_id.global_discount = self.global_discount
        return True