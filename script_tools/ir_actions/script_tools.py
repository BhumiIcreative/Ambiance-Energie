# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class ScriptTools(models.TransientModel):
    _inherit = "script.tools"

    def open_record(self, record_id, name="", target="current", context=None):
        """
        Opens a single record in a window view.

        :param record_id: The ID of the record to be opened. It should be a single record ID.
        :param name: (optional) The name to display in the window. Defaults to the record's model name if not provided.
        :param target: (optional) The target for the window ('current', 'new', or 'inline'). Defaults to 'current'.
        :param context: (optional) The context to pass to the window. Defaults to an empty dictionary if not provided.
        :return: A dictionary containing the action for opening the record.
        """

        # Set default value for context if not provided
        if context is None:
            context = {}

        # If the provided record_id represents multiple records, delegate to open_records method
        if len(record_id) != 1:
            return self.open_records(
                record_id, name=name, target=target, context=context
            )

        # Return action dictionary for opening a single record
        return {
            "type": "ir.actions.act_window",
            "name": name or record_id._name,
            "res_model": record_id._name,
            "views": [(False, "form")],
            "res_id": record_id.id,
            "target": target,
            "context": context,
        }

    def open_records(
        self,
        record_ids,
        name="",
        target="current",
        context=None,
        views=None,
        domain=None,
        force_multi=False,
    ):
        """
        Opens a record or a set of records in a window view.

        :param record_ids: A record set or a list of record IDs to be opened.
        :param name: (optional) The name to display in the window. Defaults to the model name if not provided.
        :param target: (optional) The target for the window ('current', 'new', or 'inline'). Defaults to 'current'.
        :param context: (optional) The context to pass to the window. Defaults to an empty dictionary if not provided.
        :param views: (optional) List of views to use for the records. Defaults to ['tree', 'form'].
        :param domain: (optional) Domain filter for the records. Defaults to the record IDs if not provided.
        :param force_multi: (optional) If True, forces opening multiple records even if only one is provided. Defaults to False.
        :return: A dictionary containing the action for opening the records.
        """
        # Set default values for optional parameters if they are not provided
        if context is None:
            context = {}
        if views is None:
            views = ["tree", "form"]
        if domain is None:
            domain = [("id", "in", record_ids.ids)]
        # If only one record is provided and force_multi is False, call open_record method
        if len(record_ids) == 1 and not force_multi:
            return self.open_record(
                record_ids, name=name, target=target, context=context
            )
        # Return action dictionary for opening records
        return {
            "type": "ir.actions.act_window",
            "name": name or record_ids._name,
            "res_model": record_ids._name,
            "views": [(False, view) for view in views],
            "domain": domain,
            "target": target,
            "context": context,
        }

    def open_wizard(self, wizard_id, name="", target="new", context=None):
        """
        Opens a wizard record in a new window.

        :param wizard_id: The ID of the wizard record to be opened.
        :param name: (optional) The name to display in the window. Defaults to an empty string if not provided.
        :param target: (optional) The target for the window ('current', 'new', or 'inline'). Defaults to 'new'.
        :param context: (optional) The context to pass to the window. Defaults to an empty dictionary if not provided.
        :return: The result of the `open_record` method call, which contains the action to open the wizard.
        """

        # Set default value for context if not provided
        if context is None:
            context = {}
        return self.open_record(wizard_id, name=name, target=target, context=context)
