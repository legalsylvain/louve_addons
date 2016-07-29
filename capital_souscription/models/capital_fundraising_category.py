# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class CapitalFundraisingCategory(models.Model):
    _name = 'capital.fundraising.category'

    name = fields.Char(string='Name')

    fundraising_id = fields.Many2one(
        comodel_name='capital.fundraising', string='Fundraising',
        required=True, ondelete='cascade', index=True, copy=False)

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        related='fundraising_id.company_id', store=True, readonly=True)

    manual_admission = fields.Boolean(
        string='Manual Admission', help="Check this box if partner must"
        " be accepted by General Assembly before having the possibility"
        " to buy shares")

    product_id = fields.Many2one(
        comodel_name='product.product', string='Products', required=True,
        domain="[('is_capital_souscription', '=', True)]")

    partner_account_id = fields.Many2one(
        comodel_name='account.account', string='Partner Account',
        domain="[('internal_type', '=', 'payable'),"
        "('deprecated', '=', False)]", help="This account will be used"
        " instead of the default partner one, if defined.")

    capital_account_id = fields.Many2one(
        comodel_name='account.account', string='Final Capital Account',
        domain="[('internal_type', '=', 'other'),"
        "('deprecated', '=', False)]", help="This account will be used"
        " to write a move between default product account and capital account"
        " when the payment is done.")

    minimum_share_qty = fields.Integer(
        string='Minimum Share Quantity', required=True, default=1)

    line_ids = fields.One2many(
        comodel_name='capital.fundraising.category.line', string='Lines',
        inverse_name='fundraising_category_id')
