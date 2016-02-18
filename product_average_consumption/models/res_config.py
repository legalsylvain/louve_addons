# -*- coding: utf-8 -*-

from openerp import fields, models, api


class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    default_display_range = fields.Integer(
        'Display Range in days', default=1,
        default_model='product.template', help="""Examples:
        1 -> Average Consumption per days
        7 -> Average Consumption per week
        30 -> Average Consumption per month""")
    default_calculation_range = fields.Integer(
        'Calculation Range in days', default=365,
        default_model='product.template', help="""Number of days used for
        the calculation of the average consumption. For example: if you put
        365, the calculation will be done on last year.""")

    @api.onchange('default_display_range')
    @api.multi
    def _onchange_default_display_range(self):
        for config in self:
            self.env.cr.execute("""
                UPDATE product_template
                SET display_range=%i""" % (config.default_display_range))

    @api.onchange('default_calculation_range')
    @api.multi
    def _onchange_default_calculation_range(self):
        for config in self:
            self.env.cr.execute("""
                UPDATE product_template
                SET calculation_range=%i""" % (
                config.default_calculation_range))
