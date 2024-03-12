# -*- coding: utf-8 -*-
{
    'name': 'ERP Harbor Accounting HR',
    'category': 'Human Resources',
    'author': 'ERP Harbor Consulting Services',
    'summary': 'ERP Harbor Accounting HR',
    'website': 'www.erpharbor.com',
    'version': '13.0.1.0.0',
    'description': """""",
    'depends': [
        'hr_contract',
    ],
    'data': [
        "views/hr_contract_view.xml",
        "report/report.xml",
        "report/report_appointment_letter_template.xml",
        "report/report_header_footer_template.xml",
    ],
}
