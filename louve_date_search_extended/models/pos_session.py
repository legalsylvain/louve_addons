# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models


class PosSession(models.Model):
    _name = 'pos.session'
    _inherit = ['pos.session', 'date.search.mixin']

    _SEARCH_DATE_FIELD = 'start_at'
