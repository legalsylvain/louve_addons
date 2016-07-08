# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'date.search.mixin']

    _SEARCH_DATE_FIELD = 'date'
