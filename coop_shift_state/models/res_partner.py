# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Cyril Gaspard
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
# from datetime import datetime
# from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    SHIFT_TYPE_SELECTION = [
        ('standard', 'Standard'),
        ('ftop', 'FTOP'),
    ]

    COOPERATIVE_STATE_SELECTION = [
        ('up_to_date', 'Up to date'),
        ('alert', 'Alert'),
        ('suspended', 'Suspended'),
        ('delay', 'Delay'),
        ('unsubscribed', 'Unsubscribed'),
        ('unpayed', 'Unpayed'),
        ('blocked', 'Blocked'),
    ]

    is_unpayed = fields.Boolean('Unpayed')

    is_blocked = fields.Boolean('Blocked')

    shift_type = fields.Selection(
        selection=SHIFT_TYPE_SELECTION, string='Shift type', required=True,
        default='standard')

    cooperative_state = fields.Selection(
        selection=COOPERATIVE_STATE_SELECTION, string='State',
        compute='compute_cooperative_state')

    theoritical_standard_point = fields.Integer(
        string='theoritical Standard points', store=True,
        compute='compute_theoritical_standard_point')

    manual_standard_correction = fields.Integer(
        string='Manual Standard Correction')

    final_standard_point = fields.Integer(
        string='Final Standard points',compute='compute_final_standard_point',
        store=True)

    theoritical_ftop_point = fields.Integer(
        string='theoritical FTOP points', store=True,
        compute='compute_theoritical_ftop_point')

    manual_ftop_correction = fields.Integer(
        string='Manual FTOP Correction')

    final_ftop_point = fields.Integer(
        string='Final FTOP points',compute='compute_final_ftop_point',
        store=True)

    # Compute Section
    @api.depends('theoritical_standard_point', 'manual_standard_correction')
    @api.multi
    def compute_final_standard_point(self):
        for partner in self:
            partner.final_standard_point =\
                partner.theoritical_standard_point +\
                partner.manual_standard_correction

    @api.depends('theoritical_ftop_point', 'manual_ftop_correction')
    @api.multi
    def compute_final_ftop_point(self):
        for partner in self:
            partner.final_ftop_point =\
                partner.theoritical_ftop_point +\
                partner.manual_ftop_correction

    @api.depends(
        'registration_ids.state', 'registration_ids.shift_type')
    @api.multi
    def compute_theoritical_standard_point(self):
        for partner in self:
            point = 0
            for registration in partner.registration_ids.filtered(
                        lambda reg: reg.shift_type == 'standard'):
                if not registration.template_created:
                    if registration.state in ['done', 'replaced']:
                        point += +1
                # In all cases
                if registration.state in ['absent']:
                    point += -2
                elif registration.state in ['excused', 'waiting']:
                    point += -1
            partner.theoritical_standard_point = point

    @api.depends('registration_ids.state', 'registration_ids.shift_type')
    @api.multi
    def compute_theoritical_ftop_point(self):
        for partner in self:
            point = 0
            for registration in partner.registration_ids.filtered(
                        lambda reg: reg.shift_type == 'ftop'):
                if registration.template_created:
                    # The presence was forcasted
                    if registration.state in ['absent', 'excused', 'waiting']:
                        point += -1
                else:
                    if registration.state in ['absent']:
                        point += -1
                    elif registration.state in ['present']:
                        point += 1
            partner.theoritical_ftop_point = point

    @api.depends(
        'is_blocked', 'is_unpayed', 'final_standard_point', 'final_ftop_point',
        'shift_type')
    @api.multi
    def compute_cooperative_state(self):
        for partner in self:
            state = 'up_to_date'
            if partner.is_blocked:
                state = 'blocked'
            elif partner.is_unpayed:
                state = 'unpayed'
            else:
                point = partner.shift_type == 'standard'\
                    and partner.final_standard_point\
                    or partner.final_ftop_point
                if point < 0:
                    pass
            partner.cooperative_state = state
