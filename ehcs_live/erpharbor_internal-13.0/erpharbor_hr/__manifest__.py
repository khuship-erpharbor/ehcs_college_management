# -*- coding: utf-8 -*-
{
    'name': 'ERP Harbor HR',
    'category': 'Human Resources',
    'author': 'ERP Harbor Consulting Services',
    'summary': 'ERP Harbor HR',
    'website': 'www.erpharbor.com',
    'version': '13.0.1.0.0',
    'description': """""",
    'depends': [
        'hr_timesheet_attendance',
    ],
    'data': [
        'data/mail_template_data.xml',
        'data/scheduler_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
#         'views/hr_timesheet_view.xml',
    ],
}
