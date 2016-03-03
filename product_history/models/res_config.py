# -*- coding: utf-8 -*-

from openerp import fields, models


class ProductHistorySettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    default_history_range = fields.Selection([
        ('days', 'Days'),
        ('weeks', 'Week'),
        ('months', 'Month'),
        ], 'Product History Display Range', default='weeks',
        default_model='product.product')
