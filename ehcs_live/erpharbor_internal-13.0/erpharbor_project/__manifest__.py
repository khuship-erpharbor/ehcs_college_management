# -*- coding: utf-8 -*-
{
    'name': 'ERP Harbor Project',
    'category': 'Project Management',
    'author': 'ERP Harbor Consulting Services',
    'summary': 'ERP Harbor Project',
    'website': 'www.erpharbor.com',
    'version': '13.0.1.0.0',
    'description': """""",
    'depends': [
        'project',
        'hr_timesheet',
        'hr',
        'mail',
    ],
    'data': [
        'data/cron.xml',
        'data/mail_template.xml',
        'wizard/wiz_update_tms_entries.xml',
        'views/project_view.xml',
        'views/employees_view.xml',
    ],
}
