{
    "name": "Amb sale subscription",
    "summary": "Amb sale subscription",
    "description": """ Ajouter oci_point_of_sale, payment_instrument_id sur des abonnements,
    Générer les factures et reprendre les info des champs,
    Lancer automatiquement la création des paiements après la création de facture
    """,
    "author": "Aktiv software / Groupe OCI",
    "website": "http://www.aktivsoftware.com / https://www.oci.fr",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["amb_sale", "sale_subscription", "sale_timeline"],
    "data": [
        "views/sale_subscription_views.xml",
    ],
}
