Subscription Form
=================

Usage
------------

This module has comprehensive subscription management system for wood pellet sales is established, with automated payment processing every month, with customer history tracking, and company-specific configurations.

Development
------------

* Added system parameter for execute payment.
* Created new model subscription.wood.pellet and added fields and view.
* Added schedule action 'Generate payments each month' for subscription.wood.pellet.
* Added fields Custom Comments On Invoice,Custom Comments On Sale,EDF Prime,Second Contact in company.
* Added commission report

Dependencies
------------

* **sale_timeline**:
   Adds timeline views for a visual representation of subscription statuses and activities.

* **amb_account**:
   Extends accounting capabilities for advanced payment and reporting needs in subscriptions.

