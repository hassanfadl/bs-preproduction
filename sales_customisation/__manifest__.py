# -*- coding: utf-8 -*-
{
    'name': "Sales Customisations",
    'sequence': 0,

    'summary': """Customisations in the sales""",

    'description': """Customisations in the sales""",

    'author': 'Odoo SA,Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',

    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    'depends': ['base', 'sale', 'stock','account','purchase', 'website_sale', 'sale_stock'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_rule.xml',
        'data/cron.xml',
        'report/proforma_hide_report.xml',
        'report/rfq_hide.xml',
        'views/views.xml',
        'views/res_partner_view.xml',
        'views/product_color_view.xml',
        'views/account_move_view.xml',
        'views/stock_move_view.xml',
        'views/purchase_order_view.xml',
    ],
    'demo': [
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
