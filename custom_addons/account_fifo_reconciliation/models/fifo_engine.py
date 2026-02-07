import logging
from odoo import models, api

_logger = logging.getLogger(__name__)


class AccountFifoReconciliationService(models.AbstractModel):
    """
    FIFO reconciliation logic.
    """

    _name = "account.fifo.reconciliation.service"
    _description = "FIFO Auto Reconciliation Service"

    @api.model
    def run_fifo_reconciliation(self):
        """
        PUBLIC ENTRY POINT (CALLED BY CRON).
        Iterates companies and processes partners incrementally.
        """
        companies = self.env["res.company"].search(
            [("fifo_auto_reconcile_enabled", "=", True)]
        )

        for company in companies:
            self._process_company(company)

    def _process_company(self, company):
        """
        Process FIFO reconciliation for a single company.
        """
        _logger.info("FIFO reconciliation started for company %s", company.name)
        domain = [
            ("company_id", "=", company.id),
            ("reconciled", "=", False),
            ("amount_residual", "!=", 0),
            ("move_id.state", "=", "posted"),
            ("account_id.account_type", "in", ["asset_receivable", "liability_payable"]),
        ]
        move_lines = (
            self.env["account.move.line"]
            .search(domain)
            .mapped("partner_id")
            .filtered(lambda p: p)
        )
        partners = move_lines[: company.fifo_max_partners_per_run]
        for partner in partners:
            try:
                if company.fifo_apply_customer:
                    self._process_partner_fifo(
                        company, partner, account_type="asset_receivable"
                    )

                if company.fifo_apply_vendor:
                    self._process_partner_fifo(
                        company, partner, account_type="liability_payable"
                    )
            except Exception as e:
                _logger.exception(
                    "FIFO reconciliation failed for partner %s (%s)",
                    partner.display_name,
                    str(e),
                )

    def _process_partner_fifo(self, company, partner, account_type):
        """
        Apply FIFO reconciliation for a single partner and account type.
        """
        invoices = self._get_fifo_invoices(company, partner, account_type)
        payments = self._get_fifo_payments(company, partner, account_type)
        if not invoices or not payments:
            return
        for payment in payments:
            remaining_payment = payment.amount_residual
            for invoice in invoices:
                if remaining_payment <= 0:
                    break
                if invoice.amount_residual <= 0:
                    continue
                amount = min(
                    remaining_payment,
                    invoice.amount_residual,
                )
                self._reconcile_lines(invoice, payment, amount)
                remaining_payment -= amount


    def _get_fifo_invoices(self, company, partner, account_type):
        """
        Oldest unpaid invoices/bills first (FIFO by invoice_date).
        """
        domain = [
            ("company_id", "=", company.id),
            ("partner_id", "=", partner.id),
            ("reconciled", "=", False),
            ("amount_residual", ">", 0),
            ("move_id.state", "=", "posted"),
            ("account_id.account_type", "=", account_type),
        ]
        return self.env["account.move.line"].search(
            domain,
            order="move_id.invoice_date asc, date asc, id asc",
        )

    def _get_fifo_payments(self, company, partner, account_type):
        """
        Oldest open payments first.
        """
        domain = [
            ("company_id", "=", company.id),
            ("partner_id", "=", partner.id),
            ("reconciled", "=", False),
            ("amount_residual", ">", 0),
            ("move_id.state", "=", "posted"),
            ("account_id.account_type", "=", account_type),
        ]

        return self.env["account.move.line"].search(
            domain,
            order="date asc, id asc",
        )

    def _reconcile_lines(self, invoice_line, payment_line, amount):
        """
        Delegate reconciliation to Odoo's native engine.
        """
        (invoice_line + payment_line).with_context(
            fifo_auto_reconcile=True
        ).reconcile()

        _logger.info(
            "FIFO reconciled %s between invoice %s and payment %s",
            amount,
            invoice_line.move_id.name,
            payment_line.move_id.name,
        )
