from odoo import models, fields

class ApprovalType(models.Model):
    _name = "approval.type"
    _description = "Approval Type"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

    # Example: profile_change, leave_request, training_upload etc.
    category = fields.Selection([
        ('profile', 'Profile Change'),
        ('leave', 'Leave Request'),
        ('qualification', 'Qualification/Training'),
        ('other', 'Other')
    ], string="Category", default='other')

    sequence = fields.Integer(string="Sequence", default=10)
