# custom_approvals/controllers/main.py
from odoo import http
from odoo.http import request

class CustomApprovalsController(http.Controller):

    @http.route('/custom_approvals/go_webpage', type='http', auth='public', website=True)
    def go_webpage(self, **kw):
        # Render a template called 'reset_password' inside your module
        return request.render('custom_approvals_odoo18.reset_password', {})