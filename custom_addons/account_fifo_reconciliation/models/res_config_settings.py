from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    fifo_auto_reconcile_enabled = fields.Boolean(
        related="company_id.fifo_auto_reconcile_enabled",
        readonly=False,
    )

    fifo_apply_customer = fields.Boolean(
        related="company_id.fifo_apply_customer",
        readonly=False,
    )

    fifo_apply_vendor = fields.Boolean(
        related="company_id.fifo_apply_vendor",
        readonly=False,
    )

    fifo_max_partners_per_run = fields.Integer(
        related="company_id.fifo_max_partners_per_run",
        readonly=False,
    )
