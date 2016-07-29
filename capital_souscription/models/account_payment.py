# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    capital_move_id = fields.Many2one(
        comodel_name='account.move', string='Capital Account Move',
        readonly=True)

    @api.multi
    def write(self, vals):
        account_move_obj = self.env['account.move']
        if vals.get('state', False) == 'reconciled':
            for payment in self:
                if payment.state != 'reconciled':
                    # Generate Capital account move capital_move_id
                    # TODO
                    pass
        elif vals.get('state', False) in ['sent', 'posted']:
            for payment in self:
                if payment.state == 'reconciled':
                    # Cancel Capital account move capital_move_id
                    # TODO
                    pass
        return super(AccountPayment, self).write(vals)
