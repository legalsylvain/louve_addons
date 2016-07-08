# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree
from datetime import datetime

from openerp import fields, models, api, _, SUPERUSER_ID


class DateSearchMixin(models.AbstractModel):
    _name = 'date.search.mixin'

    _SEARCH_DATE_FIELD = False

    search_year = fields.Char(
        string='Year (Search)', compute='_compute_date_search',
        multi='_date_search', store=True, index=True)

    search_month = fields.Char(
        string='Month (Search)', compute='_compute_date_search',
        multi='_date_search', store=True, index=True)

    search_day = fields.Char(
        string='Day (Search)', compute='_compute_date_search',
        multi='_date_search', store=True, index=True)

    @api.multi
    @api.depends()
    def _compute_date_search(self):
        if self._fields[self._SEARCH_DATE_FIELD].type == 'date':
            date_scheme = '%Y-%m-%d'
        elif self._fields[self._SEARCH_DATE_FIELD].type == 'datetime':
            date_scheme = '%Y-%m-%d %H:%M:%S'

        for obj in self:
            date = datetime.strptime(
                getattr(obj, self._SEARCH_DATE_FIELD), date_scheme)
            obj.search_year = date.strftime('%Y')
            obj.search_month = date.strftime('%Y-%m')
            obj.search_day = date.strftime('%Y-%m-%d')

    @api.model
    def create(self, vals):
        print "create"
        print vals
        res = super(DateSearchMixin, self).create(vals)
        if not self._context.get('ignore_date_search', False):
            res.with_context(ignore_date_search=True)._compute_date_search()
        return res

    @api.multi
    def write(self, vals):
        print "write"
        print vals
        res = super(DateSearchMixin, self).write(vals)
        if not self._context.get('ignore_date_search', False) and\
                self._SEARCH_DATE_FIELD in vals.keys():
            self.with_context(ignore_date_search=True)._compute_date_search()
        return res

    # Init values
    def init(self, cr):
        # Init Value only for inherited models
        if self._name != 'date.search.mixin':
            uid = SUPERUSER_ID
            context = {}
            ids = self.search(cr, uid, [
                ('search_year', '=', False),
                ('search_month', '=', False),
                ('search_day', '=', False),
            ], context=context)
            self._compute_date_search(cr, uid, ids, context=context)

    # View Section
    @api.model
    def fields_view_get(
            self, view_id=None, view_type='form', toolbar=False,
            submenu=False):
        res = super(DateSearchMixin, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'search':
            doc = etree.XML(res['arch'])
            # Add search fields
            year_elem = etree.Element('field', name='search_year')
            month_elem = etree.Element('field', name='search_month')
            day_elem = etree.Element('field', name='search_day')
            doc.append(year_elem)
            doc.append(month_elem)
            doc.append(day_elem)

            # Add group by filters
            year_elem = etree.Element(
                'filter', string=_('Year (Search)'),
                context='{"group_by":"search_year"}')
            month_elem = etree.Element(
                'filter', string=_('Month (Search)'),
                context='{"group_by":"search_month"}')
            day_elem = etree.Element(
                'filter', string=_('Day (Search)'),
                context='{"group_by":"search_day"}')
            doc.append(year_elem)
            doc.append(month_elem)
            doc.append(day_elem)

            # Add fields
            res['fields']['search_year'] = {
                'string': _('Year (Search)'), 'searchable': True,
                'type': 'char'}
            res['fields']['search_month'] = {
                'string': _('Month (Search)'), 'searchable': True,
                'type': 'char'}
            res['fields']['search_day'] = {
                'string': _('Day (Search)'), 'searchable': True,
                'type': 'char'}

            res['arch'] = etree.tostring(doc)
        return res
