from odoo import http, _
from odoo.http import request
from odoo.addons.web.controllers.main import Home




@http.route('/profile/complete', auth='user', website=False)
def profile_complete(self, **kw):
    uid = request.session.uid
    user = request.env['res.users'].sudo().browse(uid)
    # ensure profile exists
    profile = user.profile_id
    if not profile:
        profile = request.env['hr.profile'].sudo().create({'user_id': uid})
        user.sudo().write({'profile_id': profile.id})
    return request.redirect('/web#id=%s&model=hr.profile&view_type=form' % profile.id)
