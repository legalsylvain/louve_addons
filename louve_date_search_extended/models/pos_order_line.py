# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields


class PosOrderLine(models.Model):
    _name = 'pos.order.line'
    _inherit = ['pos.order.line', 'date.search.mixin']

    date_order = fields.Datetime(
        string='Date Order', related='order_id.date_order', store=True)

    _SEARCH_DATE_FIELD = 'date_order'
