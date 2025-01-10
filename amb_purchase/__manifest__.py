# coding: utf-8
{
    "name": "Amb purchase",
    "summary": "Amb purchase",
    "description": "Amb purchase",
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    "category": "purchase",
    "version": "17.0.1.0.0",
    "application": True,
    "depends": [
        "base",
        "purchase",
        "account",
        "oci_point_of_sale",
    ],
    "data": [
        "datas/report_paperformat.xml",
        "report/custom_external_layout.xml",
        "report/custom_report_purchaseorder.xml",
        "report/custom_report_purchasequotation.xml",
        "views/purchase_views.xml",
    ],
    "license": "LGPL-3",
}
