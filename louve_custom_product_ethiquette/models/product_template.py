# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: Smile (<http://www.smile.fr>)
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Column Section
    rack_instruction = fields.Char(
        "Rack Instruction", help="""For example, the number of packages that
        should be stored on the rack""")
    rack_location = fields.Char(
        "Rack Location", help="""The name or place of the rack""")
    rack_number_of_packages = fields.Char(
        "Number of packages on the rack")
    origin = fields.Char(
        "Origin", help="""Origin and/or producer""")
    farming_method = fields.Char(
        "Farming Method", help="""Organic Label""")
    other_information = fields.Char("Other Information")
