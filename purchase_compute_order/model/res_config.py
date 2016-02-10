# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'purchase.config.settings'

    default_valid_psi = fields.Selection([
        ('first', 'Consider only the first supplier on the product'),
        ('all', 'Consider all the suppliers registered on the product'),
        ], 'Supplier choice', default='first',
        default_model='purchase_compute_order.ComputedPurchaseOrder')
