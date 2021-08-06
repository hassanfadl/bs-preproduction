{
    'name': 'Import Invoice',
    'version': '13.0.1.0.1',
    'summary': 'Import Invoice',
    'description': 'Import Invoice',
    'category': 'Tools',
    'author': 'Cybrosys',
    'website': 'Website',
    'license': 'AGPL-3',
    'depends': ['account', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/import_wizard.xml',
    ],
    'installable': True,
    'auto_install': False
}
