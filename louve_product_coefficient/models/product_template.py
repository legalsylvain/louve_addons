# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: Smile (<http://www.smile.fr>)
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Column Section
    coeff1_id = fields.Many2one(
        comodel_name='product.coefficient', string='Loss Coefficient',
        related='categ_id.coeff1_id', readonly=True, store=True)
    coeff2_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 2',
        related='categ_id.coeff2_id', readonly=True, store=True)
    coeff3_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 3',
        related='categ_id.coeff3_id', readonly=True, store=True)
    coeff4_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 4',
        related='categ_id.coeff4_id', readonly=True, store=True)
    coeff5_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 5',
        related='categ_id.coeff5_id', readonly=True, store=True)
    coeff6_id = fields.Many2one(
        comodel_name='product.coefficient', string='Margin Coefficient',
        related='categ_id.coeff6_id', readonly=True, store=True)

    base_price = fields.Float(
        string='Base Price', compute='_compute_base_price', store=True,
        help="Base Price is the Sale Price of your Supplier.\n"
        "If product is sold by many suppliers, the first one is selected.\n"
        "If a supplier sell the product with different prices, the bigger"
        "    price is used."
        "If The supplier info belong an end date, the base price will be"
        " updated nightly, by a cron task.")

    coeff1_inter = fields.Float(
        string='With Loss Coefficient', compute='_compute_coeff1_inter',
        store=True)
    coeff2_inter = fields.Float(
        string='With Coefficient 2', compute='_compute_coeff2_inter',
        store=True)
    coeff3_inter = fields.Float(
        string='With Coefficient 3', compute='_compute_coeff3_inter',
        store=True)
    coeff4_inter = fields.Float(
        string='With Coefficient 4', compute='_compute_coeff4_inter',
        store=True)
    coeff5_inter = fields.Float(
        string='With Coefficient 5', compute='_compute_coeff5_inter',
        store=True)
    coeff6_inter = fields.Float(
        string='With Margin Coefficient', compute='_compute_coeff6_inter',
        store=True)

    theoritical_price = fields.Float(
        string='Theoritical Price', compute='_compute_theoritical_price',
        store=True, digits=dp.get_precision('Product Price'))

    has_theoritical_price_different = fields.Boolean(
        string='Has Theoritical Price Different', store=True,
        compute='_compute_has_theoritical_price_different')

    # Custom Section
    @api.multi
    def recompute_base_price(self):
        self._compute_base_price()

    # Custom Section
    @api.multi
    def use_theoritical_price(self):
        for template in self:
            template.list_price = template.theoritical_price

    @api.model
    def cron_recompute_base_price(self):
        templates = self.search([])
        templates.recompute_base_price()

    # Compute Section
    @api.multi
    @api.depends('product_variant_ids', 'seller_ids.price')
    def _compute_base_price(self):
        product_obj = self.env['product.product']
        for template in self:
            base_price = 0.0
            if template.product_variant_ids:
                seller = product_obj._select_seller(
                    template.product_variant_ids[0])
                if seller:
                    base_price = seller.price
            template.base_price = base_price

    @api.multi
    @api.depends(
        'base_price', 'coeff1_id.operation_type', 'coeff1_id.value')
    def _compute_coeff1_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            template.coeff1_inter = coefficient_obj.compute_price(
                template.coeff1_id, template.base_price)

    @api.multi
    @api.depends(
        'coeff1_inter', 'coeff2_id.operation_type', 'coeff2_id.value')
    def _compute_coeff2_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            template.coeff2_inter = coefficient_obj.compute_price(
                template.coeff2_id, template.coeff1_inter)

    @api.multi
    @api.depends(
        'coeff2_inter', 'coeff3_id.operation_type', 'coeff3_id.value')
    def _compute_coeff3_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            template.coeff3_inter = coefficient_obj.compute_price(
                template.coeff3_id, template.coeff2_inter)

    @api.multi
    @api.depends(
        'coeff3_inter', 'coeff4_id.operation_type', 'coeff4_id.value')
    def _compute_coeff4_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            template.coeff4_inter = coefficient_obj.compute_price(
                template.coeff4_id, template.coeff3_inter)

    @api.multi
    @api.depends(
        'coeff4_inter', 'coeff5_id.operation_type', 'coeff5_id.value')
    def _compute_coeff5_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            template.coeff5_inter = coefficient_obj.compute_price(
                template.coeff5_id, template.coeff4_inter)

    @api.multi
    @api.depends(
        'coeff5_inter', 'coeff6_id.operation_type', 'coeff6_id.value')
    def _compute_coeff6_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            template.coeff6_inter = coefficient_obj.compute_price(
                template.coeff6_id, template.coeff5_inter)

    @api.multi
    @api.depends(
        'coeff6_inter', 'taxes_id.amount', 'taxes_id.price_include',
        'taxes_id.amount_type')
    def _compute_theoritical_price(self):
        for template in self:
            multi = 1
            for tax in template.taxes_id:
                if tax.amount_type != 'percent' or not tax.price_include:
                    raise exceptions.UserError(_(
                        "Unimplemented Feature\n"
                        "The Tax %s is not correctly set for computing"
                        " prices with coefficients for the product %s") % (
                        tax.name, template.name))
                multi *= 1 + (tax.amount / 100)
            template.theoritical_price = template.coeff6_inter * multi

    @api.multi
    @api.depends(
        'theoritical_price', 'list_price')
    def _compute_has_theoritical_price_different(self):
        for template in self:
            if template.theoritical_price and template.base_price:
                template.has_theoritical_price_different =\
                    template.list_price != template.theoritical_price
            else:
                template.has_theoritical_price_different = False
