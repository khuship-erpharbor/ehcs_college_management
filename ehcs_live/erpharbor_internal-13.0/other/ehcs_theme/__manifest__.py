# -*- coding: utf-8 -*-
{
    'name': "Website ERP Harbor",
    'summary': """ ERP Harbor Website """,
    'description': """ ERP Harbor Website """,
    'author': "ERP Harbor Consulting Services",
    'website': "http://www.erpharbor.com",
    'category': 'Website',
    'version': '13.0.1.0.0',
    'depends': ['theme_treehouse', 'website_hr_recruitment', 'website_crm','website'],
    'data': [
        'data/ehcs_menu.xml',
        'views/web_asset_template.xml',
        'views/footer_template.xml',
        'views/technologies.xml',
        'views/services.xml',
        'views/hire_resources.xml',
        'views/events.xml',
        'views/aboutus.xml',
        # 'views/career.xml',
        # 'views/career_thankyou.xml',
        'views/blog.xml',
        'views/home.xml',
        'views/privacy.xml',
        'views/lead_view.xml',
        'views/inquiry.xml',
    ],
    'qweb': [
        # "static/src/xml/*.xml",
        
    ],
}
