from odoo import api, fields, models, _


class SwitchTvaWizard(models.TransientModel):
    _name = "switch.tva.wizard"
    _description = _("Switch tva wizard")

    name = fields.Char(string="Name")
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )
    first_tva = fields.Many2one("account.tax", string="First Tva", required=True)
    second_tva = fields.Many2one(
        "account.tax",
        string="Second Tva",
        required=True,
        domain=[("type_tax_use", "=", "sale")],
    )

    @api.model
    def default_get(self, fields):
        """Default method to set 'first_tva' field based on tax IDs from 'sale.order' or 'account.move'."""
        res = super(SwitchTvaWizard, self).default_get(fields)
        active_id = self._context.get("active_id", [])
        active_model = self.env.context.get("active_model")
        if active_model in ["sale.order", "account.move"]:
            model = self.env[active_model].browse(active_id)
            line_field = (
                "order_line" if active_model == "sale.order" else "invoice_line_ids"
            )
            tax_ids = model[line_field].mapped(
                "tax_id.id" if active_model == "sale.order" else "tax_ids.id"
            )
            res.update({"first_tva": self.env["account.tax"].browse(tax_ids)})
        return res

    def _get_target_ids(self, active_record):
        """Filter target records based on the active model ('sale.order' or 'account.move') and their tax IDs"""
        active_model = self.env.context.get("active_model")
        if active_model in ["sale.order", "account.move"]:
            return (
                active_record.order_line.filtered(
                    lambda x: self.first_tva.id in x.tax_id.ids
                )
                if active_model == "sale.order"
                else active_record.invoice_line_ids.filtered(
                    lambda x: self.first_tva.id in x.tax_ids.ids
                )
            )

    def button_confirm(self):
        """Update tax IDs for the model ('sale.order' or 'account.move') and reload the client context"""
        active_model = self.env.context.get("active_model")
        target_ids = self._get_target_ids(
            self.env[active_model].browse(self._context.get("active_id", []))
        )
        tax_ids = [(6, 0, [self.second_tva.id])]
        if active_model == "sale.order":
            target_ids.write({"tax_id": tax_ids})
        elif active_model == "account.move":
            target_ids.with_context(check_move_validity=False).write(
                {"tax_ids": tax_ids}
            )
        return {
            "type": "ir.actions.client",
            "tag": "reload_context",
        }
