from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied

class ForcePasswordController(http.Controller):

    @http.route('/force_password_reset', type='http', auth='user', website=True)
    def force_password_reset(self, **kw):
        return request.render('custom_approvals_odoo18.reset_password')

    @http.route(
        '/force_password_reset/submit',
        type='http',
        auth='user',
        methods=['POST'],
        website=True,
        csrf=True
    )
    def force_password_reset_submit(self, **post):
        user = request.env.user

        current_password = post.get('current_password')
        new_password = post.get('new_password')
        confirm_password = post.get('confirm_password')

        # Guardrails
        if not all([current_password, new_password, confirm_password]):
            return request.render(
                'custom_approvals_odoo18.reset_password',
                {'error': 'All fields are required.'}
            )

        if new_password != confirm_password:
            return request.render(
                'custom_approvals_odoo18.reset_password',
                {'error': 'New passwords do not match.'}
            )

        # ✅ Correct Odoo 18 password check
        try:
            user.sudo()._check_credentials(
                {'type': 'password', 'password': current_password},
                request.env
            )
        except Exception:
            return request.render(
                'custom_approvals_odoo18.reset_password',
                {'error': 'Current password is incorrect.'}
            )

        # Update password + clear temp flag
        user.sudo().write({
            'password': new_password,
            'is_temp_password': False,
        })

        # Update session UID so user stays logged in
        request.session.uid = user.id

        return request.redirect('/web')
