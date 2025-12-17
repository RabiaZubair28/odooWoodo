from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    # hrmis_profile_id = fields.Many2one('hrmis.user.profile', string="Profile", readonly=True)
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

    hrmis_cnic = fields.Char(string="CNIC", required=True)
    hrmis_father_name = fields.Char(string="Father's Name")
    hrmis_joining_date = fields.Date(string="Joining Date", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", required=True)

    hrmis_cadre = fields.Char(string="Cadre")
    hrmis_designation = fields.Char(string="Designation")
    hrmis_bps = fields.Selection([
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20')
    ],string="BPS")

    hrmis_tehsil = fields.Many2one('x_tehsil.master', string="Current Posting Tehsil")
    district_id = fields.Many2one('x_district.master', string="Current Posting District")
    facility_id = fields.Many2one(
        'x_facility.type', string="Current Posting Facility",
        domain="[('district_id','=',district_id)]")

    hrmis_contact_info = fields.Char(string="Contact Info")
    hrmis_description    = fields.Text(string="Additional Notes")


    service_postings_district_id = fields.Many2one(related="hrmis_service_history_ids.district_id", readonly=True)
    service_postings_facility_id = fields.Many2one(related="hrmis_service_history_ids.facility_id", readonly=True)

    service_postings_from_date = fields.Date(related="hrmis_service_history_ids.from_date", readonly=True)
    service_postings_to_date = fields.Date(related="hrmis_service_history_ids.to_date", readonly=True)
    service_postings_commission_date = fields.Date(related="hrmis_service_history_ids.commission_date", readonly=True)




    _sql_constraints = [
            ('cnic_unique', 'unique(hrmis_cnic)', 'CNIC must be unique!')
        ]
    

    @api.model_create_multi
    def create(self, vals_list):
        employees = super().create(vals_list)

        for emp in employees:
            if emp.user_id:
                emp.message_post(
                    body="Your employee profile has been created.",
                    partner_ids=[emp.user_id.partner_id.id],
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )

        return employees
    
    def write(self, vals):
        res = super().write(vals)

        for emp in self:
            if emp.user_id:
                emp.message_post(
                    body="Your employee profile has been updated.",
                    partner_ids=[emp.user_id.partner_id.id],
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )

        return res

    @api.onchange('district_id')
    def _onchange_district(self):
        """Filter facilities based on selected district"""
        if self.district_id:
            return {'domain': {'facility_id': [('district_id', '=', self.district_id.id)]}}
        else:
            return {'domain': {'facility_id': []}}
        

    @api.constrains('joining_date', 'date_of_birth')
    def _check_date_range(self):
        today = date.today()
        for rec in self:
            if rec.joining_date and rec.joining_date > today:
                raise ValidationError("Joining Date cannot be in the future.")
            if rec.date_of_birth and rec.date_of_birth > today:
                raise ValidationError("Date of Birth cannot be in the future.")
            

    # def action_open_hrmis_profile(self):
    #     self.ensure_one()

    #     profile = self.hrmis_profile_id

    #     if not profile:
    #         profile = self.env['hrmis.user.profile'].create({
    #             'employee_id': self.id
    #         })
    #         self.hrmis_profile_id = profile.id

    #     return {
    #     'type': 'ir.actions.act_window',
    #     'name': 'HRMIS Profile',
    #     'res_model': 'hrmis.user.profile',
    #     'view_mode': 'form',
    #     'target': 'current',
    #     'context': {'default_employee_id': self.id}  # prefill employee
    # }