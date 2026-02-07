FIFO Auto Reconciliation – Odoo 18

Overview

This module automatically reconciles posted invoices and payments using the FIFO (First-In, First-Out) accounting principle based on invoice date.

It works for both:

Accounts Receivable (Customer Invoices)
Accounts Payable (Vendor Bills)

Reconciliation is executed via a configurable scheduled action (cron job) and fully relies on Odoo’s native accounting engine, ensuring audit safety and accounting correctness.