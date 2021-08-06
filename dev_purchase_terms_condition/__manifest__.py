# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Purchase Terms and Conditions',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Purchases',
    'description':
        """
        This Module add below functionality into odoo

        1.Purchase Terms and Condition\n

Odoo purchase terms conditions 
Odoo terms conditions 

    """,
    'summary': 'Odoo app allow to add Terms and Condition into Purchase Order, Purchase terms condition, vendor terms condition, supplier terms condition, purchase product terms condition',
    'author': 'Devintelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/term_condition_view.xml',
        'views/purchase_view.xml',
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':10.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
