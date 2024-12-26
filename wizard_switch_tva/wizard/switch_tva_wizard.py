# -*- coding: utf-8 -*-
from odoo import fields, models, _


class SwitchTvaWizard(models.TransientModel):
    _name = 'switch.tva.wizard'
    _description = _('Switch tva wizard')

    name = fields.Char(_('Name'))
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    first_tva = fields.Many2one('account.tax', string=_('First tva'), required=True)
    second_tva = fields.Many2one('account.tax', string=_('Second tva'), required=True,
                                  domain=[('type_tax_use', '=', 'sale')])

    def _get_target_ids(self, active_record):
        """
        Returns the target lines based on the first TVA tax selection.
        """
        active_model = self.env.context.get('active_model')
        if active_model == 'sale.order':
            target_ids = active_record.order_line.filtered(
                lambda x: self.first_tva.id in x.tax_id.mapped('id'))
        elif active_model == 'account.move':
            target_ids = active_record.invoice_line_ids.filtered(
                lambda x: self.first_tva.id in x.tax_ids.mapped('id'))
        return target_ids

    def button_confirm(self):
        """
        Confirms the TVA switch by updating the tax ids on the selected lines.
        """
        active_model = self.env.context.get('active_model')
        active_record = self.env[active_model].browse(self._context.get('active_id', []))

        if active_model == 'sale.order':
            self._get_target_ids(active_record).tax_id = [(6, 0, [self.second_tva.id])]
        elif active_model == 'account.move':
            self._get_target_ids(active_record).with_context(
                check_move_validity=False).write({'tax_ids': [(6, 0, [self.second_tva.id])]})
            self._get_target_ids(active_record).with_context(
                check_move_validity=False)._compute_all_tax()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',
        }
