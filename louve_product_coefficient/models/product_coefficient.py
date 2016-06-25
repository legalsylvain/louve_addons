# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Smile (<http://www.smile.fr>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api

TYPE = [('multi', 'Multi'),
        ('amount', 'Amount')]


class ProductCoefficient(models.Model):
    _name = 'product.coefficient'
    code = fields.Char()
    type = fields.Selection(TYPE, required=True, default='multi')
    name = fields.Char()
    value = fields.Float(default=1.0)


class ProductCategory(models.Model):
    _inherit = 'product.category'
    coeff1_id = fields.Many2one('product.coefficient',
                                'Coeff Perte',
                                domain="[('code','like','COEFF')]")
    coeff2_id = fields.Many2one('product.coefficient',
                                'Coeff2',
                                domain="[('code','like','COEFF')]")
    coeff3_id = fields.Many2one('product.coefficient',
                                'Coeff3',
                                domain="[('code','like','COEFF')]")
    coeff4_id = fields.Many2one('product.coefficient',
                                'Coeff4',
                                domain="[('code','like','COEFF')]")
    coeff5_id = fields.Many2one('product.coefficient',
                                'Coeff5',
                                domain="[('code','like','COEFF')]")
    coeffLOUVE_id = fields.Many2one('product.coefficient',
                                    'LOUVE margin',
                                    domain="[('code','like','MRG')]")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    coeff1_id = fields.Many2one(
        'product.coefficient',
        'Coeff Perte',
        related='categ_id.coeff1_id',
        domain="[('code','like','COEFF')]")
    coeff2_id = fields.Many2one(
        'product.coefficient',
        'Coeff2',
        related='categ_id.coeff2_id',
        domain="[('code','like','COEFF')]")
    coeff3_id = fields.Many2one(
        'product.coefficient',
        'Coeff3',
        related='categ_id.coeff3_id',
        domain="[('code','like','COEFF')]")
    coeff4_id = fields.Many2one(
        'product.coefficient',
        'Coeff4',
        related='categ_id.coeff4_id',
        domain="[('code','like','COEFF')]")
    coeff5_id = fields.Many2one(
        'product.coefficient',
        'Coeff5',
        related='categ_id.coeff5_id',
        domain="[('code','like','COEFF')]")
    coeffLOUVE_id = fields.Many2one(
        'product.coefficient',
        'LOUVE margin',
        related='categ_id.coeffLOUVE_id',
        domain="[('code','like','MRG')]")

    @api.one
    @api.depends('standard_price')
    def _compute_base_price(self):
        self.base_price = self.standard_price

    @api.one
    @api.depends('coeff1_id', 'standard_price')
    def _compute_coeff1(self):
        self.coeff1_inter = self.base_price
        if self.coeff1_id.value is not False:
            if self.coeff1_id.type == "multi":
                self.coeff1_inter = (self.base_price +
                                     (self.base_price * self.coeff1_id.value))
            else:
                self.coeff1_inter = self.base_price + self.coeff1_id.value

    @api.one
    @api.depends('coeff2_id', 'coeff1_inter', 'standard_price')
    def _compute_coeff2(self):
        self.coeff2_inter = self.coeff1_inter
        if self.coeff2_id.value is not False:
            if self.coeff2_id.type == "multi":
                self.coeff2_inter = (self.coeff1_inter +
                                     (self.base_price * self.coeff2_id.value))
            else:
                self.coeff2_inter = self.coeff1_inter + self.coeff2_id.value
        else:
            self.coeff2_inter = self.coeff1_inter

    @api.one
    @api.depends('coeff3_id', 'coeff2_inter', 'standard_price')
    def _compute_coeff3(self):
        if self.coeff3_id.value is not False:
            if self.coeff3_id.type == "multi":
                self.coeff3_inter = (self.coeff2_inter +
                                     (self.base_price * self.coeff3_id.value))
            else:
                self.coeff3_inter = self.coeff2_inter + self.coeff3_id.value
        else:
            self.coeff3_inter = self.coeff2_inter

    @api.one
    @api.depends('coeff4_id', 'coeff3_inter', 'standard_price')
    def _compute_coeff4(self):
        if self.coeff4_id.value is not False:
            if self.coeff4_id.type == "multi":
                self.coeff4_inter = (self.coeff3_inter +
                                     (self.base_price * self.coeff4_id.value))
            else:
                self.coeff4_inter = self.coeff3_inter + self.coeff4_id.value
        else:
            self.coeff4_inter = self.coeff3_inter

    @api.one
    @api.depends('coeff5_id', 'coeff4_inter', 'standard_price')
    def _compute_coeff5(self):
        if self.coeff5_id.value is not False:
            if self.coeff5_id.type == "multi":
                self.coeff5_inter = (self.coeff4_inter +
                                     (self.base_price * self.coeff5_id.value))
            else:
                self.coeff5_inter = self.coeff4_inter + self.coeff5_id.value
        else:
            self.coeff5_inter = self.coeff4_inter

    @api.multi
    # with @api.depends & smile.base installed get a crash of dependecies
    # otherwise a "WARNING :'taxes_id' params must be field names"
    # but taxes are computed correctly
    @api.onchange(
        'coeffLOUVE_id',
        'coeff5_inter',
        'standard_price',
        'taxes_id')
    def _compute_coeffLOUVE(self):
        _tt = 0.0
        if self.coeffLOUVE_id.value is not False:
            self.with_margin = (self.coeff5_inter +
                                (self.coeff5_inter * self.coeffLOUVE_id.value))
            if len(self.taxes_id) > 0:
                for t in self.taxes_id:
                    _tt += t.amount
            self.list_price = self.with_margin
            self.lst_price = self.list_price
            self.info_price = self.list_price + (self.list_price * _tt)
        else:
            if len(self.taxes_id) > 0:
                for t in self.taxes_id:
                    _tt += t.amount
            self.with_margin = self.coeff5_inter
            self.list_price = self.with_margin
            self.lst_price = self.list_price
            self.info_price = self.list_price + (self.list_price * _tt)

    base_price = fields.Float('prix de base', compute='_compute_base_price')
    coeff1_inter = fields.Float('avec perte', compute='_compute_coeff1')
    coeff2_inter = fields.Float('avec Coeff 2', compute='_compute_coeff2')
    coeff3_inter = fields.Float('avec Coeff 3', compute='_compute_coeff3')
    coeff4_inter = fields.Float('avec Coeff 4', compute='_compute_coeff4')
    coeff5_inter = fields.Float('avec Coeff 5', compute='_compute_coeff5')
    with_margin = fields.Float('avec Marge', compute='_compute_coeffLOUVE')
    info_price = fields.Float(
        'Prix avec taxes',
        compute="_compute_coeffLOUVE")
