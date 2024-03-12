# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers import main


class HarborWebsite(main.Website):

    @http.route(['/request_quote'], type='json', auth='public', method="POST",
                website=True)
    def request_quote(self, **kw):
#         print("\n\n->request_quote >>>>>", kw, "\n")
        file_name = (str(kw.get('fileupload'))).split(",")
        file_data = (str(kw.get('image'))).split(",")
        kw.pop('fileupload', False)
        kw.pop('image', False)
        if kw.get('requirement_ids') == 0:
            kw.pop('requirement_ids', False)
        else:
            req_ids = eval(kw.get('requirement_ids')[0])
            if isinstance(req_ids, tuple) and len(req_ids) > 1:
                req_ids = list(req_ids)
            else:
                req_ids = [req_ids]
            kw['requirement_ids'] = [(6, 0, req_ids)]
        lead_id = request.env['crm.lead'].sudo().create(kw).id
        # self.send_email(lead_id)

        # Create attachmen
        attachment_indx = 0
        attachment_obj = request.env['ir.attachment']
        for value in file_name:
            if not value:
                continue
            attachment_value = {
                'name': file_name[attachment_indx],
                'datas': file_data[attachment_indx],
                'res_model': 'crm.lead',
                'res_id': lead_id,
                # 'datas_fname': file_name[attachment_indx],
            }
            attachment_obj.sudo().create(attachment_value)
            attachment_indx += 1
        return True
    

class EhcsThemeHome(http.Controller):

    @http.route('/', type='http', auth='public', website=True)
    def blog(self, **kw):
        return request.render('ehcs_theme.theme_menu_home_two', {})
    
    @http.route('/inquiry_page', type='http', auth='public', website=True)
    def get_data(self, **kw):
        requirements = request.env['project.requirement'].sudo().search([])
        return request.render('ehcs_theme.theme_menu_inquiry_page', {
            'requirement_ids': requirements,
        })


class EhcsThemeServices(http.Controller):

    @http.route('/ehcs_services/', type='http', auth='public', website=True)
    def services(self, **kw):
        return request.render('ehcs_theme.theme_menu_services_two', {})


class EhcsThemeTechnologies(http.Controller):

    @http.route('/ehcs_technologies/', type='http', auth='public', website=True)
    def technologies(self, **kw):
        return request.render('ehcs_theme.theme_menu_technologies_two', {})


class EhcsThemeHireResources(http.Controller):

    @http.route('/ehcs_hire-resources/', type='http', auth='public', website=True)
    def hireresources(self, **kw):
        return request.render('ehcs_theme.theme_menu_hire-resources_two', {})


class EhcsThemeEvents(http.Controller):

    @http.route('/ehcs_events', type='http', auth='public', website=True)
    def events(self, **kw):
        return request.render('ehcs_theme.theme_menu_events_two', {})


class EhcsThemeAboutus(http.Controller):

    @http.route('/ehcs_aboutus', type='http', auth='public', website=True)
    def aboutus(self, **kw):
        return request.render('ehcs_theme.theme_menu_aboutus_two', {})


class EhcsThemeCareer(http.Controller):

    @http.route('/ehcs_career', type='http', auth='public', website=True)
    def career(self, **kw):
        return request.render('ehcs_theme.theme_menu_career_two', {})


class EhcsThemeCareerRedirect(http.Controller):

    @http.route('/job-thank-you', type='http', auth='public', website=True)
    def career(self, **kw):
        return request.render('ehcs_theme.theme_menu_career_redirect', {})


class EhcsThemeBlog(http.Controller):

    @http.route('/ehcs_blog', type='http', auth='public', website=True)
    def blog(self, **kw):
        return request.render('ehcs_theme.theme_menu_blog_two', {})


class EhcsThemePrivacy(http.Controller):

    @http.route('/privacy_page', type='http', auth='public', website=True)
    def career(self, **kw):
        return request.render('ehcs_theme.theme_menu_privacy_page', {})


class EhcsThemeQuote(http.Controller):

    @http.route('/inquiry_page', type='http', auth='public', website=True)
    def career(self, **kw):
        return request.render('ehcs_theme.theme_menu_inquiry_page', {})
