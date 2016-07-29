# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_capital_souscription = fields.Boolean(
        string='Is a Capital Souscription Product', help=" Check this box"
        " if you want to use this product for capital souscription.\n"
        " If yes, please check accounting settings.")
