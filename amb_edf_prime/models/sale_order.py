from odoo import api, models

import logging

log = logging.getLogger(__name__).info


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "abstract.edf.prime.input"]

    @api.depends("amount_total", "type_order", "edf_prime")
    def _compute_amount_left_to_pay(self):
        """
        Computes the amount left to pay for the sale order.

        Overrides the default computation to account for the EDF Prime value.
        If the order type is "sto," the EDF Prime is subtracted from the
        amount left to pay.

        Dependent fields:
            - `amount_total`
            - `type_order`
            - `edf_prime`
        """
        super()._compute_amount_left_to_pay()
        for sale_id in self:
            if sale_id.type_order == "sto":
                sale_id.amount_left_to_pay -= sale_id.edf_prime

    @api.depends(
        "amount_total", "payment_timeline_ids", "advance", "edf_prime"
    )
    def _compute_amount_missing_from_timeline(self):
        """
        Computes the amount missing from the payment timeline.

        Overrides the default computation to adjust for the EDF Prime value.
        If the order type is "sto," the EDF Prime is subtracted from the
        amount missing from the timeline.

        Dependent fields:
            - `amount_total`
            - `payment_timeline_ids`
            - `advance`
            - `edf_prime`
        """
        super()._compute_amount_missing_from_timeline()
        for sale in self:
            if sale.type_order == "sto":
                sale.amount_missing_from_timeline -= sale.edf_prime

    def action_confirm(self):
        """
        Confirms the sale order and locks the EDF Prime.

        Before confirming the order, this method sets the `edf_prime_locked`
        field to True, ensuring that the EDF Prime can no longer be modified.
        """
        for sale_id in self:
            sale_id.edf_prime_locked = True
        return super().action_confirm()

    def action_cancel(self):
        """
        Cancels the sale order and unlocks the EDF Prime.

        Before canceling the order, this method sets the `edf_prime_locked`
        field to False, allowing the EDF Prime to be modified again.
        """
        for sale_id in self:
            sale_id.edf_prime_locked = False
        return super().action_cancel()

    def _prepare_invoice(self):
        """
        Prepares the invoice values for the sale order.

        Adds the EDF Prime value to the invoice if the order type is "sto."

        Returns:
            dict: A dictionary of values for creating the invoice.
        """
        res = super()._prepare_invoice()
        if self.type_order == "sto":
            res["edf_prime"] = self.edf_prime
        return res
