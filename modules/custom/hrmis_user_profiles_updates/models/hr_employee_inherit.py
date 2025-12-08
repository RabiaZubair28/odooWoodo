from odoo import models, fields

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    hrmis_profile_id = fields.Many2one('hrmis.user.profile', string="Profile")

    hrmis_cnic = fields.Char(related="hrmis_profile_id.cnic", readonly=True)
    hrmis_father_name = fields.Char(related="hrmis_profile_id.father_name", readonly=True)
    hrmis_date_of_birth = fields.Date(related="hrmis_profile_id.date_of_birth", readonly=True)
    hrmis_gender = fields.Selection(related="hrmis_profile_id.gender", readonly=True)

    hrmis_cadre = fields.Char(related="hrmis_profile_id.cadre", readonly=True)
    hrmis_designation = fields.Char(related="hrmis_profile_id.designation", readonly=True)
    hrmis_bps = fields.Char(related="hrmis_profile_id.bps", readonly=True)

    hrmis_district_id = fields.Many2one(related="hrmis_profile_id.district_id", readonly=True)
    hrmis_facility_id = fields.Many2one(related="hrmis_profile_id.facility_id", readonly=True)

    # def action_open_staff_profile(self):
    #     self.ensure_one()
    #     return {
    #         'name': _('Staff Profile'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'hrmis.user.profile',
    #         'view_mode': 'form',
    #         'target': 'current',
    #         'context': {'default_employee_id': self.id},
    #     }
