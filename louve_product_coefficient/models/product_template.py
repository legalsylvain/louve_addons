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
        comodel_name='product.coefficient', string='Supplier Coefficient',
        domain="[('coefficient_type', '=', 'supplier')]")
    coeff2_id = fields.Many2one(
        comodel_name='product.coefficient', string='Shipping Coefficient',
        domain="[('coefficient_type', '=', 'shipping')]")
    coeff3_id = fields.Many2one(
        comodel_name='product.coefficient', string='Loss Coefficient',
        domain="[('coefficient_type', '=', 'loss')]")
    coeff4_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 4',
        domain="[('coefficient_type', '=', 'custom')]")
    coeff5_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 5',
        domain="[('coefficient_type', '=', 'custom')]")
    coeff6_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 6',
        domain="[('coefficient_type', '=', 'custom')]")
    coeff7_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 7',
        domain="[('coefficient_type', '=', 'custom')]")
    coeff8_id = fields.Many2one(
        comodel_name='product.coefficient', string='Coefficient 8',
        domain="[('coefficient_type', '=', 'custom')]")
    coeff9_id = fields.Many2one(
        comodel_name='product.coefficient', string='Margin Coefficient',
        domain="[('coefficient_type', '=', 'margin')]")

    base_price = fields.Float(
        string='Base Price', compute='_compute_base_price', store=True,
        help="Base Price is the Sale Price of your Supplier.\n"
        "If product is sold by many suppliers, the first one is selected.\n"
        "If a supplier sell the product with different prices, the bigger"
        " price is used.\n\n"
        "If The supplier info belong an end date, the base price will be"
        " updated nightly, by a cron task.")

    alternative_base_price = fields.Float(
        string='Alternative Base Price',
        help="This alternative base price will be used instead of the Base"
        " Price, if defined.")

    coeff1_inter = fields.Float(
        string='With Supplier Discount Coefficient',
        compute='_compute_coeff1_inter', store=True)
    coeff2_inter = fields.Float(
        string='With Shipping Coefficient', compute='_compute_coeff2_inter',
        store=True)
    coeff3_inter = fields.Float(
        string='With Loss Coefficient', compute='_compute_coeff3_inter',
        store=True)
    coeff4_inter = fields.Float(
        string='With Coefficient 4', compute='_compute_coeff4_inter',
        store=True)
    coeff5_inter = fields.Float(
        string='With Coefficient 5', compute='_compute_coeff5_inter',
        store=True)
    coeff6_inter = fields.Float(
        string='With Coefficient 6', compute='_compute_coeff6_inter',
        store=True)
    coeff7_inter = fields.Float(
        string='With Coefficient 7', compute='_compute_coeff7_inter',
        store=True)
    coeff8_inter = fields.Float(
        string='With Coefficient 8', compute='_compute_coeff8_inter',
        store=True)
    coeff9_inter = fields.Float(
        string='With Margin Coefficient', compute='_compute_coeff9_inter',
        store=True)

    theoritical_price = fields.Float(
        string='Theoritical Price VAT Incl.',
        compute='_compute_theoritical_price', store=True,
        digits=dp.get_precision('Product Price'))

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
    @api.depends(
        'product_variant_ids', 'uom_id', 'uom_po_id', 'seller_ids.price',
        'seller_ids.product_uom')
    def _compute_base_price(self):
        # TODO IMPME. Compute with discount, depending on
        # product_supplierinfo_discount
        product_obj = self.env['product.product']
        for template in self:
            base_price = 0.0
            if template.product_variant_ids:
                seller = product_obj._select_seller(
                    template.product_variant_ids[0])
                if seller:
                    if seller.product_uom.id == template.uom_id.id:
                        base_price = seller.price
                    else:
                        base_price = ((
                            seller.price /
                            seller.product_uom.factor_inv) *
                            template.uom_id.factor_inv)
            template.base_price = base_price

    @api.multi
    @api.depends(
        'alternative_base_price', 'base_price', 'coeff1_id.operation_type',
        'coeff1_id.value')
    def _compute_coeff1_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            if template.alternative_base_price:
                template.coeff1_inter = coefficient_obj.compute_price(
                    template.coeff1_id, template.alternative_base_price)
            else:
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
        'coeff6_inter', 'coeff7_id.operation_type', 'coeff7_id.value')
    def _compute_coeff7_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            template.coeff7_inter = coefficient_obj.compute_price(
                template.coeff7_id, template.coeff6_inter)

    @api.multi
    @api.depends(
        'coeff7_inter', 'coeff8_id.operation_type', 'coeff8_id.value')
    def _compute_coeff8_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            template.coeff8_inter = coefficient_obj.compute_price(
                template.coeff8_id, template.coeff7_inter)

    @api.multi
    @api.depends(
        'coeff8_inter', 'coeff9_id.operation_type', 'coeff9_id.value')
    def _compute_coeff9_inter(self):
        coefficient_obj = self.env['product.coefficient']
        for template in self:
            template.coeff9_inter = coefficient_obj.compute_price(
                template.coeff9_id, template.coeff8_inter)

    @api.multi
    @api.depends(
        'coeff9_inter', 'taxes_id.amount', 'taxes_id.price_include',
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
            template.theoritical_price = template.coeff9_inter * multi

    @api.multi
    @api.depends(
        'theoritical_price', 'list_price')
    def _compute_has_theoritical_price_different(self):
        for template in self:
            if template.theoritical_price and (
                    template.base_price or template.alternative_base_price):
                template.has_theoritical_price_different =\
                    template.list_price != template.theoritical_price
            else:
                template.has_theoritical_price_different = False
