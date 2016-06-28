# -*- coding: utf-8 -*-
# from openerp import http

# class LouveCrmMembership(http.Controller):
#     @http.route('/louve_crm_membership/louve_crm_membership/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route(
# '/louve_crm_membership/louve_crm_membership/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('louve_crm_membership.listing', {
#             'root': '/louve_crm_membership/louve_crm_membership',
#             'objects': http.request.env[
# 'louve_crm_membership.louve_crm_membership'].search([]),
#         })

#     @http.route('/louve_crm_membership/louve_crm_membership/objects/<model(
#    "louve_crm_membership.louve_crm_membership"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('louve_crm_membership.object', {
#             'object': obj
#         })
