# -*- coding: utf-8 -*-
{
    'name': "Website Customisations",
    'sequence': 0,
    'summary': """Customisations with in the ecommerce website""",

    'description': """Odoo14 ecommerce website customisations""",

    'author': 'Odoo SA,Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'category': 'eCommerce',
    'version': '14.0.1.0.0',

    'depends': ['sale', 'purchase', 'website_sale', 'website_sale_comparison', 'website_sale_wishlist',
                'sales_customisation', 'auth_totp_portal', 'project', 'sign'],
    'qweb': ['static/src/xml/price_hide.xml'],
    'data': [
        'data/mail_template.xml',
        'views/hide_price.xml',
        'views/show_attribute.xml',
        'views/restrict_attribute.xml',
        'views/wizard_checkout_hide.xml',
        'views/request_quotation.xml',
        'views/quotation_conform.xml',
        'views/remove_hyperlink.xml',
        'views/two_factor_auth_hide.xml',
        'views/portal_docs_hide.xml',
        'views/templates.xml',
        'views/all_prod_attr_hiding.xml',
        'views/button_replace.xml',
        'views/mail_notification_template.xml',
        'views/mail_notification_paynow.xml',
    ],
    'demo': [
    ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
