from odoo import models, fields

class FacilityType(models.Model):
    _name = "facility.type"
    _description = "Facility Type"

    name = fields.Char(string="Facility Type Name", required=True)
    district_id = fields.Many2one("district.master", string="District", required=True)
    tehsil_ids = fields.One2many('tehsil.master', 'facility_id', string="Tehsils")
    description = fields.Text(string="Description")
    capacity = fields.Integer(string="Capacity")
    active = fields.Boolean(string="Active", default=True)
    category = fields.Selection(
        [('hospital', 'Hospital'), ('clinic', 'Clinic'), ('school', 'School'), ('other', 'Other')],
        string="Category"
    )
