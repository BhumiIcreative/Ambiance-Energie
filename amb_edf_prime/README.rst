Amb EDF Prime
============

Usage
------------

* Use the Prime Management Wizard to update the prime amount in the sales order.
* Confirm the sales order to lock the prime amount, preventing further changes.
* Invoices with EDF Primes automatically generate a credit note upon posting.

Dependencies
------------

* The `amb_sale` module is added as a dependency to utilize its fields in managing the prime amount workflow.
* The `amb_account` module is added as a dependency to utilize its fields in managing the prime amount workflow.
* The `script_tools` module is added as a dependency to utilize its functions.