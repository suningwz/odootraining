# -*- coding: utf-8 -*-
{
    'name': "demo",

    'summary': """
        模块简介""",

    'description': """
        关于模块的描述
    """,

    'author': "bt",
    'website': "网站链接",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/import_views.xml',
        'views/templates.xml',
        'views/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'qweb': [
        "static/src/xml/demo.xml",
    ],
    'application': True,
}