# from odoo import http, _
# from odoo.http import request
# from odoo.addons.web.controllers.main import Home

# class AuthHome(Home):

#     @http.route('/web/login', type='http', auth='public', website=True)
#     def web_login(self, redirect=None, **kw):
#         response = super(AuthHome, self).web_login(redirect=redirect, **kw)
#         uid = request.session.uid
#         if uid:
#             user = request.env['res.users'].sudo().browse(uid)
#             # Skip admins
#             if user.is_temp_password and not user.has_group('base.group_system'):
#                 return request.redirect('/force_password_reset')
#         return response

#     @http.route('/force_password_reset', type='http', auth='user', website=True)
#     def force_password_page(self, **kw):
#         return request.render('custom_approvals_odoo18.force_password_template', {})

#     @http.route('/force_password_reset_submit', type='http', auth='user', website=True, methods=['POST'])
#     def force_password_submit(self, **kw):
#         user = request.env.user.sudo()
#         current_password = kw.get('current_password')
#         new_password = kw.get('new_password')
#         confirm_password = kw.get('confirm_password')

#         # Validate current password
#         if not user.check_password(current_password):
#             return request.render('custom_approvals_odoo18.force_password_template', {'error': _('Current password incorrect')})
#         # Validate new passwords match
#         if new_password != confirm_password:
#             return request.render('custom_approvals_odoo18.force_password_template', {'error': _('Passwords do not match')})

#         # Set new password and mark temp flag false
#         user.write({'password': new_password, 'is_temp_password': False})
#         return request.redirect('/web')  # Or redirect to profile page


from odoo import http
from odoo.http import request

class MyCustomController(http.Controller):

    @http.route('/approvals/hello', type='http', auth='public', website=True)
    def public_hello(self, **kw):
        return request.render('custom_approvals_odoo18.hello_template', {
    'message': "Hello, world!"
})