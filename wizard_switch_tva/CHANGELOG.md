# Switch Wizard TVA

# Changelog

All notable changes to this project will be documented in this file.

## [17.0.1.0.0] - 2024-12-16

## Modified
- Changed button type 'action' to 'object' due to active_id related issue in context in v-17.

### Changed
- Changed file name 'account_views.xml' to '[account_move_views.xml](views/account_move_views.xml)'.
- Changed file name 'sale_views.xml' to '[sale_order_views.xml](views/sale_order_views.xml)'.

### Removed
- Removed 'get_domain' method. 
- Removed states attribute which is no longer used in v-17.
- Removed unnecessary code.

### Added
- Added new py file [account_move.py](models/account_move.py).
- Added new py file [sale_order.py](models/sale_order.py).
- Added security file [ir.model.access.csv](security/ir.model.access.csv).
- Added README.md file [README.md](README.md).
- Added method doc strings.
- Followed py coding standards.


