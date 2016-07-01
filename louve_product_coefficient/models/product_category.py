# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: Smile (<http://www.smile.fr>)
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields

TYPE = [('multi', 'Multi'),
        ('amount', 'Amount')]


class ProductCategory(models.Model):
    _inherit = 'product.category'

    coeff1_id = fields.Many2one(
        comodel_name='product.coefficient', string='Loss Coefficient',
        domain="[('coefficient_type', '=', 'loss')]")
    coeff2_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 2',
        domain="[('coefficient_type', '=', 'custom')]")
    coeff3_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 3',
        domain="[('coefficient_type', '=', 'custom')]")
    coeff4_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 4',
        domain="[('coefficient_type', '=', 'custom')]")
    coeff5_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 5',
        domain="[('coefficient_type', '=', 'custom')]")
    coeff6_id = fields.Many2one(
        comodel_name='product.coefficient', string='Margin Coefficient',
        domain="[('coefficient_type', '=', 'margin')]")
