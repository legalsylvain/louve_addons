# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class CapitalFundraisingWizard(models.TransientModel):
    _inherit = 'capital.fundraising.wizard'

    def default_can_change_fundraising_category(self):
        return self.user_has_groups(
            'louve_membership.subscriptions_can_change_fundraising_category')

    def default_payment_term_id(self):
        return self.env.ref('account.account_payment_term_immediate').id

    def default_category_id(self):
        return self.env.ref(
            'louve_membership.capital_fundraising_category_A').id

    # Column Section
    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term', default=default_payment_term_id)

    category_id = fields.Many2one(
        comodel_name='capital.fundraising.category',
        default=default_category_id)

    can_change_fundraising_category = fields.Boolean(
        string="Can Change fundraising Category",
        default=default_can_change_fundraising_category)
