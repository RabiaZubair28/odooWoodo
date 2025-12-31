from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied


class ServicesController(http.Controller):

    @http.route('/services', type='http', auth='user', website=True)
    def force_password_reset(self, **kw):
        return request.render('custom_approvals_odoo18.services_template')
    
    
    
class CompliantController(http.Controller):

    @http.route('/complaints', type='http', auth='user', website=True)
    def compliant_request(self, **kw):
        return request.render('custom_approvals_odoo18.compliants_template')