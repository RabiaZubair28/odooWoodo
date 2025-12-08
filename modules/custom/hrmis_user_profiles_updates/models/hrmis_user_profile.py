from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrmisUserProfile(models.Model):
    _name = "hrmis.user.profile"
    _description = "HRMIS User Profile"
    _rec_name = "employee_id"

    employee_id = fields.Many2one(
        'hr.employee', string="Employee", required=True, ondelete="cascade"
    )
    father_name = fields.Char(string="Father's Name")
    cnic = fields.Char(string="CNIC", required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    cadre = fields.Char(string="Cadre")
    designation = fields.Char(string="Designation")
    bps = fields.Char(string="BPS")
    facility_id = fields.Many2one('x_facility.type', string="Current Posting Facility")
    district_id = fields.Many2one('x_district.master', string="Current Posting District")
    contact_info = fields.Char(string="Contact Info")
    description = fields.Text(string="Additional Notes")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('cnic_unique', 'unique(cnic)', 'CNIC must be unique!')
    ]

    @api.model
    def create(self, vals):
        if self.env['hrmis.user.profile'].search([('employee_id', '=', vals.get('employee_id'))]):
            raise ValidationError("Profile already exists for this employee.")
        return super().create(vals)
