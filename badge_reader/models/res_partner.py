# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api

# TODO Set exhaustive state
_BADGE_PARTNER_STATE = [
    ('ok', 'OK'),
    ('membership_problem', 'Membership Problem'),
    ('work_problem', 'Work Problem'),
]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Column Section
    bootstrap_state = fields.Char(
        compute='_compute_bootstrap_state', string='Bootstrap State',
        store=True)

    state = fields.Selection(
        selection=_BADGE_PARTNER_STATE, state='state', default='ok')

    # Compute Section
    @api.multi
    @api.depends('state')
    def _compute_bootstrap_state(self):
        for partner in self:
            if partner.state == 'work_problem':
                partner.bootstrap_state = 'danger'
            elif partner.state == 'membership_problem':
                partner.bootstrap_state = 'warning'
            elif partner.state == 'ok':
                partner.bootstrap_state = 'success'

