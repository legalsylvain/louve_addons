# -*- coding: utf-8 -*-

from openerp import fields, models, api


class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    default_consumption_calculation_method = fields.Selection([
        ('moves', 'Calculate consumption based on Stock Moves'),
        ('history', 'Calculate consumption based on the Product History'),
        ], 'Consumption Calculation Method', default='moves',
        default_model='product.template')
    default_number_of_periods = fields.Integer(
        'Number of valid history periods used for the calculation', default=6,
        default_model='product.template',
        help="""This field is used if the selected method is based on"""
        """ Product History""")
    default_calculation_range = fields.Integer(
        'Calculation Range in days', default=365,
        default_model='product.template', help="""This field is used if the"""
        """ selected method is based on Stock Moves."""
        """Number of days used for"""
        """ the calculation of the average consumption. For example: if you"""
        """ put 365, the calculation will be done on last year.""")
    default_display_range = fields.Integer(
        'Display Range in days', default=1,
        default_model='product.template', help="""Examples:
        1 -> Average Consumption per days
        7 -> Average Consumption per week
        30 -> Average Consumption per month""")
    module_product_history = fields.Boolean(
        "View product History",
        help="This will install product_history module")

    @api.onchange('default_consumption_calculation_method')
    def _onchange_default_consumption_calculation_method(self):
        if self.default_consumption_calculation_method == 'history':
            self.module_product_history = True

    @api.onchange('module_product_history')
    def _onchange_module_product_history(self):
        if self.module_product_history == False:
            self.default_consumption_calculation_method = 'moves'


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
