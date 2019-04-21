# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'demo.wizard'

    project_id = fields.Many2one('demo.project', string=u'项目', require=True)
    test_ids = fields.One2many('demo.many.test', 'wizard_id')

    @api.multi
    def subscribe(self):
        print(self.env.context)
        cache_id = self.env.context['record_id']
        cache = self.env['demo.cache'].sudo().search([('id', '=', cache_id)])
        print(self.project_id.id)
        project = self.env['demo.project'].sudo().search([('id', '=', self.project_id.id)])
        vals = {
            "no": cache.no,
            "name": cache.name,
            "startDate": cache.startDate
        }
        self.env['demo.project'].sudo().create(vals)
        # cache.active = False
        return {}


class WizardManyFields(models.TransientModel):
    _name = 'demo.many.test'
    _transient_max_hours = 12.0

    name = fields.Char()
    wizard_id = fields.Many2one('demo.wizard', ondelete='cascade', string='test')