# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _


class CapitalFundraisingWizard(models.TransientModel):
    _name = 'capital.fundraising.wizard'

    date_invoice = fields.Date(
        string='Invoice Date', required=True,
        default=fields.Date.context_today)

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner', required=True)

    share_qty = fields.Integer(string='Shares Quantity')

    category_id = fields.Many2one(
        comodel_name='capital.fundraising.category', string='Category',
        required=True)

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term', string='Payment Term',
        required=True)

    payment_journal_id = fields.Many2one(
        comodel_name='account.journal', string='Payment Method')

    @api.multi
    def button_confirm(self):
        invoice_obj = self.env['account.invoice']
        invoice_line_obj = self.env['account.invoice.line']
        wizard = self[0]
        product = wizard.category_id.product_id
        invoice_vals = invoice_obj.default_get(
            invoice_obj._fields.keys())
        invoice_line_vals = invoice_line_obj.default_get(
            invoice_line_obj._fields.keys())
        invoice_line_vals.update({
            'product_id': product.id,
            'account_id': product.property_account_income_id.id,
            'name': _('Capital Souscription'),
            'price_unit': wizard.category_id.fundraising_id.share_value,
            'quantity': wizard.share_qty,
        })
        invoice_vals.update({
            'type': 'out_invoice',
            'date_invoice': wizard.date_invoice,
            'journal_id': wizard.category_id.fundraising_id.journal_id.id,
            'account_id': wizard.category_id.partner_account_id.id,
            'payment_term_id': wizard.payment_term_id.id,
            'partner_id': wizard.partner_id.id,
            'is_capital_souscription': True,
            'fundraising_category_id': wizard.category_id.id,
            'invoice_line_ids': [[0, False, invoice_line_vals]],
        })

        # Create new invoice and validate
        invoice = invoice_obj.create(invoice_vals)
        invoice.onchange_fundraising_category_id()

#        invoice.invoice_validate()
        print invoice

        # Mark Payment

        return {'type': 'ir.actions.act_window_close'}
