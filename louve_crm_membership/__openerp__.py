# -*- coding: utf-8 -*-
{
    'name': "louve_crm_membership",

    'summary': """
        Customization of res.partner for Louve@Paris""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Louve@Paris",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/
    # module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/res_partner_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
