# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    key_file = fields.Binary(string='Key File')
    sheet_key = fields.Char(string='Sheet Key')

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsInherit, self).get_values()
        res['sheet_key'] = (self.env['ir.config_parameter'].sudo().get_param('sheet_key'))
        res['key_file'] = (self.env['ir.config_parameter'].sudo().get_param('key_file'))
        return res

    @api.model
    def set_values(self):
        super(ResConfigSettingsInherit, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('key_file', (self.key_file))
        self.env['ir.config_parameter'].sudo().set_param('sheet_key', (self.sheet_key))
      