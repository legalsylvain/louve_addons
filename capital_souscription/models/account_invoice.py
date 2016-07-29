# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, exceptions, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    is_capital_souscription = fields.Boolean(
        string='Is Capital Souscription Invoice')

    fundraising_category_id = fields.Many2one(
        comodel_name='capital.fundraising.category',
        string='Fundraising Category')

    @api.model
    def create(self, vals):
        print vals
        return super(AccountInvoice, self).create(vals)

    @api.one
    @api.constrains(
        'is_capital_souscription', 'fundraising_category_id',
        'partner_id', 'invoice_line_ids')
    def _check_capital_souscription(self):
        invoice = self
        if invoice.is_capital_souscription:
            # Check mandatory field
            if not invoice.fundraising_category_id:
                raise exceptions.UserError(_(
                    "A Capital souscription must have a capital category"
                    " defined"))

            # Check products
            product_ids = invoice.invoice_line_ids.mapped('product_id.id')
            forbidden_product_ids =\
                list(set(product_ids) - set(
                    [invoice.fundraising_category_id.product_id.id]))
            if forbidden_product_ids:
                forbidden_products = self.env['product.product'].browse(
                    forbidden_product_ids)
                raise exceptions.UserError(_(
                    "%s category do not allow %s products") % (
                    invoice.fundraising_category_id.name, ', '.join(
                        forbidden_products.mapped('name'))))

            # check minimum qty
            minimum_qty =\
                invoice.fundraising_category_id.minimum_share_qty
            if invoice.partner_id.fundraising_type_id:
                for line in invoice.fundraising_category_id.line_ids:
                    if line.fundraising_type_id.id ==\
                            invoice.partner_id.fundraising_type_id.id:
                        minimum_qty = line.minimum_share_qty
            current_qty = sum(invoice.invoice_line_ids.mapped('quantity'))
            if current_qty < minimum_qty:
                raise exceptions.UserError(_(
                    "This category requires at least %d shares.") % (
                    minimum_qty))

    @api.onchange('fundraising_category_id')
    def onchange_fundraising_category_id(self):
        if self.fundraising_category_id:
            self.journal_id = \
                self.fundraising_category_id.fundraising_id.journal_id
            if self.fundraising_category_id.partner_account_id:
                self.account_id =\
                    self.fundraising_category_id.partner_account_id
