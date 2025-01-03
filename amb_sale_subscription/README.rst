Amb sale subscription
======================

Usage
---------------------

* In this module two fields are added in subscription form view and that values will be transfer to invoice.

Development
----------------------

* Added fields Point of sale and Payment method.
* Inherited _prepare_invoice and _create_recurring_invoice.

Dependencies
---------------------

* **amb_account**
    Used method _generate_invoice_rest_payments
* **sale_timeline**
    Model is used for reference for many2one.

