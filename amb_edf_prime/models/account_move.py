from odoo import models,fields,_
import logging
log = logging.getLogger(__name__).info


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'abstract.edf.prime.input']

    type_invoice = fields.Selection(
        [
            ("std", _("Standard")),
            ("gran", _("Granule")),
            ("serv", _("Service")),
            ("sto", _("Stove")),
        ],
        string=_("Type invoice"),
        default="std",
    )

    def _prepare_move_line_with_product(self, product_id):
        ####################
        # VARIABLES EN DUR #
        if self.company_id.id == 1:      # AMBIANCE
            var_edf_prime_account_id = 45
        if self.company_id.id == 2:      # JLCP
            var_edf_prime_account_id = 45
        ####################

        move_line_vals = {
            'product_id': product_id.id,
            'name': 'PRIME CEE EDF',
            'quantity': 1,
            'price_unit': self.edf_prime,
            'account_id' : var_edf_prime_account_id,
        }

        return move_line_vals

    def _prepare_credit_note(self):
        move_reversal = self.env['account.move.reversal'].with_context(
            {'active_ids': [self.id], 'active_id': self.id, 'active_model': 'account.move'}).create(
            {
                'journal_id': self.journal_id.id,
                'reason': 'PRIME CEE EDF',
            })
        reversal = move_reversal.reverse_moves()
        reverse_move = self.env['account.move'].browse(reversal['res_id'])
        return reverse_move

    def _post_edf_prime(self):

        product_tmpl_id = self.env.ref('amb_edf_prime.product_edf_prime')
        product_id = product_tmpl_id.product_variant_id
        prime_move_line = self._prepare_move_line_with_product(product_id)

        bypass_context = dict(force_bypass_timeline=True, check_move_validity=False)
        self.with_context(**bypass_context).write({
            'invoice_line_ids': [(5, 0, 0)] + [(0, 0, prime_move_line)],
            'edf_prime': 0,
        })
        self.action_post()

    def action_post(self):
        res = super().action_post()
        if self.edf_prime and self.move_type == 'out_invoice': # Only for invoice client

            # Make a credit note
            reverse_move = self._prepare_credit_note()

            # replace invoice_line_ids by edf_prime line
            reverse_move._post_edf_prime()

        return res
