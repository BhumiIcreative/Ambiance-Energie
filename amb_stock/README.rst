Amb Stock
============

Usage
------------

* Saleable quantity: Available quantity minus the quantity that is not completed, where the location is the customer location.
* Net quantity: Available quantity plus the order quantity.
* Order Stock: Quantity of purchase orders that are in the "purchase" or "locked" state, minus the received quantity.

Development
------------

* Added Saleable quantity,Net quantity,Order Stock,Purchase order lines,Purchase order field in product template and variants for calculate quantity.
* Added Vendor field in transfers.
* Added Transfer voucher report in transfers.

Dependencies
------------

* The `script_tools` module is added as a dependency to utilize its functions.
