from odoo import models, fields

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    hrmis_profile_id = fields.Many2one('hrmis.user.profile', string="Profile")
    hrmis_service_history_ids = fields.One2many(
        'hrmis.service.history', 
        'employee_id',           
        string="Service History"
    )
    hrmis_training_ids = fields.One2many(
        "hrmis.training.record",
        "employee_id",
        string="Qualifications & Trainings"
    )

    hrmis_cnic = fields.Char(related="hrmis_profile_id.cnic", readonly=True)
    hrmis_father_name = fields.Char(related="hrmis_profile_id.father_name", readonly=True)
    hrmis_date_of_birth = fields.Date(related="hrmis_profile_id.date_of_birth", readonly=True)
    hrmis_joining_date = fields.Date(related="hrmis_profile_id.joining_date", readonly=True)
    hrmis_gender = fields.Selection(related="hrmis_profile_id.gender", readonly=True)
 
    hrmis_cadre = fields.Char(related="hrmis_profile_id.cadre", readonly=True)
    hrmis_designation = fields.Char(related="hrmis_profile_id.designation", readonly=True)
    hrmis_bps = fields.Selection(related="hrmis_profile_id.bps", readonly=True)

    hrmis_contact_info = fields.Char(related="hrmis_profile_id.contact_info", readonly=True)
    hrmis_description    = fields.Text(related="hrmis_profile_id.description", readonly=True)
    hrmis_active = fields.Boolean(related="hrmis_profile_id.active", readonly=True)

    hrmis_district_id = fields.Many2one(related="hrmis_profile_id.district_id", readonly=True)
    hrmis_facility_id = fields.Many2one(related="hrmis_profile_id.facility_id", readonly=True)



    service_postings_district_id = fields.Many2one(related="hrmis_service_history_ids.district_id", readonly=True)
    service_postings_facility_id = fields.Many2one(related="hrmis_service_history_ids.facility_id", readonly=True)

    service_postings_from_date = fields.Date(related="hrmis_service_history_ids.from_date", readonly=True)
    service_postings_to_date = fields.Date(related="hrmis_service_history_ids.to_date", readonly=True)
    service_postings_commission_date = fields.Date(related="hrmis_service_history_ids.commission_date", readonly=True)