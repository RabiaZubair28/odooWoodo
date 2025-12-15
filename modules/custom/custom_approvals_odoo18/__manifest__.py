{
    "name": "Custom Approvals",
    "version": "1.0.0",
    "author": "Aneeqa",
    "depends": ["base", "hr", "website" ],
    "data": [
        # 'views/approval_views.xml',
        "security/ir.model.access.csv",
        'views/hello_template.xml',
        'views/force_password_template.xml',
        "views/custom_approvals.xml",
        "views/res_user_views.xml",
       
    ],
#    'assets': {
#     'web.assets_backend': [
#         'custom_approvals_odoo18/static/src/js/redirect.js',
#     ],
# },


    # 'controllers':[
    #     'controllers/auth.py',
    #     'controllers/profile_complete.py',
    # ],
    "installable": True,
    "application": False,
}
