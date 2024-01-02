# -*- coding: utf-8 -*-
from odoo import http

# class EbMergeIssues(http.Controller):
#     @http.route('/eb_merge_issues/eb_merge_issues/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eb_merge_issues/eb_merge_issues/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('eb_merge_issues.listing', {
#             'root': '/eb_merge_issues/eb_merge_issues',
#             'objects': http.request.env['eb_merge_issues.eb_merge_issues'].search([]),
#         })

#     @http.route('/eb_merge_issues/eb_merge_issues/objects/<model("eb_merge_issues.eb_merge_issues"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eb_merge_issues.object', {
#             'object': obj
#         })