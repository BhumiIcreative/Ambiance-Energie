Amb Account
============

- Added some fields in the invoice like 'client situation' , 'type invoice'.
Type Invoice
1) Standard : This is the default invoice type used for regular transactions.
2) Granule  : This invoice type is specifically designed for customers purchasing wood pellets.
                    Blocks posting invoices if the invoice amount exceeds the subscription balance.
- Automatically registers payments for granule invoices using the subscription balance.
- Links invoices to the customer's current wood pellet subscription. And it is visible when select the invoice type Granule.
- The module has the 3 reports changes and new one also : invoice, invoice without payment, and account pieces