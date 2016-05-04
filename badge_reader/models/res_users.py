# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Exist because has_group function is not correctly decorated.
    @api.multi
    def check_group(self, group_ext_id):
        return self.has_group(group_ext_id)

    # Compute Section
    @api.multi
    def log_move(self):
        user_move_obj = self.env['res.users.move']
        for user in self:
            user_move_obj.create({
                'user_id': user.id,
                'state': user.partner_id.state,
                'bootstrap_state': user.partner_id.bootstrap_state,
            })
        return True
