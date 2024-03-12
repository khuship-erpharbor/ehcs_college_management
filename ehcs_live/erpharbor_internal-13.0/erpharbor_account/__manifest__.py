# -*- coding: utf-8 -*-
{
    'name': 'ERP Harbor Account',
    'category': 'Accounting',
    'author': 'ERP Harbor Consulting Services',
    'summary': '',
    'website': 'http://www.erpharbor.com',
    'version': '13.0.1.0.0',
    'description': """
        ERP Harbor Account
    """,
    'depends': [
        'account',
        'hr_payroll_community',
    ],
    'data': [
        'data/account_data.xml',
        'report/account_report.xml',
        'report/ehcs_report_invoice.xml',
        'views/res_company_view.xml',
        'views/journal_view.xml',
        'views/account_payment_view.xml',
        'views/hr_payslip_view.xml',
    ],
}
