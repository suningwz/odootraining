# -*- coding: utf-8 -*-
from odoo import http


class Demo(http.Controller):
    @http.route('/demo/demo/', auth='user', type='http')
    def indexa(self, **post):
        print(post)
        return "type:http;auth:user"

    @http.route('/demo/public/', auth='public', type='http')
    def indexb(self, **kw):
        return "type:http;auth:public"

    @http.route('/demo/none/', auth='none', type='http')
    def indexc(self, **kw):
        return "type:http;auth:none"

    @http.route('/demo/json/', auth='user', type='json')
    def indexd(self, **kw):
        return "type:json;auth:user"

    @http.route('/demo/csrfF/', auth='user', type='http', csrf=False)
    def indexe(self, **kw):
        return "type:http;auth:user;csrf:false"

    @http.route('/demo/demo/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('demo.listing', {
            'root': '/demo/demo',
            'objects': http.request.env['demo.project'].search([]),
        })

    @http.route('/demo/demo/objects/<model("demo.project"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('demo.object', {
            'object': obj
        })