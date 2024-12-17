# coding: utf-8
from odoo import api, fields, models, _, SUPERUSER_ID

import logging
log = logging.getLogger(__name__).info


class SwitchTvaWizard(models.TransientModel):
    _name = 'switch.tva.wizard'
    _description = _('Switch tva wizard')

    @api.model
    def default_get(self, fields):
        res = super(SwitchTvaWizard, self).default_get(fields)
        return res

    def get_domain(self):
        domain = []
        active_id = self._context.get('active_id', [])
        active_model = self.env.context.get('active_model')

        tax_ids = []
        if active_model == 'sale.order':
            active_order = self.env['sale.order'].browse(active_id)
            for line in active_order.order_line:
                tax_ids += line.tax_id.mapped('id')
        elif active_model == 'account.move':
            active_invoice = self.env['account.move'].browse(active_id)
            for line in active_invoice.invoice_line_ids:
                tax_ids += line.tax_ids.mapped('id')

        domain += [('id', 'in', tax_ids)]
        return domain

    name = fields.Char(_('Name'))
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    first_tva = fields.Many2one('account.tax', string=_('First tva'), required=True, domain=lambda self: self.get_domain())
    second_tva = fields.Many2one('account.tax', string=_('Second tva'), required=True, domain=[('type_tax_use', '=', 'sale')])

    def _get_target_ids(self, active_record):
        active_model = self.env.context.get('active_model')
        if active_model =='sale.order':
            target_ids = active_record.order_line.filtered(lambda x: self.first_tva.id in x.tax_id.mapped('id'))

        if active_model =='account.move':
            target_ids = active_record.invoice_line_ids.filtered(lambda x: self.first_tva.id in x.tax_ids.mapped('id'))
        return target_ids

    def button_confirm(self):
        active_id = self._context.get('active_id', [])
        active_model = self.env.context.get('active_model')
        active_record = self.env[active_model].browse(active_id)
        target_ids = self._get_target_ids(active_record)

        tax_ids = [(6, 0, [self.second_tva.id])]
        if active_model == 'sale.order':
            target_ids.tax_id = tax_ids

        if active_model == 'account.move':
            target_ids.with_context(check_move_validity=False).write({'tax_ids': tax_ids})

            target_ids.with_context(check_move_validity=False)._onchange_price_subtotal()
            target_ids.with_context(check_move_validity=False)._onchange_mark_recompute_taxes()
            target_ids.with_context(check_move_validity=False).move_id._recompute_dynamic_lines(True)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',
        }