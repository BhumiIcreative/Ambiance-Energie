from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    pos_vendeur_id = fields.Many2one(
        "point.de.vente",
        string="Pos Seller",
        copy=False,
        readonly=True,
        ondelete="set null",
        related="user_id.point_de_vente_id",
    )
    oci_saleorder_yourref = fields.Char(string="Your Reference", copy=False)
    oci_saleorder_refcustomer = fields.Char(
        string="Customer Reference", copy=False, readonly=True, related="partner_id.ref"
    )
    field_pMXi2_id = fields.Many2one(
        "hr.employee", string="Employee", copy=False, ondelete="set null"
    )
    field_xAmex_ids = fields.Many2many(
        "hr.employee",
        "x_hr_employee_sale_order_rel",
        string="Employee",
        copy=False,
        ondelete="cascade",
    )
    oci_saleorder_technicien_id = fields.Many2one(
        "hr.employee", string="Technician", copy=False, ondelete="set null"
    )
    adresse = fields.Char(
        string="Address",
        copy=False,
        readonly=True,
        related="partner_id.contact_address",
    )
    modle_de_poele = fields.Char(
        string="Stove Model",
        copy=False,
        readonly=True,
        related="partner_id.modele_equipement_contact",
    )
    no_invoiced = fields.Monetary(
        string="Not Billed",
        copy=False,
        readonly=True,
        help="Difference including VAT between the order and the invoices",
        compute="_compute_no_invoiced",
    )

    oci_abo_date_prochaine_intervention = fields.Date(
        string="Next intervention date", copy=False
    )

    @api.depends("invoice_ids")
    def _compute_no_invoiced(self):
        for record in self:
            record["no_invoiced"] = record.amount_total - sum(
                record.invoice_ids.mapped(lambda x: x.amount_total_signed)
            )
