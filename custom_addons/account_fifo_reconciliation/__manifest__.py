{
    "name": "FIFO Auto Reconciliation (AR/AP)",
    "version": "1.0.0",
    "category": "Accounting",
    "summary": "Automatically reconcile invoices and payments using FIFO logic",
    "description": """
Automatically reconciles posted customer invoices and vendor bills with payments
using FIFO (First-In, First-Out) based on invoice date.
Runs via configurable scheduled action and respects all Odoo accounting rules.
    """,
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "data/fifo_reconcile_cron.xml",
    ],
    "installable": True,
    "application": False,
}
