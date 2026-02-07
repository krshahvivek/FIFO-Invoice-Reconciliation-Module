from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    fifo_auto_reconcile_enabled = fields.Boolean(
        string="Enable FIFO Auto Reconciliation",
        default=False,
    )
    fifo_apply_customer = fields.Boolean(
        string="Apply to Customers (AR)",
        default=True,
    )
    fifo_apply_vendor = fields.Boolean(
        string="Apply to Vendors (AP)",
        default=True,
    )
    fifo_max_partners_per_run = fields.Integer(
        string="Max Partners Per Cron Run",
        default=50,
        help="Limits how many partners are processed per cron execution.",
    )
