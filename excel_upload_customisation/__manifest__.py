# -*- coding: utf-8 -*-
{
    'name': "Upload excel from Lots/serial No",
    'sequence': 0,
    'summary': """Customisations in the inventory""",
    'description': """Customisations in the inventory""",
    'author': 'Odoo SA,Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    'depends': ['base', 'stock', 'purchase'],

    'data': [
        'security/ir.model.access.csv',
        'views/lot_sn_tree_view.xml',
        'views/importing.xml',
    ],
    'demo': [
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
