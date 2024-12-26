# wizard_switch_tva

# sale.order

# usage

- The sale.order model has been inherited to add a new button called Switch TVA. This button is visible only when the sale order is in draft or sent states.
- When clicked, the button opens the Switch TVA Wizard.
- The wizard is pre-filled with the current tax applied to the order lines, and the user can select a new TVA to apply to the order lines.

# account.move

# usage

- The account.move model (used for invoices) also includes a Switch TVA button, which functions similarly to the one in the sales order form.
- The button is displayed only when the invoice is in draft or sent states.
- When clicked, the button opens the Switch TVA Wizard, pre-filled with the current TVA applied to the invoice lines.
- The user can select a new TVA to apply to the invoice lines.


# switch.tva.wizard 

# usage

- This is a transient model that opens as a wizard for the user to switch the TVA (tax) on a sale order or invoice.
- It contains two fields:
  - first_tva: The current TVA (pre-filled based on the active record).
  - second_tva: The new TVA to be applied.
- The wizard is triggered from both the sale.order and account.move models.
- It allows the user to choose a new TVA and apply it to the relevant order lines or invoice lines.
