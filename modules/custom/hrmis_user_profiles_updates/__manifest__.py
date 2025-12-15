{
    'name': "HRMIS User Profiles Updates",
    'version': "1.0",
    'summary': "Staff Personal Information Profile - Read Only for Employees",
    'category': 'Human Resources',
    'author': "Humza Aqeel Shaikh",
    'depends': ['hr', 'district_facility'],
    'data': [
        'security/ir.model.access.csv',
        'views/hrmis_user_profile_views.xml',
        'views/hr_employee_inherit.xml',
        'views/hrmis_user_services_views.xml',
        'views/hrmis_training_views.xml',
        'data/mail_server_data.xml'
    ],
    'installable': True,
    'application': False,
}
