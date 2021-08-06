# -*- coding: utf-8 -*-
{
    'name': "Tolerence Customizations",
    'sequence': 1,
    'summary': """Customisations with in the  sales module""",

    'description': """Odoo14  customisations""",

    'author': 'Odoo SA,Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'category': 'eCommerce',
    'version': '14.0.1.0.0',

    'depends': ['base', 'sale'],
    'qweb': [],
    'data': [
        'views/views.xml',
    ],
    'demo': [
    ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
