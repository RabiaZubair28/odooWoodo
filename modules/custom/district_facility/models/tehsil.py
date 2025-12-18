from odoo import models, fields

class Tehsil(models.Model):
    _name = "tehsil.master"
    _description = "Tehsil"
    _order = "name"

    

    name = fields.Char(string="Tehsil Name", required=True)
    code = fields.Char(string="Tehsil Code")
    facility_id = fields.Many2one('facility.type', string="Facility", required=True)
    district_id = fields.Many2one(related='facility_id.district_id', readonly=True)
    active = fields.Boolean(default=True)
    note = fields.Text(string="Notes")

    _sql_constraints = [
        ('name_district_unique',
         'unique(name, district_id)',
         'Tehsil name must be unique within a district!')
    ]