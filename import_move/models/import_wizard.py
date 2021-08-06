import openpyxl
import xlrd
import base64
import csv
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools import ustr


class ModelName(models.TransientModel):
    _name = 'import.move'
    _description = 'Import'

    excel_file = fields.Binary(string = "Upload Excel", attachment = True)

    def load_invoice(self):
        with open('file.csv', 'wb') as p:
            p.write(base64.b64decode(self.excel_file))
        csvfile = open('file.csv', 'rt')
        objects = csv.DictReader(csvfile)
        product = self.env['product.template']
        for obj in objects:
            if obj.get('Name'):
                product = self.env['product.template'].search([('name', '=', obj.get('Name'))])
                product.attribute_line_ids = False
                product.seller_ids = False
                if not product:
                    internal_reference = obj.get('Internal Reference')
                    name = obj.get('Name')
                    prod_category = obj.get('Product Category')
                    if prod_category:
                        category_id = self.env['product.category'].search([('name', '=', prod_category)], limit = 1)
                        if not category_id:
                            category_id = self.env['product.category'].create({'name': prod_category}).id
                        else:
                            category_id = category_id.id
                    else:
                        category_id = False
                    responsible = obj.get('Product Category')
                    if responsible:
                        responsible_id = self.env['res.users'].search([('name', '=', responsible)], limit = 1)
                        if responsible_id:
                            responsible_id = responsible_id.id
                    else:
                        responsible_id = False
                    uom = obj.get('Unit of Measure')
                    if uom:
                        uom_id = self.env['uom.uom'].search([('name', '=', uom)], limit = 1)
                        if uom_id:
                            uom_id = uom_id.id
                        else:
                            uom_category = self.env['uom.category'].create({'name': uom}).id
                            uom_id = self.env['uom.uom'].create({
                                'name': uom,
                                'category_id': uom_category
                            }).id
                    else:
                        uom_id = self.env['uom.uom'].search([], limit = 1).id
                    list_price = obj.get('Sales Price')
                    standard_price = obj.get('Cost')
                    hkd = obj.get('HKD')
                    if hkd:
                        currency = self.env['res.currency'].search([('name', '=', hkd)])
                        if currency:
                            currency = currency.id
                        else:
                            currency = self.env.company.currency_id.id
                    else:
                        currency = self.env.company.currency_id.id
                    track = obj.get('Tracking', False)
                    if track:
                        if track == 'lot':
                            tracking = track
                        elif track == 'serial':
                            tracking = track
                        else:
                            tracking = False
                    else:
                        tracking = 'none'
                    product = self.env['product.template'].create({
                        'name': name,
                        'type': 'product',
                        'default_code': internal_reference,
                        'categ_id': category_id,
                        'responsible_id': responsible_id,
                        'uom_id': uom_id,
                        'uom_po_id': uom_id,
                        'list_price': list_price,
                        'standard_price': standard_price,
                        'currency_id': currency,
                        'tracking': tracking,
                    })
            if product:
                product_attributes = obj.get('Product Attributes')
                if product_attributes:
                    attribute_id = self.env['product.attribute'].search([('name', '=', product_attributes)], limit = 1)
                    if not attribute_id:
                        attribute_id = self.env['product.attribute'].create({'name': product_attributes}).id
                    else:
                        attribute_id = attribute_id.id
                    attribute_values = obj.get('Product Attributes/Values')
                    value_ids = []
                    if product_attributes:
                        values = attribute_values.split('|')
                        for value in values:
                            value_id = self.env['product.attribute.value'].search(
                                [('name', '=', value), ('attribute_id', '=', attribute_id)], limit = 1)
                            if not value_id:
                                value_id = self.env['product.attribute.value'].create(
                                    {'name': value, 'attribute_id': attribute_id}).id
                            else:
                                value_id = value_id.id
                            value_ids.append((4, value_id))
                        product.attribute_line_ids = [(0,0, {'attribute_id' : attribute_id, 'value_ids': value_ids })]
                vendor = obj.get('Vendors / Vendor')
                vendor_currency = obj.get('Vendors / Currency')
                if vendor_currency:
                    vendor_currency_id = self.env['res.currency'].search([('name', '=', vendor_currency)])
                    if vendor_currency_id:
                        vendor_currency_id = vendor_currency_id.id
                    else:
                        vendor_currency_id = self.env.company.currency_id.id
                else:
                    vendor_currency_id = self.env.company.currency_id.id
                if vendor:
                    vendor_id = self.env['res.partner'].search([('name','=', vendor)])
                    if not vendor_id:
                        vendor_id = self.env['res.partner'].with_context({'search_default_supplier': 1,'res_partner_search_mode': 'supplier', 'default_is_company': True, 'default_supplier_rank': 1}).create({'name' : vendor}).id
                    else:
                        vendor_id = vendor_id.id
                    vendor_price = obj.get('Vendors/ Price') or 0
                    product.seller_ids = [(0,0, {'name' : vendor_id, 'price' : vendor_price, 'currency_id' : vendor_currency_id})]