# -*- coding: utf-8 -*-

from odoo import models, fields, api
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account  
import os

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id:
            data = {}
            SERVICE_ACCOUNT_FILE = os.getcwd() + '/keys.json'
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            creds = None
            creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            service = build('sheets', 'v4', credentials=creds)
            SAMPLE_SPREADSHEET_ID = self.env['ir.config_parameter'].sudo().get_param('sheet_key')
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range='Sheet1!A2:D26').execute()
            for li in result.get('values'):
                if li[0] == self.product_id.name:
                    self.price_unit = float(li[3].replace('$',''))
                    break;
        return res