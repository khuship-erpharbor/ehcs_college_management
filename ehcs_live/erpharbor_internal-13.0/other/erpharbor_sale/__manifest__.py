# -*- coding: utf-8 -*-
{
    'name': 'ERP Harbor Sale',
    'category': 'Sales',
    'author': 'ERP Harbor Consulting Services',
    'summary': '',
    'website': 'www.erpharbor.com',
    'version': '13.0.1.0.0',
    'description': """
        Hide Tax from Quotation
    """,
    'depends': [
        'sale',
        'erpharbor_base',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/sale_order_report_view.xml'
    ],
}
